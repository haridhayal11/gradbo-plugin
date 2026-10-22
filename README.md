# Gradbo for your agent

Find UK early-careers roles with [Gradbo](https://gradbo.com) and apply with your own AI agent. Gradbo crawls employers' career pages and keeps your tracker. This repository gives your agent two things:

- **The `gradbo` skill** (`skills/gradbo/`) in the open [Agent Skills](https://agentskills.io) format. It keeps your profile, answers, application documents and receipts in a local workspace folder, tailors your CV (LaTeX or Word), fills in applications in the agent's browser, reads verification codes and replies from your email, and records each submission in Gradbo.
- **A connection to the Gradbo MCP server** at `https://app.gradbo.com/mcp/`, authenticated with your token.

Your CV, answers and email never pass through Gradbo.

## 1. Get a token

In the Gradbo dashboard, open **Settings › Connect your agent**, create a token with `read` and `write`, and add it to your shell profile (`~/.zshrc`, `~/.bashrc`, or Windows' user environment variables):

```sh
export GRADBO_TOKEN=jr_pat_...
```

## 2. Install the skill and the connection

### Claude Code

```sh
claude plugin marketplace add haridhayal11/gradbo-plugin
claude plugin install gradbo@gradbo
```

The plugin brings both the skill and the connection.

### Any other agent: the skill

```sh
npx skills add haridhayal11/gradbo-plugin
```

This needs Node 22.20 or later. [skills](https://github.com/vercel-labs/skills) detects your agents (Codex, Gemini CLI, Cursor, GitHub Copilot, OpenCode and many more) and copies `skills/gradbo` into each. To do it by hand instead, copy `skills/gradbo` into `~/.agents/skills/gradbo`, which Codex, Gemini CLI, Cursor, Copilot and OpenCode all read.

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

Gemini CLI documents `$VAR` expansion in settings but doesn't say it applies to headers. If the connection is refused, paste the token in place of `$GRADBO_TOKEN`. To install the skill without npx: `gemini skills install https://github.com/haridhayal11/gradbo-plugin --path skills/gradbo`.

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

## 3. What the skill needs on your machine

| For | Install | Without it |
|---|---|---|
| Applying | A browser tool in your agent, e.g. [Playwright MCP](https://github.com/microsoft/playwright-mcp) | The skill prepares everything and you submit the form yourself |
| Checking and tailoring documents | Python 3.10+, ideally with [uv](https://docs.astral.sh/uv/) (`scripts/docs.py` fetches its own packages under uv) | Your CV is sent unchanged |
| LaTeX CVs | [Tectonic](https://tectonic-typesetting.github.io) | Your compiled PDF is sent unchanged |
| Seeing Word CVs' pages | LibreOffice, or Word on Windows/macOS | Word CVs are checked by text only |
| Verification codes and replies | A mail connector in your agent, or an IMAP app password (Gmail) in `GRADBO_IMAP_USER` / `GRADBO_IMAP_PASSWORD` | You read codes out when asked |

## 4. Start

Open your agent in an empty folder for your job search and ask it to set up your Gradbo profile. It reads your CV, asks for what a CV can't say (right to work, sponsorship, start date), saves your search preferences, then finds and triages roles. Ask it to apply to the ones you like.

## Contents

- `skills/gradbo/SKILL.md`: the router and the rules every task follows.
- `skills/gradbo/references/`: setup, find, apply, questions, consents, documents, email, organise, folder layout, question keys, and the writing guide (`humanizer.md`, bundled from [humanizer](https://github.com/blader/humanizer) under its MIT licence).
- `skills/gradbo/templates/`: the files the skill writes (job, receipt, facts, handoff, cover letter).
- `skills/gradbo/scripts/`: `docs.py` (documents) and `mail.py` (read-only IMAP).
- `.claude-plugin/` and `.mcp.json`: the Claude Code plugin packaging.

This repository is published from `gradbo/agent` in the Gradbo source tree; changes are made there.
