"""Read-only job mail over IMAP, for agents without a mail tool. Standard library only.

Settings come from the environment, never from files in the workspace:
  GRADBO_IMAP_USER      the mailbox address
  GRADBO_IMAP_PASSWORD  an app password (Gmail: Google Account > Security > App passwords)
  GRADBO_IMAP_HOST      default imap.gmail.com (Outlook.com and Microsoft 365 need OAuth and
                        don't take app passwords; use a mail connector in the agent instead)

Commands
  codes [--minutes 30] [--from DOMAIN]   verification codes and links from the last few minutes
  scan [--days 14] [--domains a.com,b.com]
                                         recruiting mail (applicant tracking systems, plus the given
                                         employer domains), each classified as confirmation, rejection,
                                         interview, offer, viewed, verification or reply

The mailbox is opened read-only: nothing is marked read, moved, deleted or sent.
"""
from __future__ import annotations

import email
import imaplib
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from email.header import decode_header, make_header
from email.utils import parseaddr, parsedate_to_datetime
from html import unescape

ATS_DOMAINS = (
    "greenhouse.io", "greenhouse-mail.io", "lever.co", "hire.lever.co", "myworkday.com", "myworkdayjobs.com",
    "workday.com", "smartrecruiters.com", "ashbyhq.com", "taleo.net", "oracle.com", "oraclecloud.com",
    "successfactors.com", "successfactors.eu", "sap.com", "icims.com", "teamtailor.com", "personio.de",
    "personio.com", "bamboohr.com", "recruitee.com", "workable.com", "jobvite.com", "pinpointhq.com",
    "tal.net", "avature.net", "eightfold.ai", "beamery.com", "applytojob.com", "hirebridge.com",
)
VERIFY = re.compile(r"verification (?:code|link|e-?mail)|verify (?:your )?(?:\w+ )?(?:email|e-mail|account|identity|address)|"
                    r"one[- ]time (?:pass)?code|security code|confirm (?:your )?(?:\w+ )?(?:email|e-mail|account|address)|"
                    r"activate (?:your )?(?:\w+ )?account|your code is|passcode", re.I)
OFFER = re.compile(r"pleased to offer|offer of employment|job offer|offer letter|formal offer", re.I)
REJECT = re.compile(r"unfortunately|not (?:be )?(?:moving|progressing|proceeding) (?:forward )?with|unsuccessful|"
                    r"other candidates|decided not to|no longer (?:being )?considered|regret to inform|not been selected", re.I)
INTERVIEW = re.compile(r"\binterview\b|invit(?:e|ation) (?:you )?to (?:an? )?(?:assessment|call|chat|meet)|next stage|"
                       r"assessment cent(?:re|er)|online assessment|schedule a (?:call|chat|time)|your availability|book a slot", re.I)
CONFIRM = re.compile(r"thank(?:s| you) for (?:your )?appl|application (?:has been )?(?:received|submitted)|"
                     r"we(?:'ve| have) received your application|successfully applied", re.I)
VIEWED = re.compile(r"(?:being|under) review|reviewing your application|has been viewed|application update", re.I)
# A code is 4-8 digits, two groups of three, or 6-8 mixed letters and digits ("1PdQMc8K").
CODE_TOKEN = re.compile(r"(?<![\w/=.@#-])(?:\d{3}[ -]\d{3}|\d{4,8}|(?=[A-Za-z0-9]*\d)(?=[A-Za-z0-9]*[A-Za-z])[A-Za-z0-9]{6,8})(?![\w/=@-]|\.\w)")
CODE_NEAR = re.compile(r"\b(?:code|passcode|pin|otp)\b", re.I)
LINK = re.compile(r"https://[^\s\"'<>)\]]+", re.I)
ACTION_LINK = re.compile(r"verif|confirm|activat|validate|token|registration|signup|register", re.I)
IGNORED_LINK = re.compile(r"unsubscribe|privacy|preferences|help|support|terms|cookie|\.(?:png|jpe?g|gif|css)(?:\?|$)", re.I)


def classify(subject: str, body: str) -> str:
    text = f"{subject}\n{body[:6000]}"
    for name, pattern in (("verification", VERIFY), ("offer", OFFER), ("rejection", REJECT),
                          ("interview", INTERVIEW), ("confirmation", CONFIRM), ("viewed", VIEWED)):
        if pattern.search(text):
            return name
    return "reply"


def codes_in(body: str) -> list[str]:
    found = []
    for match in CODE_NEAR.finditer(body):
        window = body[match.end():match.end() + 80]
        token = CODE_TOKEN.search(window)
        if token and token.group() not in found:
            found.append(token.group())
    return found


ACTION_TEXT = re.compile(r"confirm|verif|activat|validate|complete (?:your )?registration|set (?:up )?(?:your )?password|"
                         r"click here to (?:confirm|verify|activate)|get started", re.I)
ANCHOR = re.compile(r"<a\b[^>]*?href\s*=\s*([\"'])(https://[^\"']+)\1[^>]*>(.*?)</a>", re.I | re.S)


