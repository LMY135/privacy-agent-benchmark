from typing import Any

from builders.persona_builder import PersonaBuilder
from builders.prompt_builder import UserPromptBuilder


class UserAgent:

    def __init__(
        self,
        persona_data: dict[str, Any],
        memories: list[dict[str, Any]],
        llm,
        use_persona_builder: bool = True,
        use_dialogue_rules: bool = True,
    ):
        self.persona_data = persona_data
        self.memories = memories
        self.llm = llm

        self.use_persona_builder = use_persona_builder
        self.use_dialogue_rules = use_dialogue_rules

        self.persona = self._build_persona()

        self.prompt_builder = UserPromptBuilder()

        system_prompt = self.prompt_builder.build(
            stable_profile=self.persona["stable_profile"],
            dialogue_behavior=self.persona["dialogue_behavior"],
            memories=self.memories,
        )

        self.messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

    def _build_persona(self) -> dict:
        if self.use_persona_builder:
            return PersonaBuilder(
                self.persona_data
            ).build()

        # Ablation baseline:
        # use raw persona information without behavioral construction.
        return {
            "stable_profile": self.persona_data,
            "dialogue_behavior": {},
        }

    def opening_message(self) -> str:
        return self.next_turn(
            "The conversation is starting. "
            "Send your first natural message to the AI assistant."
        )

    def next_turn(
        self,
        assistant_message: str,
    ) -> str:

        self.messages.append({
            "role": "user",
            "content": assistant_message,
        })

        response = self.llm.generate(
            self.messages
        )

        self.messages.append({
            "role": "assistant",
            "content": response,
        })

        return response