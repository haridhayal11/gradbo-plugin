"""Check this machine has what the Gradbo skill uses, and say how to install what's missing.
Standard library only, so it runs before anything else is installed.

  python doctor.py            a checklist for people
  python doctor.py --json     the same as JSON
  python doctor.py --mail     also try logging in to IMAP with GRADBO_IMAP_USER / GRADBO_IMAP_PASSWORD

The Gradbo connection, the browser tool and any mail connector live in the agent, not on
the machine; the agent checks those itself (references/install.md).
"""
from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

SYSTEM = {"Darwin": "macos", "Windows": "windows"}.get(platform.system(), "linux")

FIX = {
    "uv": {"macos": "brew install uv   (or: curl -LsSf https://astral.sh/uv/install.sh | sh)",
           "linux": "curl -LsSf https://astral.sh/uv/install.sh | sh",
           "windows": 'powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"'},
    "python": {"macos": "brew install python   (or let uv provide it: uv python install)",
               "linux": "sudo apt install python3   (or: uv python install)",
               "windows": "winget install Python.Python.3.12   (or: uv python install)"},
    "node": {"macos": "brew install node", "linux": "see https://nodejs.org/en/download (Node 22 LTS)",
             "windows": "winget install OpenJS.NodeJS.LTS"},
    "tectonic": {"macos": "brew install tectonic",
                 "linux": "curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net | sh   (then move ./tectonic onto your PATH)",
                 "windows": "see https://tectonic-typesetting.github.io/en-US/install.html"},
    "libreoffice": {"macos": "brew install --cask libreoffice", "linux": "sudo apt install libreoffice-writer",
                    "windows": "winget install TheDocumentFoundation.LibreOffice"},
}


