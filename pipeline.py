"""Pipeline orchestrator that chains agents sequentially."""

from agents.base import BaseAgent
from agents.summary import SummaryAgent
from utils.formatting import print_agent_header, print_agent_output, print_status, print_divider


class Pipeline:
    """Runs a sequence of agents, passing output from one to the next."""

    def __init__(self, agents: list[BaseAgent]):
        self.agents = agents

    def run(self, subject: str, save_to_file: str | None = None) -> dict[str, str]:
        """Execute the full pipeline on the given subject.

        Returns a dict of agent_name -> output_text.
        """
        results: dict[str, str] = {}
        current_input = subject

        for agent in self.agents:
            print_status(f"Running {agent.name}...")
            print_agent_header(agent.name)

            # Summary agent gets ALL prior outputs, not just the previous one
            if isinstance(agent, SummaryAgent) and results:
                combined = f"# Original Subject\n{subject}\n\n"
                for name, output in results.items():
                    combined += f"# {name} Output\n{output}\n\n"
                current_input = combined

            output = agent.run(current_input)
            results[agent.name] = output

            print_agent_output(output)
            print_divider()

            # Next agent receives this agent's output
            current_input = output

        if save_to_file:
            self._save_results(subject, results, save_to_file)

        return results

    def _save_results(self, subject: str, results: dict[str, str], filepath: str) -> None:
        """Save all agent outputs to a markdown file."""
        with open(filepath, "w") as f:
            f.write(f"# Multi-Agent Analysis: {subject}\n\n")
            for name, output in results.items():
                f.write(f"---\n\n## {name}\n\n{output}\n\n")
        print(f"\n✓ Results saved to {filepath}")