def links_in(body: str, html: str = "") -> list[str]:
    """Confirmation and verification links, best first: buttons in the HTML
    whose words say confirm or verify (often behind a tracking address),
    then addresses that say so themselves, then plain-text links right after
    such words. Footer links (unsubscribe, privacy) are left out."""
    found: list[str] = []
    for _, url, text in ANCHOR.findall(html or ""):
        words = unescape(re.sub(r"<[^>]+>", " ", text))
        url = unescape(url)
        if (ACTION_TEXT.search(words) or ACTION_LINK.search(url)) and not IGNORED_LINK.search(url):
            found.append(url)
    found += [l for l in LINK.findall(body) if ACTION_LINK.search(l) and not IGNORED_LINK.search(l)]
    for match in ACTION_TEXT.finditer(body):
        after = LINK.search(body[match.end():match.end() + 160])
        if after and not IGNORED_LINK.search(after.group()):
            found.append(after.group())
    return [l.rstrip(".,;") for l in dict.fromkeys(found)][:3]


def html_of(message) -> str:
    return "\n".join(_decode(part.get_payload(decode=True) or b"", part.get_content_charset())
                     for part in message.walk() if part.get_content_type() == "text/html" and not part.get_filename())


def domain(address: str) -> str:
    return parseaddr(address)[1].rsplit("@", 1)[-1].lower()


def _decode(payload: bytes, charset: str | None) -> str:
    """A part's text, whatever charset it claims: an unknown one (unknown-8bit,
    a misspelling) falls back to UTF-8 rather than failing the whole read."""
    try:
        return payload.decode(charset or "utf-8", errors="replace")
    except LookupError:
        return payload.decode("utf-8", errors="replace")


def text_of(message) -> str:
    plain, html = [], []
    for part in message.walk():
        kind = part.get_content_type()
        if kind not in ("text/plain", "text/html") or part.get_filename():
            continue
        text = _decode(part.get_payload(decode=True) or b"", part.get_content_charset())
        (plain if kind == "text/plain" else html).append(text)
    if plain:
        return "\n".join(plain)
    raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", "\n".join(html))
    return unescape(re.sub(r"<[^>]+>", " ", raw))


def connect() -> imaplib.IMAP4_SSL:
    user, password = os.environ.get("GRADBO_IMAP_USER"), os.environ.get("GRADBO_IMAP_PASSWORD")
    if not user or not password:
        sys.exit("Set GRADBO_IMAP_USER and GRADBO_IMAP_PASSWORD (an app password) in the environment.")
    box = imaplib.IMAP4_SSL(os.environ.get("GRADBO_IMAP_HOST", "imap.gmail.com"))
    box.login(user, password)
    box.select("INBOX", readonly=True)
    return box


def messages(box, since: datetime):
    status, data = box.search(None, "SINCE", since.strftime("%d-%b-%Y"))
    for num in reversed((data[0] or b"").split()[-300:]):
        status, parts = box.fetch(num, "(BODY.PEEK[])")
        if status != "OK" or not parts or not isinstance(parts[0], tuple):
            continue
        message = email.message_from_bytes(parts[0][1])
        try:
            when = parsedate_to_datetime(message["Date"])
            when = when if when.tzinfo else when.replace(tzinfo=timezone.utc)
        except (TypeError, ValueError):
            continue
        if when < since:
            continue
        yield when, message


def is_recruiting(sender_domain: str, extra: tuple[str, ...]) -> bool:
    return any(sender_domain == d or sender_domain.endswith("." + d) for d in ATS_DOMAINS + extra)


def header(message, name: str) -> str:
    try:
        return str(make_header(decode_header(message[name] or "")))
    except (LookupError, UnicodeError, ValueError):
        return str(message[name] or "")  # a malformed encoded header: its raw text


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    command, args = argv[0], dict(zip(argv[1::2], argv[2::2]))
    now = datetime.now(timezone.utc)
    box = connect()
    try:
        if command == "codes":
            since = now - timedelta(minutes=int(args.get("--minutes", 30)))
            want = args.get("--from", "").lower()
            shown = 0
            for when, message in messages(box, since):
                sender = domain(message["From"] or "")
                if want and not (sender == want or sender.endswith("." + want)):
                    continue
                body, subject = text_of(message), header(message, "Subject")
                if classify(subject, body) != "verification":
                    continue
                shown += 1
                print(f"{when:%Y-%m-%d %H:%M} UTC  from {sender}  subject: {subject}")
                print(f"  codes: {', '.join(codes_in(body)) or 'none found'}")
                for link in links_in(body, html_of(message)):
                    print(f"  link: {link}")
            if not shown:
                print("No verification mail yet. Wait a minute and run this again.")
        elif command == "scan":
            since = now - timedelta(days=int(args.get("--days", 14)))
            extra = tuple(d.strip().lower() for d in args.get("--domains", "").split(",") if d.strip())
            for when, message in messages(box, since):
                sender = domain(message["From"] or "")
                if not is_recruiting(sender, extra):
                    continue
                body, subject = text_of(message), header(message, "Subject")
                kind = classify(subject, body)
                snippet = " ".join(body.split())[:200]
                print(f"{when:%Y-%m-%d}  {kind:<12}  {sender}  {subject}\n  {snippet}")
        else:
            print(__doc__)
            return 2
    finally:
        box.logout()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