def version(command: list[str]) -> str | None:
    try:
        out = subprocess.run(command, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return None
    text = (out.stdout or out.stderr).strip().splitlines()
    return text[0][:80] if text else ""


def chromium_browser() -> str | None:
    """Chrome or Edge, where the agent's browser extension runs."""
    if SYSTEM == "macos":
        for app in ("Google Chrome", "Microsoft Edge", "Chromium", "Brave Browser"):
            if Path(f"/Applications/{app}.app").exists() or (Path.home() / f"Applications/{app}.app").exists():
                return app
        return None
    if SYSTEM == "windows":
        roots = [os.environ.get(v, "") for v in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA")]
        for root in filter(None, roots):
            for rel, name in (("Google/Chrome/Application/chrome.exe", "Google Chrome"), ("Microsoft/Edge/Application/msedge.exe", "Microsoft Edge")):
                if Path(root, rel).exists():
                    return name
        return None
    for exe in ("google-chrome", "google-chrome-stable", "microsoft-edge", "microsoft-edge-stable", "chromium", "chromium-browser", "brave-browser"):
        if shutil.which(exe):
            return exe
    return None


def word_installed() -> bool:
    if SYSTEM == "macos":
        return Path("/Applications/Microsoft Word.app").exists()
    if SYSTEM == "windows":
        roots = [os.environ.get(v, "") for v in ("ProgramFiles", "ProgramFiles(x86)")]
        return any(list(Path(r, "Microsoft Office").rglob("WINWORD.EXE")) for r in roots if r and Path(r, "Microsoft Office").exists())
    return False


def humanizer_path() -> Path | None:
    """The humanizer skill, wherever an agent installs it: this folder, the user's skill folders,
    or Claude Code's plugin cache."""
    home, here = Path.home(), Path.cwd()
    claude = Path(os.environ.get("CLAUDE_CONFIG_DIR") or home / ".claude")
    candidates = [here / ".agents/skills/humanizer", here / ".claude/skills/humanizer", here / ".gemini/skills/humanizer",
                  here / ".opencode/skills/humanizer", here / ".cursor/skills/humanizer", here / ".github/skills/humanizer",
                  home / ".agents/skills/humanizer", claude / "skills/humanizer", home / ".gemini/skills/humanizer",
                  home / ".cursor/skills/humanizer", home / ".copilot/skills/humanizer", home / ".config/opencode/skills/humanizer"]
    for folder in candidates:
        if (folder / "SKILL.md").is_file():
            return folder / "SKILL.md"
    cache = claude / "plugins" / "cache"
    if cache.is_dir():
        for skill in cache.glob("*/humanizer/**/SKILL.md"):
            return skill
    return None


def gradbo_folder() -> tuple[bool, str]:
    here = Path.cwd()
    agents = here / "AGENTS.md"
    if agents.is_file() and "Gradbo" in agents.read_text(encoding="utf-8", errors="ignore"):
        return True, str(here)
    if (here / "profile" / "cv").is_dir() or (here / "profile" / "facts.md").is_file():
        return True, f"{here} (no AGENTS.md yet)"
    if any((here / d / "skills" / "gradbo" / "SKILL.md").is_file() for d in (".agents", ".claude", ".gemini", ".cursor", ".github", ".opencode")):
        return True, f"{here} (skills installed, no profile yet)"
    default = Path.home() / "Gradbo"
    # Agent configuration and version control don't make a folder "used".
    config = {".agents", ".claude", ".gemini", ".cursor", ".github", ".opencode", ".codex", ".vscode", ".git",
              ".mcp.json", "opencode.json", "skills-lock.json", ".DS_Store"}
    if here.name.lower() == "gradbo" or all(p.name in config for p in here.iterdir()):
        return True, f"{here} (new)"
    hint = f"{default} exists: restart the agent there" if default.is_dir() else f"create {default} and start the agent there"
    return False, f"{here} is not a Gradbo folder; {hint}"


def check(mail: bool) -> list[dict]:
    items = []

    def add(name, ok, need, detail, fix_key=None, fix=None):
        items.append({"name": name, "ok": ok, "need": need, "detail": detail,
                      "fix": None if ok else (fix or (FIX[fix_key][SYSTEM] if fix_key else None))})

    ok, where = gradbo_folder()
    add("Gradbo folder (start the agent here)", ok, "required", where, fix=None if ok else "see references/setup.md step 1")
    skill = humanizer_path()
    add("humanizer skill", bool(skill), "required", str(skill) if skill else "not found",
        fix="see references/install.md step 3 (Claude Code: claude plugin install humanizer@gradbo --scope project; "
            "others: npx skills add blader/humanizer -a <agent> -y)")
    py = sys.version_info
    add("Python 3.10+", py >= (3, 10), "recommended", f"{platform.python_version()} at {sys.executable}", "python")
    uv = shutil.which("uv")
    add("uv", bool(uv), "recommended", version([uv, "--version"]) if uv else "not found: docs.py then needs its packages installed by hand", "uv")
    if not uv:
        missing = [m for m in ("docx", "pypdfium2", "PIL") if __import__("importlib.util").util.find_spec(m) is None]
        add("docs.py packages", not missing, "recommended", "installed" if not missing else f"missing: {', '.join(missing)}",
            fix=f"{Path(sys.executable).name} -m pip install python-docx pypdfium2 pillow   (or install uv)")
    node = shutil.which("node")
    node_version = version([node, "--version"]) if node else None
    major = int(node_version.lstrip("v").split(".")[0]) if node_version and node_version.lstrip("v")[:1].isdigit() else 0
    add("Node 18+ (for `npx skills`, and the Playwright fallback browser)", major >= 18, "recommended",
        node_version or "not found", "node")
    browser = chromium_browser()
    add("Chrome or Edge (the agent applies in your own browser)", bool(browser), "recommended",
        browser or "not found", fix="install Google Chrome or Microsoft Edge, then your agent's browser extension (references/install.md step 4)")
    tectonic = shutil.which("tectonic")
    add("Tectonic (only for LaTeX CVs)", bool(tectonic), "optional", version([tectonic, "--version"]) if tectonic else "not found", "tectonic")
    office = shutil.which("soffice") or shutil.which("libreoffice")
    word = word_installed()
    add("LibreOffice or Word (to see Word CVs' pages)", bool(office or word), "optional",
        "LibreOffice" if office else "Microsoft Word" if word else "neither found; Word CVs are checked by text only", "libreoffice")
    user, password = os.environ.get("GRADBO_IMAP_USER"), os.environ.get("GRADBO_IMAP_PASSWORD")
    detail = "set" if user and password else "not set (fine if the agent has a mail connector, or you read codes out)"
    ok = bool(user and password)
    if ok and mail:
        import imaplib
        try:
            box = imaplib.IMAP4_SSL(os.environ.get("GRADBO_IMAP_HOST", "imap.gmail.com"))
            box.login(user, password)
            box.logout()
            detail = f"logged in as {user}"
        except Exception as exc:
            ok, detail = False, f"login failed: {exc.__class__.__name__}"
    add("IMAP mail access (GRADBO_IMAP_USER / GRADBO_IMAP_PASSWORD)", ok, "optional", detail,
        fix="Gmail: create an app password (Google Account > Security > App passwords) and set both variables in your shell profile")
    return items


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    items = check("--mail" in argv)
    if "--json" in argv:
        print(json.dumps({"system": SYSTEM, "checks": items}, indent=1))
        return 0
    print(f"System: {platform.system()} {platform.release()} ({SYSTEM})\n")
    for item in items:
        mark = "ok " if item["ok"] else {"optional": "-- ", "recommended": "!! "}.get(item["need"], "XX ")
        print(f"{mark} {item['name']}: {item['detail']}")
        if item["fix"]:
            print(f"      install: {item['fix']}")
    required = [i["name"] for i in items if not i["ok"] and i["need"] == "required"]
    missing = [i["name"] for i in items if not i["ok"] and i["need"] == "recommended"]
    if required:
        print(f"\nRequired and missing: {', '.join(required)}")
    print("\nReady." if not (required or missing) else f"Recommended but missing: {', '.join(missing)}" if missing else "")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
