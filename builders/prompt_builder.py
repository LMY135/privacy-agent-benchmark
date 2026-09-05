from pathlib import Path
from typing import Any


class UserPromptBuilder:

    def __init__(
        self,
        template_path: str = (
            "prompts/user_system.txt"
        ),
    ):
        self.template_path = Path(
            template_path
        )

    def build(
        self,
        identity_profile: dict[str, Any],
        behavior_profile: dict[str, Any],
        memories: list[dict[str, Any]],
        scenario: dict[str, Any],
    ) -> str:

        template = (
            self.template_path.read_text(
                encoding="utf-8"
            )
        )

        identity_text = (
            self._render_dict(
                identity_profile
            )
        )

        behavior_text = (
            self._render_dict(
                behavior_profile
            )
        )

        memory_text = (
            self._render_memories(
                memories
            )
        )

        scenario_text = (
            self._render_scenario(
                scenario
            )
        )

        return template.format(
            identity_profile=identity_text,
            behavior_profile=behavior_text,
            personal_memory=memory_text,
            scenario=scenario_text,
        )

    @staticmethod
    def _render_dict(
        data: dict[str, Any],
    ) -> str:

        if not data:
            return "None"

        return "\n".join(
            f"- {key}: {value}"
            for key, value in data.items()
        )

    @staticmethod
    def _render_memories(
        memories: list[dict[str, Any]],
    ) -> str:

        if not memories:
            return "None"

        lines = []

        for memory in memories:

            category = memory.get(
                "category",
                "unknown",
            )

            text = memory.get(
                "memory",
                "",
            )

            lines.append(
                f"- [{category}] {text}"
            )

        return "\n".join(lines)

    @staticmethod
    def _render_scenario(
        scenario: dict[str, Any],
    ) -> str:

        return (
            f"Task family: "
            f"{scenario['task_family']}\n"
            f"Privacy category: "
            f"{scenario['privacy_category']}\n"
            f"Domain: "
            f"{scenario['domain']}\n"
            f"Context: "
            f"{scenario['context']}\n"
            f"Goal: "
            f"{scenario['user_goal']}"
        )