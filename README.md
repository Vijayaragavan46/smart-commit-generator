# Smart Commit Generator

A lightweight CLI tool that analyzes your Git changes and uses **Claude AI or Ollama (local/free)** to generate clear, meaningful, and standardized commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) specification.

No more vague commits like `"fix stuff"` or `"update files"` — get professional commit messages automatically.

---

## Example Output

```
------------------------------------------------------------
feat(auth): replace hardcoded credentials with environment variables

Hardcoded admin credentials posed a security risk and would fail
in production. Auth now reads from ADMIN_USER and ADMIN_PASS
environment variables.
------------------------------------------------------------
```

---

## Commit Types Generated

| Type       | When Used                                      |
|------------|------------------------------------------------|
| `feat`     | A new feature                                  |
| `fix`      | A bug fix                                      |
| `refactor` | Code change with no feature or bug impact      |
| `docs`     | Documentation changes only                     |
| `style`    | Formatting, spacing (no logic change)          |
| `test`     | Adding or fixing tests                         |
| `chore`    | Build process, dependencies, tooling           |
| `perf`     | Performance improvement                        |
| `ci`       | CI/CD configuration changes                    |
| `revert`   | Reverting a previous commit                    |

---

## Providers

| Provider | Cost | Requires | Quality | Speed |
|---|---|---|---|---|
| **Claude AI** (default) | Pay per use | Anthropic API key | Best | Fast |
| **Ollama** (local) | Free forever | Ollama installed | Good | 30-60s (CPU) |
| **Ollama** (remote server) | Server cost | Ollama on server | Good | Fast |

---

## Requirements

