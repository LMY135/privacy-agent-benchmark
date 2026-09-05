from typing import Any

from agents.assistant_agent import AssistantAgent
from agents.user_agent import UserAgent


class ConversationGenerator:

    def __init__(
        self,
        user_agent: UserAgent,
        assistant_agent: AssistantAgent,
        min_turns: int = 5,
        max_turns: int = 10,
    ):
        self.user_agent = user_agent
        self.assistant_agent = assistant_agent

        self.min_turns = min_turns
        self.max_turns = max_turns

        if self.min_turns < 1:
            raise ValueError(
                "min_turns must be at least 1."
            )

        if self.max_turns < self.min_turns:
            raise ValueError(
                "max_turns must be greater than "
                "or equal to min_turns."
            )

    def generate(
        self,
        scenario: dict[str, Any],
    ) -> dict[str, Any]:

        self.user_agent.reset()
        self.assistant_agent.reset()

        conversation = []

        print(
            f"[Turn 1/{self.max_turns}] "
            f"User generating opening message..."
        )

        (
            user_message,
            should_continue,
        ) = self.user_agent.opening_message()

        for turn in range(
            1,
            self.max_turns + 1,
        ):

            conversation.append({
                "turn": turn,
                "role": "user",
                "content": user_message,
            })

            print(
                f"[Turn {turn}/{self.max_turns}] "
                f"Assistant generating..."
            )

            assistant_message = (
                self.assistant_agent.next_turn(
                    user_message
                )
            )

            conversation.append({
                "turn": turn,
                "role": "assistant",
                "content": assistant_message,
            })

            # Hard safety cap.
            if turn >= self.max_turns:
                print(
                    "[Conversation] Reached "
                    f"max_turns={self.max_turns}. "
                    "Stopping."
                )
                break

            # Allow natural stopping only after
            # the minimum number of turns.
            if (
                turn >= self.min_turns
                and not should_continue
            ):
                print(
                    "[Conversation] User decided "
                    f"to stop after turn {turn}."
                )
                break

            print(
                f"[Turn {turn + 1}/{self.max_turns}] "
                f"User generating..."
            )

            (
                user_message,
                should_continue,
            ) = self.user_agent.next_turn(
                assistant_message
            )

        return {
            "scenario_id": (
                scenario["scenario_id"]
            ),
            "persona_id": (
                scenario["persona_id"]
            ),
            "task_family": (
                scenario["task_family"]
            ),
            "privacy_category": (
                scenario["privacy_category"]
            ),
            "anchor_memory_id": (
                scenario["anchor_memory_id"]
            ),
            "num_turns": self._count_turns(
                conversation
            ),
            "messages": conversation,
        }

    @staticmethod
    def _count_turns(
        conversation: list[dict[str, Any]],
    ) -> int:

        return sum(
            1
            for message in conversation
            if message["role"] == "user"
        )