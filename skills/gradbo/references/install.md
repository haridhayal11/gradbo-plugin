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
| Node 18+ | Playwright MCP, the usual browser tool | Install another browser tool, or the candidate submits forms themselves |
| Tectonic | LaTeX CVs only | Their compiled PDF is sent unchanged |
| LibreOffice or Word | Seeing Word CVs' pages | Word CVs are checked by text only |
| IMAP variables | Reading mail without a connector | Codes are read out by the candidate |

If Python itself is missing, `doctor.py` can't run. Ask the candidate to install uv (it brings Python), using the commands in step 2 of the plugin README or https://docs.astral.sh/uv/.

## 3. Humanizer skill (required)

Every piece of prose the skill writes goes through the `humanizer` skill ([blader/humanizer](https://github.com/blader/humanizer), MIT). Check that it is available: it's in your skill list, or `doctor.py` reports where it found its `SKILL.md`. If it is missing, install it into the Gradbo folder (ask first):

- **Claude Code:** it comes with the gradbo plugin as a dependency. If it is missing, run `claude plugin install humanizer@gradbo --scope project`.
- **Codex, Cursor, GitHub Copilot:** `npx skills add blader/humanizer -a <codex|cursor|github-copilot> -y`, run in the Gradbo folder.
- **OpenCode:** `npx skills add blader/humanizer -a opencode -g -y`.
- **Gemini CLI:** `gemini skills install https://github.com/blader/humanizer --scope workspace`.
- **Anything else:** copy the repository's `SKILL.md` into a `humanizer` folder in the agent's skills directory (`.agents/skills/humanizer/` works for most).

Then ask the candidate to restart the agent so it loads the skill. Until it is installed, prepare nothing an employer will read: no tailored CV, cover letter or written answer.

## 4. The candidate's browser (strongly recommended)

You apply in the candidate's own Chrome or Edge, with their logins, saved passwords and autofill, through Playwright MCP in extension mode. Check your tools for Playwright's (`browser_navigate`, `browser_snapshot` and the rest). Without a browser tool, applying stops at "here is everything, please submit it yourself".

To set it up (needs Node 18+ and Chrome or Edge), the candidate:

1. Installs the [Playwright Extension](https://chromewebstore.google.com/detail/playwright-extension/mmlmfjhmonkocbjadbfplnigmagldckm) in Chrome or Edge.
2. Adds Playwright MCP with `--extension` to this agent, using the snippet below, and restarts the agent:

- **Claude Code** (from the Gradbo folder): `claude mcp add --scope project playwright -- npx @playwright/mcp@latest --extension`
- **Codex** (`~/.codex/config.toml`):

  ```toml
  [mcp_servers.playwright]
  command = "npx"
  args = ["@playwright/mcp@latest", "--extension"]
  ```

- **Gemini CLI** (`~/.gemini/settings.json`) and **Cursor** (`~/.cursor/mcp.json`):

  ```json
  {"mcpServers": {"playwright": {"command": "npx", "args": ["@playwright/mcp@latest", "--extension"]}}}
  ```

- **VS Code with Copilot** (user `mcp.json`, via **MCP: Open User Configuration**):

  ```json
  {"servers": {"playwright": {"command": "npx", "args": ["@playwright/mcp@latest", "--extension"]}}}
  ```

- **OpenCode** (`~/.config/opencode/opencode.json`):

  ```json
  {"mcp": {"playwright": {"type": "local", "command": ["npx", "@playwright/mcp@latest", "--extension"], "enabled": true}}}
  ```

Merge the snippet into the existing file if it has other servers; don't replace it. If a `playwright` entry already exists without `--extension`, add the flag: a separate Playwright profile has none of the candidate's logins.

How it behaves:
- The first time you use the browser in a session, the browser shows a page where the candidate approves the connection and picks the tab. Tell them to expect it.
- You work only in the tabs of your own tab group. Leave their other tabs alone, and close the tabs you opened when you are done.
- Claude Code's Chrome integration (`claude --chrome`) and Cowork's browser also drive the candidate's own browser. If one of those is what this agent has, use it instead.

## 5. Mail (optional)

See [email.md](email.md), "Which mail access to use". Check your tools for a mail connector first (Gmail, Outlook, Microsoft 365). Without one, the IMAP route needs an app password; `doctor.py --mail` tests the login once the variables are set.

## Report

End with one checklist, required items first:

```
Gradbo connection    ok
Humanizer skill      ok
Browser tool         missing: add Playwright MCP (snippet above), then restart me
Documents (Python)   ok
LaTeX (Tectonic)     not needed: your CV is a Word file
Mail                 Gmail connector found
```

Then continue with setup. A missing optional item never blocks it.
