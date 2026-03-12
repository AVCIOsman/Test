"""Console formatting helpers using ANSI escape codes."""

# ANSI color codes
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
DIM = "\033[2m"
RESET = "\033[0m"


def print_agent_header(agent_name: str) -> None:
    """Print a boxed header for an agent's output section."""
    width = len(agent_name) + 6
    border = "═" * width
    print(f"\n{CYAN}{BOLD}╔{border}╗")
    print(f"║   {agent_name}   ║")
    print(f"╚{border}╝{RESET}\n")


def print_agent_output(text: str) -> None:
    """Print agent output with subtle formatting."""
    print(f"{text}\n")


def print_status(message: str) -> None:
    """Print a status message (e.g., 'Running agent...')."""
    print(f"{YELLOW}{BOLD}▶ {message}{RESET}")


def print_divider() -> None:
    """Print a thin divider between sections."""
    print(f"{DIM}{'─' * 60}{RESET}")