- Python 3.10 or higher
- Git installed
- **Claude:** Anthropic API key → [console.anthropic.com](https://console.anthropic.com)
- **Ollama:** Ollama installed → [ollama.com](https://ollama.com)

---

## Installation

### Step 1 — Install the package

```bash
pip install smart-commit-generator
```

### Step 2 — Set up your provider

#### Option A — Claude AI (best quality)
Get your API key from [console.anthropic.com](https://console.anthropic.com) and set it as an environment variable (see [Setting the API Key](#setting-the-api-key)).

#### Option B — Ollama (free, local, no API key)
Install Ollama and pull a model:
```bash
# Install Ollama from https://ollama.com/download
ollama pull gemma3
```

---

## Setting the API Key (Claude only)

### Windows

#### Temporary (current session only)

**CMD:**
```cmd
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**PowerShell:**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

#### Permanent (recommended)

1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Go to **Advanced** tab → click **Environment Variables**
3. Under **User variables**, click **New**
4. Set:
   - Variable name: `ANTHROPIC_API_KEY`
   - Variable value: `sk-ant-your-key-here`
5. Click **OK** → restart your terminal

---

### macOS / Linux

#### Temporary

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

#### Permanent

**zsh (default on macOS):**
```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**bash:**
```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

---

## Usage

### Claude AI (default)

```bash
# Stage your files
git add .

# Generate commit message
smart-commit

# Generate and commit immediately
smart-commit --apply
```

### Ollama — Local (free, no API key)

```bash
# Install Ollama + pull model (one time)
ollama pull gemma3

# Stage your files
git add .

# Generate commit message using local Ollama
smart-commit --provider ollama

# Use a specific model
smart-commit --provider ollama --model gemma3:12b

# Generate and commit immediately
smart-commit --provider ollama --apply
```

### Ollama — Remote Server (shared team server)

```bash
# Point to your team's server
smart-commit --provider ollama --host http://YOUR_SERVER_IP:11434

# Set permanently so you never have to type --host
```

**Windows (permanent):**
```cmd
setx SMART_COMMIT_OLLAMA_HOST "http://YOUR_SERVER_IP:11434"
setx SMART_COMMIT_PROVIDER "ollama"
```

**macOS/Linux (permanent):**
```bash
echo 'export SMART_COMMIT_OLLAMA_HOST="http://YOUR_SERVER_IP:11434"' >> ~/.zshrc
echo 'export SMART_COMMIT_PROVIDER="ollama"' >> ~/.zshrc
source ~/.zshrc
```

Then just run:
```bash
smart-commit
```

---

## All Options

```
smart-commit [options]

Options:
  --all, -a         Analyze all changes (staged + unstaged)
  --apply           Commit immediately with the generated message
  --copy, -c        Copy the generated message to clipboard
  --provider, -p    AI provider: claude (default) or ollama
  --model, -m       Model to use:
                      Claude:  claude-opus-4-6 (default)
                               claude-sonnet-4-6
                               claude-haiku-4-5
                      Ollama:  gemma3 (default)
                               gemma3:12b
                               llama3
                               mistral
                               codellama
  --host            Ollama server URL (default: http://localhost:11434)
  --no-context      Skip reading recent commits for style matching
  -h, --help        Show help message
```

---

## Step-by-Step Workflow

### Scenario 1 — Quick commit with Claude

```bash
git add .
smart-commit --apply
```

### Scenario 2 — Free local commit with Ollama

```bash
git add .
smart-commit --provider ollama --apply
```

### Scenario 3 — Preview before committing

```bash
git add .
smart-commit --provider ollama   # preview
smart-commit --provider ollama --apply  # commit if happy
```

### Scenario 4 — Analyze all changes without staging

```bash
smart-commit --all
# or
smart-commit --provider ollama --all
```

### Scenario 5 — Generate, copy, paste manually

```bash
git add .
smart-commit --copy
git commit   # paste from clipboard
```

---

## How It Works

1. Runs `git diff --cached` (or `git diff` with `--all`) to capture your changes
2. Runs `git status` to see which files changed
3. Reads your last 5 commits to match your repo's style
4. Sends everything to Claude or Ollama with a structured prompt
5. Returns a conventional commit message
6. Displays it — optionally applies or copies it

---

## Models Comparison

### Claude Models

| Model                  | Speed    | Cost     | Best For                        |
|------------------------|----------|----------|---------------------------------|
| `claude-opus-4-6`      | Moderate | Higher   | Complex changes, best quality   |
| `claude-sonnet-4-6`    | Fast     | Medium   | Most everyday commits           |
| `claude-haiku-4-5`     | Fastest  | Lowest   | Simple changes, high volume     |

### Ollama Models

| Model          | Size   | RAM Needed | Best For              |
|----------------|--------|------------|-----------------------|
| `gemma3`       | 3.3 GB | 8 GB       | General use (default) |
| `gemma3:12b`   | 7.8 GB | 16 GB      | Better quality        |
| `codellama`    | 3.8 GB | 8 GB       | Code-heavy changes    |
| `llama3`       | 4.7 GB | 8 GB       | General use           |
| `mistral`      | 4.1 GB | 8 GB       | General use           |

---

## Team Setup with Shared Ollama Server

Run Ollama on a shared server (e.g. DigitalOcean) so your whole team can use it for free.

### Server Requirements

| Spec | Value |
|---|---|
| OS | Ubuntu 22.04 LTS |
| RAM | 16 GB |
| vCPUs | 4 |
| Storage | 320 GB SSD |

### Server Setup

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull the model
ollama pull gemma3

# Start Ollama accessible to your team
OLLAMA_HOST=0.0.0.0 ollama serve
```

### Each Team Member

```bash
# Install smart-commit
pip install smart-commit-generator

# Set the shared server (add to shell profile)
export SMART_COMMIT_PROVIDER=ollama
export SMART_COMMIT_OLLAMA_HOST=http://YOUR_SERVER_IP:11434

# Use it
smart-commit
```

---

## Troubleshooting

### `smart-commit: command not found`

```bash
pip install smart-commit-generator
```

On macOS if not found after install:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

### `ANTHROPIC_API_KEY environment variable not set`

Set your API key — see [Setting the API Key](#setting-the-api-key) above.

---

### `Cannot connect to Ollama`

Make sure Ollama is running:
```bash
ollama serve
```

Or check if it's already running:
```bash
# Windows
tasklist | findstr ollama

# macOS/Linux
ps aux | grep ollama
```

---

### `No staged changes`

Stage your files first:
```bash
git add .
smart-commit
```

Or use `--all` to analyze without staging:
```bash
smart-commit --all
```

---

### Ollama is slow

- Use a smaller model: `smart-commit --provider ollama --model gemma3` (3.3GB, fastest)
- Use a remote GPU server for sub-5-second responses
- Claude API is faster than local CPU Ollama

---

### Clipboard not working on Linux

```bash
sudo apt install xclip      # Ubuntu/Debian
sudo dnf install xclip      # Fedora
```

---

## Project Structure

```
smart-commit-generator/
├── smart_commit.py     ← Main CLI script
├── setup.py            ← Package config & entry point
├── requirements.txt    ← Dependencies (anthropic)
├── .github/
│   └── workflows/
│       └── python-publish.yml  ← Auto-publish to PyPI on release
└── README.md           ← This file
```

---

## Changelog

### v1.1.0
- Added Ollama provider support (free, local, no API key needed)
- Live spinner with elapsed timer for Ollama responses
- `--provider` flag to switch between Claude and Ollama
- `--host` flag for remote Ollama servers (team sharing)
- `SMART_COMMIT_PROVIDER` and `SMART_COMMIT_OLLAMA_HOST` env vars

### v1.0.0
- Initial release
- Claude AI powered commit message generation
- Conventional Commits format
- `--apply`, `--copy`, `--all`, `--model` flags
- Windows and macOS support

---

## License

MIT — free to use, modify, and distribute.
