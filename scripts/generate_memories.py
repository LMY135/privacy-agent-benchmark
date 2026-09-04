import argparse
import json
import sys
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from builders.memory_generator import (
    MemoryGenerator,
    PRIVACY_CATEGORIES,
)
from builders.persona_builder import PersonaBuilder
from clients.llm_client import LLMClient


PERSONA_DIR = PROJECT_ROOT / "data" / "personas"
OUTPUT_DIR = PROJECT_ROOT / "data" / "generated" / "memories"


def load_persona(persona_id: str) -> dict:
    """
    Load a raw persona YAML file and build the normalized persona.
    """

    persona_path = PERSONA_DIR / f"persona_{persona_id}.yaml"

    if not persona_path.exists():
        raise FileNotFoundError(
            f"Persona file not found: {persona_path}"
        )

    with persona_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        raw_persona = yaml.safe_load(file)

    persona = PersonaBuilder(raw_persona).build()

    return persona


def save_memories(
    persona_id: str,
    category: str,
    memories: list[dict[str, str]],
) -> Path:
    """
    Save generated memories under the corresponding persona directory.
    """

    persona_output_dir = (
        OUTPUT_DIR / f"persona_{persona_id}"
    )

    persona_output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        persona_output_dir / f"{category}.json"
    )

    output_data = {
        "persona_id": persona_id,
        "category": category,
        "count": len(memories),
        "memories": memories,
    }

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            output_data,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return output_path


def generate_single_category(
    persona_id: str,
    category: str,
    count: int,
) -> Path:
    """
    Generate memories for one persona and one privacy category.
    """

    if category not in PRIVACY_CATEGORIES:
        raise ValueError(
            f"Unknown category: {category}. "
            f"Available categories: "
            f"{list(PRIVACY_CATEGORIES.keys())}"
        )

    print(f"Loading persona {persona_id}...")

    persona = load_persona(persona_id)

    print("Initializing LLM client...")

    llm_client = LLMClient()

    generator = MemoryGenerator(
        llm_client=llm_client,
    )

    print(
        f"Generating {count} memories "
        f"for '{category}'..."
    )

    memories = generator.generate(
        persona=persona,
        category=category,
        count=count,
    )

    output_path = save_memories(
        persona_id=persona_id,
        category=category,
        memories=memories,
    )

    print(f"Saved to: {output_path}")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Generate synthetic private memories "
            "for one persona."
        )
    )

    parser.add_argument(
        "--persona",
        required=True,
        help="Persona ID, e.g. 0001",
    )

    parser.add_argument(
        "--category",
        required=True,
        choices=list(PRIVACY_CATEGORIES.keys()),
        help="Privacy category",
    )

    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of memories to generate",
    )

    args = parser.parse_args()

    persona_id = args.persona.zfill(4)

    generate_single_category(
        persona_id=persona_id,
        category=args.category,
        count=args.count,
    )


if __name__ == "__main__":
    main()