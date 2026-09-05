import json
from typing import Any

from builders.persona_builder import PersonaBuilder
from builders.prompt_builder import UserPromptBuilder


class UserAgent:

    def __init__(
        self,
        persona_data: dict[str, Any],
        memories: list[dict[str, Any]],
        scenario: dict[str, Any],
        llm,
        use_persona_builder: bool = True,
    ):
        self.persona_data = persona_data
        self.memories = memories
        self.scenario = scenario
        self.llm = llm

        self.use_persona_builder = (
            use_persona_builder
        )

        self.persona = (
            self._build_persona()
        )

        self.prompt_builder = (
            UserPromptBuilder()
        )

        self.messages: list[dict[str, str]] = []

        self.reset()

    def _build_persona(
        self,
    ) -> dict[str, Any]:

        if self.use_persona_builder:

            return PersonaBuilder(
                self.persona_data
            ).build()

        return {
            "identity_profile":
                self.persona_data,

            "behavior_profile": {},
        }

    def reset(
        self,
    ) -> None:

        system_prompt = (
            self.prompt_builder.build(
                identity_profile=(
                    self.persona[
                        "identity_profile"
                    ]
                ),
                behavior_profile=(
                    self.persona[
                        "behavior_profile"
                    ]
                ),
                memories=self.memories,
                scenario=self.scenario,
            )
        )

        print("\n" + "=" * 80)
        print("USER SYSTEM PROMPT")
        print("=" * 80)
        print(system_prompt)
        print("=" * 80 + "\n")

        self.messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

    def opening_message(
        self,
    ) -> tuple[str, bool]:

        return self.next_turn(
            (
                "The conversation is starting. "
                "Begin naturally based on your "
                "current situation and goal. "
                "Do not try to explain everything "
                "about the situation immediately."
            )
        )

    def next_turn(
        self,
        assistant_message: str,
    ) -> tuple[str, bool]:

        self.messages.append({
            "role": "user",
            "content": assistant_message,
        })

        response_text = (
            self.llm.generate(
                self.messages
            )
        )

        data = self._parse_response(
            response_text
        )

        message = data["message"]
        should_continue = data["continue"]

        self.messages.append({
            "role": "assistant",
            "content": response_text,
        })

        return (
            message,
            should_continue,
        )

    @staticmethod
    def _parse_response(
        response_text: str,
    ) -> dict[str, Any]:

        try:
            data = json.loads(
                response_text
            )

        except json.JSONDecodeError as exc:

            raise ValueError(
                "UserAgent returned invalid JSON:\n"
                f"{response_text}"
            ) from exc

        if not isinstance(
            data,
            dict,
        ):
            raise ValueError(
                "UserAgent response must be a JSON object."
            )

        message = data.get(
            "message"
        )

        should_continue = data.get(
            "continue"
        )

        if (
            not isinstance(
                message,
                str,
            )
            or not message.strip()
        ):
            raise ValueError(
                "UserAgent response must contain "
                "a non-empty string field 'message'."
            )

        if not isinstance(
            should_continue,
            bool,
        ):
            raise ValueError(
                "UserAgent response must contain "
                "a boolean field 'continue'."
            )

        return {
            "message": message.strip(),
            "continue": should_continue,
        }