from pathlib import Path
from typing import Any


class UserPromptBuilder:
    def __init__(
        self,
        template_path: str = "prompts/user_system.txt",
    ):
        self.template_path = Path(template_path)

    def build(
        self,
        stable_profile: dict[str, Any],
        dialogue_behavior: dict[str, Any],
        memories: list[dict[str, Any]],
    ) -> str:

        template = self.template_path.read_text(
            encoding="utf-8"
        )

        profile_text = self._render_dict(stable_profile)

        behavior_text = self._render_behavior(
            dialogue_behavior
        )

        memory_text = self._render_memories(memories)

        return template.format(
            stable_profile=profile_text,
            dialogue_behavior=behavior_text,
            personal_memory=memory_text,
        )

    def _render_dict(
        self,
        data: dict[str, Any],
    ) -> str:

        if not data:
            return "No additional profile information."

        return "\n".join(
            f"- {key}: {value}"
            for key, value in data.items()
        )

    def _render_behavior(
        self,
        behavior: dict[str, Any],
    ) -> str:

        if not behavior:
            return (
                "Communicate naturally as an ordinary user. "
                "Do not sound like an AI assistant."
            )

        lines = []

        for key, value in behavior.items():
            lines.append(f"- {key}: {value}")

        return "\n".join(lines)

    def _render_memories(
        self,
        memories: list[dict[str, Any]],
    ) -> str:

        if not memories:
            return "No personal memories are available."

        lines = []

        for item in memories:
            memory = item.get("memory")

            if memory:
                lines.append(f"- {memory}")

        return "\n".join(lines)