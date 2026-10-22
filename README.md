# Gradbo for your agent

Find UK early-careers roles with [Gradbo](https://gradbo.com) and apply with your own AI agent. Gradbo crawls employers' career pages and keeps your tracker. This repository gives your agent two things:

- **One folder for everything.** Your CV, facts, answers and every application live in a single Gradbo folder (`~/Gradbo`), together with the skills. You always start your agent there.
- **The `gradbo` skill** (`skills/gradbo/`) in the open [Agent Skills](https://agentskills.io) format. It keeps your profile, answers, application documents and receipts in a local workspace folder, tailors your CV (LaTeX or Word), fills in applications in the agent's browser, reads verification codes and replies from your email, and records each submission in Gradbo.
- **A connection to the Gradbo MCP server** at `https://app.gradbo.com/mcp/`, authenticated with your token.
- **The [humanizer](https://github.com/blader/humanizer) skill** (MIT), which is required: everything written for an employer goes through it so it doesn't read as AI-written.

Your CV, answers and email never pass through Gradbo.

## Quick start

1. Sign up at [app.gradbo.com](https://app.gradbo.com). New accounts are approved by an administrator; you can get your agent ready while you wait.
2. Once approved, the dashboard's **Connect your agent** step (also under **Settings**) asks which agent you use, creates your token, and shows the exact commands with the token filled in: make the Gradbo folder, install the skills and the connection into it, and add a browser. It tells you when your agent has connected.
3. Start your agent in the Gradbo folder and say: **"Set up my Gradbo profile. My CV is at <path>."** It first checks your computer and lists anything missing, with install commands for your system, then copies your CV into the folder and reads it.

The rest of this page is the same setup by hand.

## 1. Get a token

In the dashboard, open **Settings › Connect your agent** and create a token with `read` and `write`. Claude Code stores it for you (below). For other agents, keep it in your shell profile (`~/.zshrc` or `~/.bashrc`; on Windows, `setx GRADBO_TOKEN <token>`):

```sh
export GRADBO_TOKEN=jr_pat_...
```

## 2. Make the Gradbo folder

```sh
mkdir -p ~/Gradbo && cd ~/Gradbo                  # Windows PowerShell: mkdir $HOME\Gradbo -Force; cd $HOME\Gradbo
```

Run the install commands below inside it, and always start your agent there.

## 3. Install the skills and the connection

### Claude Code

```sh
claude plugin marketplace add haridhayal11/gradbo-plugin
claude plugin install gradbo@gradbo --scope project --config token=<your token>
claude mcp add --scope project playwright -- npx @playwright/mcp@latest
```

The plugin brings the Gradbo skill and the connection, and installs the humanizer plugin as a dependency. `--scope project` records all of it in the folder's `.claude/settings.json`, and Claude Code keeps the token in its credential store. To change the token later, run `claude plugin configure gradbo@gradbo`. For your own Gradbo server, add `--config server=https://your.server`. The last line adds the browser the skill applies with.

### Any other agent: the skills

In the Gradbo folder:

```sh
npx skills add haridhayal11/gradbo-plugin
npx skills add blader/humanizer
```

This needs Node 22.20 or later. Tested with Codex; OpenCode 1.19.3 connected to Gradbo but didn't list skills from a project's `.agents/skills`, so install both skills globally there (add `-g`). [skills](https://github.com/vercel-labs/skills) detects your agents (Codex, Gemini CLI, Cursor, GitHub Copilot, OpenCode and many more) and copies `skills/gradbo` into each. Without `-g`, the skills go into the folder's `.agents/skills/`, which Codex, Cursor and Copilot read when started there. To do it by hand, copy `skills/gradbo` and the humanizer's `SKILL.md` into `.agents/skills/gradbo/` and `.agents/skills/humanizer/`. Gemini CLI: `gemini skills install https://github.com/haridhayal11/gradbo-plugin --path skills/gradbo --scope workspace`, and the same for `https://github.com/blader/humanizer`.

### Any other agent: the connection

Add the server to your agent's MCP settings.

**Codex** (`~/.codex/config.toml`):

```toml
[mcp_servers.gradbo]
url = "https://app.gradbo.com/mcp/"
bearer_token_env_var = "GRADBO_TOKEN"
```

**Gemini CLI** (`~/.gemini/settings.json`; `httpUrl`, not `url`):

```json
{"mcpServers": {"gradbo": {"httpUrl": "https://app.gradbo.com/mcp/", "headers": {"Authorization": "Bearer $GRADBO_TOKEN"}}}}
```

Gemini CLI documents `$VAR` expansion in settings but doesn't say it applies to headers. If the connection is refused, paste the token in place of `$GRADBO_TOKEN`. 

**Cursor** (`~/.cursor/mcp.json`):

```json
{"mcpServers": {"gradbo": {"url": "https://app.gradbo.com/mcp/", "headers": {"Authorization": "Bearer ${env:GRADBO_TOKEN}"}}}}
```

**GitHub Copilot in VS Code** (`.vscode/mcp.json`, or the user `mcp.json` via **MCP: Open User Configuration**). VS Code asks for the token once and stores it securely:

```json
{
  "inputs": [{"type": "promptString", "id": "gradbo-token", "description": "Gradbo token", "password": true}],
  "servers": {"gradbo": {"type": "http", "url": "https://app.gradbo.com/mcp/", "headers": {"Authorization": "Bearer ${input:gradbo-token}"}}}
}
```

**GitHub Copilot CLI:** `copilot mcp add gradbo --transport http --header "Authorization: Bearer <token>" https://app.gradbo.com/mcp/`. Its config doesn't document environment variables, so the token is stored in `~/.copilot/mcp-config.json`.

**OpenCode** (`~/.config/opencode/opencode.json`):

```json
{"$schema": "https://opencode.ai/config.json", "mcp": {"gradbo": {"type": "remote", "url": "https://app.gradbo.com/mcp/", "headers": {"Authorization": "Bearer {env:GRADBO_TOKEN}"}}}}
```

**Anything else:** the server speaks streamable HTTP at `https://app.gradbo.com/mcp/` and wants `Authorization: Bearer <token>`.

## 4. What the skill needs on your machine

The skill checks all of this itself at the start of setup (`scripts/doctor.py`, which needs only Python) and tells you what's missing, with the install command for your system.

| For | Install | Without it |
|---|---|---|
| Applying | A browser tool in your agent, e.g. [Playwright MCP](https://github.com/microsoft/playwright-mcp) | The skill prepares everything and you submit the form yourself |
| Checking and tailoring documents | Python 3.10+, ideally with [uv](https://docs.astral.sh/uv/) (`scripts/docs.py` fetches its own packages under uv) | Your CV is sent unchanged |
| LaTeX CVs | [Tectonic](https://tectonic-typesetting.github.io) | Your compiled PDF is sent unchanged |
| Seeing Word CVs' pages | LibreOffice, or Word on Windows/macOS | Word CVs are checked by text only |
| Verification codes and replies | A mail connector in your agent, or an IMAP app password (Gmail) in `GRADBO_IMAP_USER` / `GRADBO_IMAP_PASSWORD` | You read codes out when asked |

## 5. Start

Open your agent in the Gradbo folder and ask it to set up your Gradbo profile. It reads your CV, asks for what a CV can't say (right to work, sponsorship, start date), saves your search preferences, then finds and triages roles. Ask it to apply to the ones you like.

## Contents

- `skills/gradbo/SKILL.md`: the router and the rules every task follows.
- `skills/gradbo/references/`: install (preflight), setup, find, apply, questions, consents, documents, email, organise, folder layout and question keys.
- `skills/gradbo/templates/`: the files the skill writes (the folder's AGENTS.md, job, receipt, facts, handoff, cover letter).
- `skills/gradbo/scripts/`: `doctor.py` (checks your computer), `docs.py` (documents) and `mail.py` (read-only IMAP).
- `.claude-plugin/` and `.mcp.json`: the Claude Code plugin packaging. The marketplace also lists the humanizer, which the gradbo plugin depends on.

This repository is published from `gradbo/agent` in the Gradbo source tree; changes are made there.
