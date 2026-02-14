#!/usr/bin/env python3
"""Process to fix lint issues one at a time using an agent."""

import os
import subprocess
import tempfile
from human_do_task import Process


def count_lint_issues(lint_output: str) -> int:
    """Count the number of lint issues in the output."""
    return len([line for line in lint_output.strip().split('\n') if line])


def run_linter() -> tuple[str, int]:
    """Run the linter and return output and count of issues."""
    try:
        # Run flake8 (Python linter) - adjust command for your project
        result = subprocess.run(
            ['flake8', '.'],
            capture_output=True,
            text=True,
            check=False
        )
        output = result.stdout + result.stderr
        count = count_lint_issues(output)
        return output, count
    except FileNotFoundError:
        print("Linter not found. Please install flake8: pip install flake8")
        return "", 0


def save_to_file(content: str, filename: str) -> None:
    """Save content to a file."""
    with open(filename, 'w') as f:
        f.write(content)


def revert_changes() -> None:
    """Revert the last git changes."""
    subprocess.run(['git', 'checkout', '.'], check=False)
    if os.path.exists('commit_msg.txt'):
        os.remove('commit_msg.txt')


def commit_changes() -> None:
    """Commit the current changes using the saved commit message."""
    if os.path.exists('commit_msg.txt'):
        with open('commit_msg.txt', 'r') as f:
            commit_msg = f.read().strip()
        subprocess.run(['git', 'add', '-A'], check=True)
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        os.remove('commit_msg.txt')
        print(f"Committed: {commit_msg}")
    else:
        print("No commit message found")


def perform(go: Process) -> None:
    """Main process to fix lint issues one by one."""

    # Initial setup
    go.tell("Please ensure you have a clean git working directory before starting.")

    iteration = 0
    max_iterations = 50  # Prevent infinite loops

    while iteration < max_iterations:
        iteration += 1
        print(f"\n=== Iteration {iteration} ===\n")

        # Run linter and save results
        go.do(lambda: print("Running linter..."))
        lint_output, issue_count = run_linter()

        if issue_count == 0:
            print("No lint issues found! Process complete.")
            break

        go.do(lambda: save_to_file(lint_output, f'lint_results_{iteration}.txt'))
        print(f"Found {issue_count} lint issue(s)")

        # Ask agent to fix ONE issue
        prompt = f"""
Look at the lint issues in this output and fix EXACTLY ONE RANDOM issue:

{lint_output}

Instructions:
1. Pick only ONE RANDOM lint issue from the output
2. Fix that single issue in the code
3. Do NOT fix any other issues
4. Do NOT create a commit
5. Write a brief commit message (one line) describing what you fixed and save it to 'commit_msg.txt'
6. Return the exact lint issue you fixed

Example commit message: "Fix E501 line too long in example.py:42"
"""

        go.agent(prompt)

        # Check if lint issues decreased
        go.do(lambda: print("\nChecking if lint issues decreased..."))
        new_lint_output, new_issue_count = run_linter()

        if new_issue_count < issue_count:
            print(f"Success! Lint issues reduced from {issue_count} to {new_issue_count}")

            # Ask human for approval
            if go.ask_yes_no(f"The agent fixed 1 issue (from {issue_count} to {new_issue_count} issues). Review the changes and approve?"):
                go.do(commit_changes)
                print("Changes committed successfully")
            else:
                go.do(revert_changes)
                print("Changes reverted by user")
                if not go.ask_yes_no("Do you want to continue fixing other issues?"):
                    break
        else:
            print(f"Failed to reduce issues (still {new_issue_count} issues). Reverting...")
            go.do(revert_changes)

            if not go.ask_yes_no("The fix didn't work. Try again?"):
                break

    if iteration >= max_iterations:
        print(f"Reached maximum iterations ({max_iterations}). Stopping.")

    print("\nProcess complete!")


def verify(go: Process) -> None:
    """Verify the lint fixing process."""

    # Check git is available
    go.verify(lambda: subprocess.run(['git', '--version'], capture_output=True).returncode == 0)

    # Check linter is available
    go.verify(lambda: subprocess.run(['which', 'flake8'], capture_output=True).returncode == 0 or
              subprocess.run(['which', 'ruff'], capture_output=True).returncode == 0)

    # Check we're in a git repository
    go.verify(lambda: os.path.exists('.git'))

    # Check git working directory is clean
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    go.verify(lambda: len(result.stdout.strip()) == 0)

    go.verify(go.that("the agent command (bunx claude) is available"))


if __name__ == "__main__":
    Process.run(perform, verify)