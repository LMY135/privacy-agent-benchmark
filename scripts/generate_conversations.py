import argparse
import json
import sys
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from agents.assistant_agent import AssistantAgent
from agents.user_agent import UserAgent
from builders.conversation_generator import (
    ConversationGenerator,
)
from clients.llm_client import LLMClient


PERSONA_DIR = (
    PROJECT_ROOT
    / "data"
    / "personas"
)

MEMORY_DIR = (
    PROJECT_ROOT
    / "data"
    / "generated"
    / "memories"
)

SCENARIO_DIR = (
    PROJECT_ROOT
    / "data"
    / "generated"
    / "scenarios"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "generated"
    / "conversations"
)


PRIVACY_CATEGORIES = [
    "personal_identity",
    "financial",
    "health_medical",
    "beliefs_and_politics",
    "relationships_and_work",
]


def load_persona(
    persona_id: str,
) -> dict:

    path = (
        PERSONA_DIR
        / f"persona_{persona_id}.yaml"
    )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        return yaml.safe_load(file)


def load_all_memories(
    persona_id: str,
) -> list[dict]:

    memories = []

    for category in PRIVACY_CATEGORIES:

        path = (
            MEMORY_DIR
            / f"persona_{persona_id}"
            / f"{category}.json"
        )

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        memories.extend(
            data["memories"]
        )

    return memories


def load_scenarios(
    persona_id: str,
) -> list[dict]:

    path = (
        SCENARIO_DIR
        / f"persona_{persona_id}"
        / "scenarios.json"
    )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    return data["scenarios"]


def save_conversation(
    persona_id: str,
    conversation: dict,
    index: int,
) -> Path:

    persona_dir = (
        OUTPUT_DIR
        / f"persona_{persona_id}"
    )

    persona_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        persona_dir
        / (
            f"{conversation['scenario_id']}"
            f"_conv_{index:02d}.json"
        )
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            conversation,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return output_path


def generate_conversations(
    persona_id: str,
    conversations_per_scenario: int,
    max_turns: int,
    scenario_id: str | None = None,
):

    persona_data = load_persona(
        persona_id
    )

    all_memories = load_all_memories(
        persona_id
    )

    print(
        f"Loaded {len(all_memories)} memories."
    )

    scenarios = load_scenarios(
        persona_id
    )

    if scenario_id is not None:
        scenarios = [
            scenario
            for scenario in scenarios
            if scenario["scenario_id"] == scenario_id
        ]

        if not scenarios:
            raise ValueError(
                f"Scenario not found: {scenario_id}"
            )

    for scenario in scenarios:

        print(
            f"\nScenario: "
            f"{scenario['scenario_id']}"
        )

        for index in range(
            1,
            conversations_per_scenario + 1,
        ):

            user_llm = LLMClient()
            assistant_llm = LLMClient()

            user_agent = UserAgent(
                persona_data=persona_data,
                memories=all_memories,
                scenario=scenario,
                llm=user_llm,
            )

            assistant_agent = AssistantAgent(
                llm=assistant_llm,
            )

            generator = ConversationGenerator(
                user_agent=user_agent,
                assistant_agent=assistant_agent,
                max_turns=max_turns,
            )

            conversation = generator.generate(
                scenario=scenario
            )

            output_path = save_conversation(
                persona_id=persona_id,
                conversation=conversation,
                index=index,
            )

            print(
                f"Saved conversation "
                f"{index}: {output_path}"
            )


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--persona",
        required=True,
    )

    parser.add_argument(
        "--scenario",
        type=str,
        default=None,
    )

    parser.add_argument(
        "--num-conversations",
        type=int,
        default=1,
    )

    parser.add_argument(
        "--max-turns",
        type=int,
        default=10,
    )

    args = parser.parse_args()

    persona_id = (
        args.persona.zfill(4)
    )

    generate_conversations(
        persona_id=persona_id,
        conversations_per_scenario=(
            args.num_conversations
        ),
        max_turns=args.max_turns,
        scenario_id=args.scenario,
    )


if __name__ == "__main__":
    main()