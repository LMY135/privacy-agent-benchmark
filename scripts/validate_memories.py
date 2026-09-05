import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from builders.memory_generator import PRIVACY_CATEGORIES


MEMORY_DIR = PROJECT_ROOT / "data" / "generated" / "memories"

PERSONA_IDS = [
    "0001",
    "0002",
    "0003",
    "0004",
    "0005",
    "0006",
    "0007",
    "0008",
]

EXPECTED_MEMORIES_PER_CATEGORY = 7


def validate_memories():
    errors = []

    total_files = 0
    total_memories = 0

    seen_ids = set()
    seen_texts = {}

    print("Validating memory bank...\n")

    for persona_id in PERSONA_IDS:
        persona_dir = MEMORY_DIR / f"persona_{persona_id}"

        if not persona_dir.exists():
            errors.append(
                f"Missing persona directory: {persona_dir}"
            )
            continue

        for category in PRIVACY_CATEGORIES:
            file_path = persona_dir / f"{category}.json"

            if not file_path.exists():
                errors.append(
                    f"Missing file: {file_path}"
                )
                continue

            total_files += 1

            try:
                with file_path.open(
                    "r",
                    encoding="utf-8",
                ) as file:
                    data = json.load(file)
            except json.JSONDecodeError as exc:
                errors.append(
                    f"{file_path}: invalid JSON ({exc})"
                )
                continue

            memories = data.get("memories")

            if not isinstance(memories, list):
                errors.append(
                    f"{file_path}: 'memories' must be a list"
                )
                continue

            # Check top-level metadata
            if data.get("persona_id") != persona_id:
                errors.append(
                    f"{file_path}: top-level persona_id mismatch"
                )

            if data.get("category") != category:
                errors.append(
                    f"{file_path}: top-level category mismatch"
                )

            if data.get("count") != len(memories):
                errors.append(
                    f"{file_path}: count field does not match "
                    f"actual number of memories"
                )

            if len(memories) != EXPECTED_MEMORIES_PER_CATEGORY:
                errors.append(
                    f"{file_path}: expected "
                    f"{EXPECTED_MEMORIES_PER_CATEGORY} memories, "
                    f"got {len(memories)}"
                )

            print(
                f"{persona_id} | "
                f"{category:<24} | "
                f"{len(memories)} memories"
            )

            for memory in memories:
                total_memories += 1

                if not isinstance(memory, dict):
                    errors.append(
                        f"{file_path}: memory entry is not an object"
                    )
                    continue

                required_fields = {
                    "id",
                    "persona_id",
                    "category",
                    "memory",
                }

                missing_fields = (
                    required_fields - memory.keys()
                )

                if missing_fields:
                    errors.append(
                        f"{file_path}: missing fields "
                        f"{sorted(missing_fields)}"
                    )
                    continue

                memory_id = memory["id"]
                memory_text = memory["memory"]

                # Check ID uniqueness
                if memory_id in seen_ids:
                    errors.append(
                        f"Duplicate memory ID: {memory_id}"
                    )
                else:
                    seen_ids.add(memory_id)

                # Check persona
                if memory["persona_id"] != persona_id:
                    errors.append(
                        f"{memory_id}: persona_id mismatch"
                    )

                # Check category
                if memory["category"] != category:
                    errors.append(
                        f"{memory_id}: category mismatch"
                    )

                # Check memory text
                if not isinstance(memory_text, str):
                    errors.append(
                        f"{memory_id}: memory must be a string"
                    )
                    continue

                normalized_text = (
                    memory_text.strip().lower()
                )

                if not normalized_text:
                    errors.append(
                        f"{memory_id}: empty memory"
                    )
                    continue

                # Check exact duplicate memories
                if normalized_text in seen_texts:
                    errors.append(
                        f"Duplicate memory text: "
                        f"{seen_texts[normalized_text]} "
                        f"and {memory_id}"
                    )
                else:
                    seen_texts[normalized_text] = memory_id

    expected_files = (
        len(PERSONA_IDS)
        * len(PRIVACY_CATEGORIES)
    )

    expected_memories = (
        len(PERSONA_IDS)
        * len(PRIVACY_CATEGORIES)
        * EXPECTED_MEMORIES_PER_CATEGORY
    )

    print("\n" + "=" * 60)
    print("MEMORY BANK SUMMARY")
    print("=" * 60)

    print(f"JSON files:       {total_files}")
    print(f"Total memories:   {total_memories}")
    print(f"Unique IDs:       {len(seen_ids)}")
    print(f"Unique memories:  {len(seen_texts)}")

    print("\nExpected:")
    print(f"JSON files:       {expected_files}")
    print(f"Total memories:   {expected_memories}")

    print("=" * 60)

    if total_files != expected_files:
        errors.append(
            f"Expected {expected_files} files, "
            f"got {total_files}"
        )

    if total_memories != expected_memories:
        errors.append(
            f"Expected {expected_memories} memories, "
            f"got {total_memories}"
        )

    if errors:
        print("\nVALIDATION FAILED\n")

        for error in errors:
            print(f"[ERROR] {error}")

        print(f"\nTotal errors: {len(errors)}")

        sys.exit(1)

    print("\nVALIDATION PASSED")
    print(
        f"All {total_memories} memories are "
        f"structurally valid and unique."
    )


if __name__ == "__main__":
    validate_memories()