#!/usr/bin/env python3
"""
Smart Commit Message Generator
Analyzes git changes and generates conventional commit messages using Claude AI or Ollama.
"""

import subprocess
import sys
import os
import argparse
import json
import urllib.request
import urllib.error


SYSTEM_PROMPT = """You are an expert at writing conventional Git commit messages.
Analyze the provided git diff and generate a clear, concise commit message.

Follow the Conventional Commits specification:
  <type>(<scope>): <short description>

  [optional body]

Types:
  feat     - A new feature
  fix      - A bug fix
  refactor - Code change that neither fixes a bug nor adds a feature
  docs     - Documentation only changes
  style    - Formatting, missing semicolons, etc (no logic change)
  test     - Adding or correcting tests
  chore    - Build process, dependencies, tooling
  perf     - Performance improvement
  ci       - CI/CD configuration changes
  revert   - Reverts a previous commit

Rules:
- Subject line: max 72 characters, imperative mood ("add" not "added")
- Scope is optional but helpful (e.g., feat(auth): ...)
- Body: explain WHAT changed and WHY, not HOW (wrap at 72 chars)
- Only include body if the change needs explanation beyond the subject line
- Output ONLY the commit message, nothing else — no markdown, no explanation
"""

DEFAULT_OLLAMA_HOST = "http://localhost:11434"


