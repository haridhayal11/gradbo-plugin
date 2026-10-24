# Preflight: make sure everything works

Run this at the start of setup, and whenever something the skill needs seems to be missing. Report one short checklist to the candidate, fix what you can with their agreement, and tell them exactly what to do for the rest. Installing software changes their machine, so ask before you run any install command.

## 1. Gradbo connection (required)

Call `get_preferences()`.

- **It works:** the connection is fine.
- **The gradbo tools don't exist:** the connection isn't installed in this agent. Point the candidate to "Connect your agent" in the Gradbo dashboard (Settings), which shows the exact steps for their agent. Nothing else in the skill works until it's done, so stop here.
- **401 or "invalid token":** the token is wrong, revoked, or read-only. They create a new one with read and write in the dashboard, then:
  - **Claude Code:** `claude plugin configure gradbo@gradbo` (or `/plugin configure gradbo@gradbo` inside Claude Code), paste the token, and restart.
  - **Other agents:** update `GRADBO_TOKEN` (or the token in the agent's MCP settings) and restart.
- **"A write-scoped token is required"** on a write: the token is read-only; same fix.

## 2. This machine

Run `python <skill>/scripts/doctor.py` (`py` on Windows if `python` isn't found). It needs nothing but Python and prints what is installed, what is missing, and the install command for this OS.

| Item | Needed for | Without it |
|---|---|---|
| Python 3.10+ and uv | `docs.py` (checking and tailoring documents) | The candidate's CV is sent unchanged |
| Node 18+ | The Playwright fallback browser, and `npx skills` | Only needed if the agent has no browser of its own |
| Tectonic | LaTeX CVs only | Their compiled PDF is sent unchanged |
| LibreOffice or Word | Seeing Word CVs' pages | Word CVs are checked by text only |
| Inbox connected in Gradbo, or a mail connector | Verification codes, confirmation links and replies | Codes are read out by the candidate |

If Python itself is missing, `doctor.py` can't run. Ask the candidate to install uv (it brings Python) from https://docs.astral.sh/uv/ (one command on each system there).

## 3. Humanizer skill (required)

Every piece of prose the skill writes goes through the `humanizer` skill ([blader/humanizer](https://github.com/blader/humanizer), MIT). Check that it is available: it's in your skill list, or `doctor.py` reports where it found its `SKILL.md`. If it is missing, install it into the Gradbo folder (ask first):

- **Claude Code:** it comes with the gradbo plugin as a dependency. If it is missing, run `claude plugin install humanizer@gradbo --scope project`.
- **Codex:** `npx skills add blader/humanizer -a codex -y`, run in the Gradbo folder.
- **Gemini CLI:** `gemini skills install https://github.com/blader/humanizer --scope workspace`.

Then ask the candidate to restart the agent so it loads the skill. Until it is installed, prepare nothing an employer will read: no tailored CV, cover letter or written answer.

## 4. The candidate's browser (strongly recommended)

Apply with this agent's own browser tools, in the candidate's own browser wherever the agent supports it, so their logins and saved passwords are there. Check your tools for one that can open pages, read them, click, type and attach files. Without any, applying stops at "here is everything, please submit it yourself".

| Agent | Built-in browser | Set up |
|---|---|---|
| Claude Code | Chrome integration: the candidate's own Chrome or Edge; uploads up to 10 MB | Install the [Claude in Chrome](https://claude.ai/chrome) extension, then start Claude Code with `claude --chrome`, or run `/chrome` and choose "Enabled by default". Needs a Claude Pro, Max, Team or Enterprise login. |
| Claude desktop / Cowork | Built-in browser, or Claude in Chrome for the candidate's own Chrome | Settings › Cowork › Preferred browser; connect Claude in Chrome for their logins |
| Codex in the ChatGPT desktop app | ChatGPT browser extension: the candidate's own browser | Settings › Computer Use: choose the browser and install the extension. For uploads (Chrome only), turn on "Allow access to file URLs" on the extension's Details page |
| Gemini CLI | `browser_agent`, attached to the candidate's running Chrome (144+) | In `~/.gemini/settings.json`, enable `agents.overrides.browser_agent.enabled` and set `agents.browser.sessionMode` to `"existing"`; in Chrome, turn on remote debugging at `chrome://inspect/#remote-debugging` |
| Codex CLI | None | Use the fallback below |

**Fallback for the Codex CLI: Playwright in the candidate's own browser.**
1. Install the [Playwright Extension](https://chromewebstore.google.com/detail/playwright-extension/mmlmfjhmonkocbjadbfplnigmagldckm) in Chrome or Edge.
2. Add this to `~/.codex/config.toml` (needs Node 18+), then restart Codex:

   ```toml
   [mcp_servers.playwright]
   command = "npx"
   args = ["@playwright/mcp@latest", "--extension"]
   ```

   The browser asks the candidate to allow the connection the first time in each session.

**However it is set up:**
- Work in the tabs you open, and leave the candidate's other tabs alone.
- Expect the browser's own permission prompts (allowing a site, sharing a tab, approving the connection), and tell the candidate when one is coming.
- If an upload fails, the candidate picks the file themselves ([apply.md](apply.md)).

## 5. Mail (optional)

See [email.md](email.md), "Which mail access to use". `mail_status()` first: when the candidate has connected their inbox in Gradbo, mail works from any agent. Otherwise check your tools for a mail connector (Gmail, Outlook, Microsoft 365), and suggest connecting the inbox in Settings > Your data. The IMAP script needs an app password in the environment; `doctor.py --mail` tests that login.

## Report

End with one checklist, required items first:

```
Gradbo connection    ok
Humanizer skill      ok
Browser              missing: install Claude in Chrome and start me with `claude --chrome`
Documents (Python)   ok
LaTeX (Tectonic)     not needed: your CV is a Word file
Mail                 inbox connected in Gradbo
```

Then continue with setup. A missing optional item never blocks it.
