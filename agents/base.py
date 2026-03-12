"""Base agent class that all specialized agents inherit from."""

import anthropic


class BaseAgent:
    """Base class for all pipeline agents.

    Subclasses only need to set `name` and `system_prompt`.
    The API call logic is handled entirely by this class.
    """

    name: str = "BaseAgent"
    system_prompt: str = "You are a helpful assistant."

    def __init__(self, client: anthropic.Anthropic, model: str = "claude-sonnet-4-20250514", max_tokens: int = 4096):
        self.client = client
        self.model = model
        self.max_tokens = max_tokens

    def run(self, input_text: str) -> str:
        """Send input to Claude and return the response text."""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system_prompt,
            messages=[{"role": "user", "content": input_text}],
        )
        return message.content[0].text
