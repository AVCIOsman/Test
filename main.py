"""CLI entry point for the multi-agent workflow."""

import argparse
import sys
import os

import anthropic

from agents import ResearchAgent, StrategyAgent, BlueprintAgent, SummaryAgent
from pipeline import Pipeline
from utils.formatting import BOLD, CYAN, RESET


def main():
    parser = argparse.ArgumentParser(
        description="Multi-agent AI workflow: Research → Strategy → Blueprint → Summary"
    )
    parser.add_argument(
        "subject",
        nargs="?",
        help="The subject or idea to analyze",
    )
    parser.add_argument(
        "-o", "--output",
        help="File path to save the full analysis as markdown",
    )
    args = parser.parse_args()

    # Get subject from argument or interactive prompt
    subject = args.subject
    if not subject:
        print(f"{CYAN}{BOLD}Multi-Agent Workflow{RESET}")
        print("Enter the subject or idea you want to analyze:\n")
        subject = input("> ").strip()
        if not subject:
            print("Error: No subject provided.")
            sys.exit(1)

    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable is not set.")
        print("Set it with: export ANTHROPIC_API_KEY=your-api-key")
        sys.exit(1)

    # Initialize client and agents
    client = anthropic.Anthropic()
    agents = [
        ResearchAgent(client),
        StrategyAgent(client),
        BlueprintAgent(client),
        SummaryAgent(client),
    ]

    # Run pipeline
    print(f"\n{CYAN}{BOLD}═══ Multi-Agent Analysis ═══{RESET}")
    print(f"Subject: {subject}\n")

    pipe = Pipeline(agents)
    try:
        pipe.run(subject, save_to_file=args.output)
    except anthropic.APIError as e:
        print(f"\nAPI Error: {e}")
        sys.exit(1)

    print(f"\n{CYAN}{BOLD}═══ Analysis Complete ═══{RESET}")


if __name__ == "__main__":
    main()
