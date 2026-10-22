# Gradbo plugin

Find UK early-careers roles with [Gradbo](https://gradbo.com) and apply with your own agent. Gradbo crawls employers' career pages and keeps your tracker; this plugin connects your agent to it and adds a skill that keeps your profile, answers, application documents and receipts in a local workspace folder. Your CV and answers never leave your machine.

## Install (Claude Code)

1. Create a token with `read` and `write` in the Gradbo dashboard under **Settings › Connect your agent**, and export it in your shell profile:

   ```sh
   export GRADBO_TOKEN=jr_pat_...
   ```

2. Add the marketplace and install the plugin:

   ```sh
   claude plugin marketplace add haridhayal11/gradbo-plugin
   claude plugin install gradbo@gradbo
   ```

3. Start Claude Code in the folder you want as your job-search workspace and ask it to set up your profile.

The connection goes to `https://app.gradbo.com/mcp/`. Set `GRADBO_URL` to use another Gradbo server.

## What's inside

- `.mcp.json`: the Gradbo MCP server (jobs, tracker, preferences, `record_submission`).
- `skills/gradbo/`: the skill. `SKILL.md` routes to setup, finding roles, applying and organising; `references/` holds the rules (facts, consents, documents, question keys) and `templates/` the files it writes.

Applying needs a browser tool in your agent, such as Playwright MCP. Tailored CVs and cover letters need [Tectonic](https://tectonic-typesetting.github.io) and Poppler (`pdftotext`, `pdftoppm`, `pdfinfo`).

This repository is published from `gradbo/agent` in the Gradbo source tree; changes are made there.
