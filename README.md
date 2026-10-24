# Gradbo plugin

Find UK early-careers roles with [Gradbo](https://gradbo.com) and apply with your own agent. Supported agents: Claude Code, Codex and Gemini CLI.

Gradbo remembers what you tell your agent (your facts, answers and applications, encrypted), so it never asks you the same thing twice, on any agent or computer. Your CV and documents stay in your Gradbo folder. **Settings › Your data** in the dashboard downloads or deletes what Gradbo keeps.

The **Connect your agent** step in the Gradbo dashboard shows these same steps with your token filled in, and tells you when your agent has connected.

## 1. Get a token

Sign up at [app.gradbo.com](https://app.gradbo.com). Once your account is approved, open **Settings › Connect your agent** and create a token with `read` and `write`.

## 2. Make your Gradbo folder

```sh
mkdir -p ~/Gradbo && cd ~/Gradbo
```

On Windows (PowerShell): `mkdir $HOME\Gradbo -Force; cd $HOME\Gradbo`. Run the rest inside this folder, and always start your agent here.

## 3. Install

### Claude Code

```sh
claude plugin marketplace add haridhayal11/gradbo-plugin
claude plugin install gradbo@gradbo --scope project --config token=<your token>
```

Then install [Claude in Chrome](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) in Chrome or Edge, and start Claude Code with:

```sh
claude --chrome
```

### Codex

```sh
npx skills add haridhayal11/gradbo-plugin -a codex -y
npx skills add blader/humanizer -a codex -y
```

Add your token to your shell profile (`~/.zshrc` or `~/.bashrc`; on Windows, `setx GRADBO_TOKEN <your token>`):

```sh
export GRADBO_TOKEN=<your token>
```

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.gradbo]
url = "https://app.gradbo.com/mcp/"
bearer_token_env_var = "GRADBO_TOKEN"
```

For the browser, use one of these:

- **ChatGPT desktop app:** go to Settings › Computer Use, choose your browser and install the ChatGPT extension. For CV uploads in Chrome, turn on "Allow access to file URLs" on the extension's Details page.
- **Codex CLI:** install the [Playwright Extension](https://chromewebstore.google.com/detail/playwright-extension/mmlmfjhmonkocbjadbfplnigmagldckm) in Chrome or Edge, and add to `~/.codex/config.toml`:

  ```toml
  [mcp_servers.playwright]
  command = "npx"
  args = ["@playwright/mcp@latest", "--extension"]
  ```

### Gemini CLI

```sh
gemini skills install https://github.com/haridhayal11/gradbo-plugin --path skills/gradbo --scope workspace
gemini skills install https://github.com/blader/humanizer --scope workspace
```

Merge into `~/.gemini/settings.json`. Keep this file private, because it holds your token:

```json
{
  "mcpServers": {"gradbo": {"httpUrl": "https://app.gradbo.com/mcp/", "headers": {"Authorization": "Bearer <your token>"}}},
  "agents": {"overrides": {"browser_agent": {"enabled": true}}, "browser": {"sessionMode": "existing"}}
}
```

In Chrome (144 or later), open `chrome://inspect/#remote-debugging` and turn on remote debugging.

## 4. Start

Start your agent in `~/Gradbo` and say:

> Set up my Gradbo profile. My CV is at <path to your CV>.

It checks your computer first, lists anything missing with the install command for your system, then reads your CV.
