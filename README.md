# Smart Commit Generator

A lightweight CLI tool that analyzes your Git changes and uses **Claude AI** to generate clear, meaningful, and standardized commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) specification.

No more vague commits like `"fix stuff"` or `"update files"` — get professional commit messages automatically.

---

## Example Output

```
────────────────────────────────────────────────────────────
fix(auth): replace hardcoded credentials with environment variables

Hardcoded admin credentials posed a security risk and would fail
in production. Auth now reads from ADMIN_USER and ADMIN_PASS
environment variables.
────────────────────────────────────────────────────────────
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

## Requirements

- Python 3.10 or higher
- Git installed
- An Anthropic API key → [console.anthropic.com](https://console.anthropic.com)

---

## Installation

### Step 1 — Clone or download the project

```bash
# Clone
git clone https://github.com/your-username/smart-commit-generator.git
cd smart-commit-generator

# Or just download and navigate into the folder
cd path/to/smart-commit-generator
```

### Step 2 — Install dependencies and register the CLI

```bash
pip install -e .
```

This installs the `smart-commit` command globally so you can run it from any folder.

### Step 3 — Set your Anthropic API key

Get your key from [console.anthropic.com](https://console.anthropic.com) → API Keys → Create Key.

---

## Setting the API Key

### Windows

#### Option A — Temporary (current terminal session only)

**CMD:**
```cmd
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**PowerShell:**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

#### Option B — Permanent (recommended)

1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Go to **Advanced** tab → click **Environment Variables**
3. Under **User variables**, click **New**
4. Set:
   - Variable name: `ANTHROPIC_API_KEY`
   - Variable value: `sk-ant-your-key-here`
5. Click **OK** on all dialogs
6. **Restart your terminal** — it now works in CMD, PowerShell, VS Code, Git Bash, etc.

---

### macOS / Linux

#### Option A — Temporary (current terminal session only)

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

#### Option B — Permanent (recommended)

Add the export line to your shell profile file:

**For zsh (default on macOS):**
```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**For bash:**
```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

Verify it's set:
```bash
echo $ANTHROPIC_API_KEY
```

---

## Usage

Navigate to any Git repository and run:

### Basic — Analyze staged changes

```bash
# 1. Stage your files
git add .

# 2. Generate commit message
smart-commit
```

### Auto-commit — Generate and commit in one step

```bash
git add .
smart-commit --apply
```

### Analyze all changes (no need to stage first)

```bash
smart-commit --all
```

### Copy message to clipboard

```bash
smart-commit --copy
```

### Use a different Claude model

```bash
# Faster and cheaper
smart-commit --model claude-sonnet-4-6

# Fastest and most cost-effective
smart-commit --model claude-haiku-4-5

# Most powerful (default)
smart-commit --model claude-opus-4-6
```

### Skip recent commit history context

```bash
smart-commit --no-context
```

---

## All Options

```
smart-commit [options]

Options:
  --all, -a         Analyze all changes (staged + unstaged)
  --apply           Commit immediately with the generated message
  --copy, -c        Copy the generated message to clipboard
  --model, -m       Claude model to use:
                      claude-opus-4-6     (default, most powerful)
                      claude-sonnet-4-6   (faster, cheaper)
                      claude-haiku-4-5    (fastest, most cost-effective)
  --no-context      Skip reading recent commits for style matching
  -h, --help        Show help message
```

---

## Step-by-Step Workflow

### Scenario 1 — You made changes and want to commit

```bash
# Step 1: Check what changed
git status

# Step 2: Stage everything (or specific files)
git add .
# git add src/auth.py    ← stage a specific file

# Step 3: Preview the generated commit message
smart-commit

# Step 4: If happy with it, commit
smart-commit --apply
```

### Scenario 2 — Quick commit without previewing

```bash
git add .
smart-commit --apply
```

### Scenario 3 — Generate message without staging first

```bash
smart-commit --all
# Preview only — does NOT commit automatically
```

### Scenario 4 — Generate, copy, then paste manually

```bash
git add .
smart-commit --copy
git commit    # opens editor with your clipboard content
```

---

## How It Works

1. Runs `git diff --cached` (or `git diff` with `--all`) to get your changes
2. Runs `git status` to see which files are affected
3. Reads your last 5 commit messages to match your repo's style
4. Sends everything to Claude AI with a structured prompt
5. Claude returns a conventional commit message
6. The message is displayed — and optionally applied or copied

---

## Models Comparison

| Model                  | Speed    | Cost     | Best For                        |
|------------------------|----------|----------|---------------------------------|
| `claude-opus-4-6`      | Moderate | Higher   | Complex changes, best quality   |
| `claude-sonnet-4-6`    | Fast     | Medium   | Most everyday commits           |
| `claude-haiku-4-5`     | Fastest  | Lowest   | Simple changes, high volume     |

---

## Troubleshooting

### `smart-commit: command not found`

Re-install the package:
```bash
cd path/to/smart-commit-generator
pip install -e .
```

On macOS, if pip installs to a path not on your `$PATH`:
```bash
pip install -e . --user
# Then add to PATH:
export PATH="$HOME/.local/bin:$PATH"
```

---

### `ANTHROPIC_API_KEY environment variable not set`

The key isn't set in your current terminal session.

**Windows CMD:**
```cmd
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Windows PowerShell:**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

**macOS/Linux:**
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

For a permanent fix, see the [Setting the API Key](#setting-the-api-key) section above.

---

### `No staged changes`

You need to stage files before running `smart-commit`:
```bash
git add .
smart-commit
```

Or analyze unstaged changes directly:
```bash
smart-commit --all
```

---

### `Not inside a git repository`

Make sure you're inside a git project folder:
```bash
cd path/to/your/project
git status    # should show repo status, not an error
smart-commit
```

---

### Clipboard not working on macOS/Linux

- **macOS:** Should work out of the box (uses `pbcopy`)
- **Linux:** Install `xclip`:
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
└── README.md           ← This file
```

---

## License

MIT — free to use, modify, and distribute.
