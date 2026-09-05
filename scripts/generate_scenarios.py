import argparse
import json
import random
import sys
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from builders.persona_builder import PersonaBuilder
from builders.scenario_generator import ScenarioGenerator
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

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "generated"
    / "scenarios"
)

SCENARIO_CONFIG_PATH = (
    PROJECT_ROOT
    / "configs"
    / "conversation_scenarios.yaml"
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

    if not path.exists():
        raise FileNotFoundError(
            f"Persona not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        raw_persona = yaml.safe_load(file)

    return PersonaBuilder(
        raw_persona
    ).build()


def load_category_memories(
    persona_id: str,
    category: str,
) -> list[dict]:

    path = (
        MEMORY_DIR
        / f"persona_{persona_id}"
        / f"{category}.json"
    )

    if not path.exists():
        raise FileNotFoundError(
            f"Memory file not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    memories = data.get(
        "memories",
        [],
    )

    if not memories:
        raise ValueError(
            f"No memories found for "
            f"{persona_id} / {category}"
        )

    return memories


def load_scenario_families() -> dict:

    with SCENARIO_CONFIG_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:

        data = yaml.safe_load(file)

    return data["scenario_families"]


def sample_anchor_memories(
    persona_id: str,
    rng: random.Random,
) -> list[dict]:

    selected_memories = []

    for category in PRIVACY_CATEGORIES:

        memories = load_category_memories(
            persona_id=persona_id,
            category=category,
        )

        selected_memory = rng.choice(
            memories
        )

        selected_memories.append(
            selected_memory
        )

    return selected_memories


def save_scenarios(
    persona_id: str,
    scenarios: list[dict],
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
        / "scenarios.json"
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            {
                "persona_id": persona_id,
                "count": len(scenarios),
                "scenarios": scenarios,
            },
            file,
            ensure_ascii=False,
            indent=2,
        )

    return output_path


def generate_scenarios(
    persona_id: str,
    seed: int,
):

    rng = random.Random(
        seed + int(persona_id)
    )

    persona = load_persona(
        persona_id
    )

    scenario_families = (
        load_scenario_families()
    )

    task_families = list(
        scenario_families.keys()
    )

    if len(task_families) != 5:
        raise ValueError(
            "Expected exactly 5 task families."
        )

    anchor_memories = (
        sample_anchor_memories(
            persona_id=persona_id,
            rng=rng,
        )
    )

    rng.shuffle(
        task_families
    )

    llm_client = LLMClient()

    generator = ScenarioGenerator(
        llm_client=llm_client
    )

    scenarios = []

    print(
        f"\nScenario assignments "
        f"for persona {persona_id}:\n"
    )

    for memory, task_family in zip(
        anchor_memories,
        task_families,
    ):

        config = (
            scenario_families[
                task_family
            ]
        )

        print(
            f"{memory['category']:<28}"
            f" -> {task_family}"
        )

        print(
            f"  anchor: {memory['id']}"
        )

        scenario = generator.generate(
            persona=persona,
            memory=memory,
            task_family=task_family,
            task_description=(
                config["description"]
            ),
            goal_pattern=(
                config["goal_pattern"]
            ),
        )

        scenarios.append(
            scenario
        )

    output_path = save_scenarios(
        persona_id=persona_id,
        scenarios=scenarios,
    )

    print(
        f"\nGenerated {len(scenarios)} scenarios."
    )

    print(
        f"Saved to: {output_path}"
    )


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Generate five balanced scenarios "
            "for one persona."
        )
    )

    parser.add_argument(
        "--persona",
        required=True,
        help="Persona ID, e.g. 0001",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
    )

    args = parser.parse_args()

    persona_id = (
        args.persona.zfill(4)
    )

    generate_scenarios(
        persona_id=persona_id,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()