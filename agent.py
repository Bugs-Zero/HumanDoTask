import subprocess
import sys


def agent(prompt: str, model: str = "sonnet") -> str:
    """
    Call an agent with the given prompt.

    Args:
        prompt: The prompt to send to the agent
        model: The model to use (default: "sonnet")

    Returns:
        The response from the agent
    """
    cmd = [
        "bunx",
        "--bun",
        "claude",
        "--dangerously-skip-permissions",
        "--model",
        model,
        "-p",
        prompt
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        # Mirror stdout to our process's stdout
        if result.stdout:
            print(result.stdout.strip())
        # Mirror stderr to our process's stderr
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        # Mirror error to stderr before raising
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        raise RuntimeError(f"Agent call failed: {e.stderr}") from e