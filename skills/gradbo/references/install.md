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

## 3. Browser tool (strongly recommended)

Check your own tools for something that opens pages, clicks, types and uploads files: a browser MCP server or a built-in browser. If there is none, applying stops at "here is everything, please submit it yourself". To add Playwright MCP (needs Node 18+), give the candidate the snippet for their agent, then ask them to restart it:

- **Claude Code:** `claude mcp add playwright -- npx @playwright/mcp@latest`
- **Codex** (`~/.codex/config.toml`):

  ```toml
  [mcp_servers.playwright]
  command = "npx"
  args = ["@playwright/mcp@latest"]
  ```

- **Gemini CLI** (`~/.gemini/settings.json`) and **Cursor** (`~/.cursor/mcp.json`):

  ```json
  {"mcpServers": {"playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}}}
  ```

- **VS Code with Copilot** (user `mcp.json`, via **MCP: Open User Configuration**):

  ```json
  {"servers": {"playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}}}
  ```

- **OpenCode** (`~/.config/opencode/opencode.json`):

  ```json
  {"mcp": {"playwright": {"type": "local", "command": ["npx", "@playwright/mcp@latest"], "enabled": true}}}
  ```

Merge the snippet into the existing file if it has other servers; don't replace it. Playwright MCP opens a visible browser by default, so the candidate can watch and take over for a CAPTCHA.

## 4. Mail (optional)

See [email.md](email.md), "Which mail access to use". Check your tools for a mail connector first (Gmail, Outlook, Microsoft 365). Without one, the IMAP route needs an app password; `doctor.py --mail` tests the login once the variables are set.

## Report

End with one checklist, required items first:

```
Gradbo connection    ok
Browser tool         missing: add Playwright MCP (snippet above), then restart me
Documents (Python)   ok
LaTeX (Tectonic)     not needed: your CV is a Word file
Mail                 Gmail connector found
```

Then continue with setup. A missing optional item never blocks it.