def run_git_command(args: list[str]) -> tuple[str, int]:
    """Run a git command and return (output, exit_code)."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout.strip(), result.returncode


def get_git_diff(staged_only: bool = True) -> str:
    """Get the git diff for staged or all changes."""
    if staged_only:
        diff, code = run_git_command(["diff", "--cached"])
        if code != 0:
            print("Error: Not a git repository or no staged changes.")
            sys.exit(1)
        return diff
    else:
        diff, _ = run_git_command(["diff", "HEAD"])
        if not diff:
            diff, _ = run_git_command(["diff"])
        return diff


def get_git_status() -> str:
    """Get a summary of changed files."""
    status, _ = run_git_command(["status", "--short"])
    return status


def get_recent_commits(n: int = 5) -> str:
    """Get recent commit messages for style context."""
    log, code = run_git_command([
        "log", f"-{n}", "--pretty=format:%s", "--no-merges"
    ])
    if code != 0:
        return ""
    return log


def truncate_diff(diff: str, max_chars: int = 12000) -> str:
    """Truncate large diffs to fit within context limits."""
    if len(diff) <= max_chars:
        return diff

    lines = diff.split("\n")
    truncated = []
    total = 0
    for line in lines:
        if total + len(line) > max_chars:
            truncated.append(f"\n... [diff truncated — {len(diff) - total} chars omitted]")
            break
        truncated.append(line)
        total += len(line) + 1

    return "\n".join(truncated)


def build_user_message(diff: str, status: str, recent_commits: str) -> str:
    """Build the user message from git context."""
    context_parts = []

    if status:
        context_parts.append(f"## Changed Files\n```\n{status}\n```")

    if diff:
        context_parts.append(f"## Git Diff\n```diff\n{truncate_diff(diff)}\n```")
    else:
        print("Error: No changes detected. Stage your changes first with `git add`.")
        sys.exit(1)

    if recent_commits:
        context_parts.append(
            f"## Recent Commit Style (for reference only)\n```\n{recent_commits}\n```"
        )

    return "\n\n".join(context_parts) + "\n\nGenerate a conventional commit message for these changes."


def generate_with_claude(user_message: str, model: str) -> str:
    """Generate commit message using Claude API."""
    try:
        import anthropic
    except ImportError:
        print("Error: anthropic package not installed. Run: pip install anthropic")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("Get your key at https://console.anthropic.com")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text.strip()


def generate_with_ollama(user_message: str, model: str, host: str) -> str:
    """Generate commit message using Ollama local API."""
    url = f"{host.rstrip('/')}/api/chat"

    payload = json.dumps({
        "model": model,
        "stream": False,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            text = result["message"]["content"].strip()
            # Strip markdown code fences some models wrap output in
            if text.startswith("```"):
                lines = text.splitlines()
                lines = [l for l in lines if not l.strip().startswith("```")]
                text = "\n".join(lines).strip()
            return text
    except urllib.error.URLError:
        print(f"\nError: Cannot connect to Ollama at {host}")
        print("Make sure Ollama is running. Start it with: ollama serve")
        sys.exit(1)
    except KeyError:
        print("\nError: Unexpected response from Ollama.")
        sys.exit(1)


def generate_commit_message(
    diff: str,
    status: str,
    recent_commits: str,
    provider: str = "claude",
    model: str = "claude-opus-4-6",
    ollama_host: str = DEFAULT_OLLAMA_HOST,
) -> str:
    """Generate a commit message using the selected provider."""
    user_message = build_user_message(diff, status, recent_commits)

    if provider == "ollama":
        return generate_with_ollama(user_message, model, ollama_host)
    else:
        return generate_with_claude(user_message, model)


def apply_commit(message: str) -> None:
    """Apply the commit message using git commit."""
    result = subprocess.run(
        ["git", "commit", "-m", message],
        capture_output=False,
        text=True,
    )
    if result.returncode != 0:
        print("\nCommit failed. Make sure you have staged changes.")
        sys.exit(1)


def copy_to_clipboard(text: str) -> bool:
    """Try to copy text to clipboard. Returns True on success."""
    try:
        if sys.platform == "win32":
            subprocess.run(
                ["clip"], input=text.encode("utf-16"), check=True, capture_output=True
            )
            return True
        elif sys.platform == "darwin":
            subprocess.run(["pbcopy"], input=text.encode(), check=True, capture_output=True)
            return True
        else:
            subprocess.run(
                ["xclip", "-selection", "clipboard"],
                input=text.encode(),
                check=True,
                capture_output=True,
            )
            return True
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate smart commit messages using Claude AI or Ollama",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  smart-commit                              Staged changes via Claude
  smart-commit --all                        All changes via Claude
  smart-commit --apply                      Generate and immediately commit
  smart-commit --copy                       Copy message to clipboard
  smart-commit --provider ollama            Use local Ollama (gemma3 default)
  smart-commit --provider ollama --model gemma3:12b
  smart-commit --provider ollama --host http://YOUR_SERVER_IP:11434
  smart-commit --model claude-sonnet-4-6   Use Claude Sonnet
        """,
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Analyze all changes (staged + unstaged), not just staged",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the generated message with git commit",
    )
    parser.add_argument(
        "--copy", "-c",
        action="store_true",
        help="Copy the generated message to clipboard",
    )
    parser.add_argument(
        "--provider", "-p",
        default=os.environ.get("SMART_COMMIT_PROVIDER", "claude"),
        choices=["claude", "ollama"],
        help="AI provider to use: claude (default) or ollama (local/free)",
    )
    parser.add_argument(
        "--model", "-m",
        default=None,
        help=(
            "Model to use. Claude: claude-opus-4-6 (default), claude-sonnet-4-6, claude-haiku-4-5. "
            "Ollama: gemma3 (default), gemma3:12b, llama3, mistral, codellama"
        ),
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("SMART_COMMIT_OLLAMA_HOST", DEFAULT_OLLAMA_HOST),
        help=f"Ollama server host (default: {DEFAULT_OLLAMA_HOST}). Can also set SMART_COMMIT_OLLAMA_HOST env var",
    )
    parser.add_argument(
        "--no-context",
        action="store_true",
        help="Skip reading recent commit history for style context",
    )

    args = parser.parse_args()

    # Set default model based on provider
    if args.model is None:
        args.model = "gemma3" if args.provider == "ollama" else "claude-opus-4-6"

    # Verify we're in a git repo
    _, code = run_git_command(["rev-parse", "--git-dir"])
    if code != 0:
        print("Error: Not inside a git repository.")
        sys.exit(1)

    provider_label = f"Ollama ({args.model})" if args.provider == "ollama" else f"Claude ({args.model})"
    print(f"Analyzing changes via {provider_label}...", end=" ", flush=True)

    diff = get_git_diff(staged_only=not args.all)
    status = get_git_status()
    recent_commits = "" if args.no_context else get_recent_commits()

    if not diff:
        print()
        if args.all:
            print("No changes detected.")
        else:
            print("No staged changes. Use `git add` to stage files, or run with --all.")
        sys.exit(0)

    print("generating message...", end=" ", flush=True)

    message = generate_commit_message(
        diff=diff,
        status=status,
        recent_commits=recent_commits,
        provider=args.provider,
        model=args.model,
        ollama_host=args.host,
    )

    print("done.\n")
    print("-" * 60)
    print(message)
    print("-" * 60)

    if args.copy:
        if copy_to_clipboard(message):
            print("\nCopied to clipboard.")
        else:
            print("\nCould not copy to clipboard (clipboard tool not available).")

    if args.apply:
        print()
        apply_commit(message)
        print("Committed successfully.")
    else:
        print("\nTo use this message:")
        print(f'  git commit -m "{message.splitlines()[0]}"')
        print("  Or run with --apply to commit automatically.")


if __name__ == "__main__":
    main()
