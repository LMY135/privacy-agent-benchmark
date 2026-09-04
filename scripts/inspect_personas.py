from pathlib import Path
from collections import defaultdict
import yaml


PERSONA_DIR = Path("data/personas")


def main():
    field_values = defaultdict(set)

    persona_files = sorted(PERSONA_DIR.glob("persona_*.yaml"))

    print(f"Found {len(persona_files)} personas.\n")

    for path in persona_files:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        print(f"=== {path.name} ===")

        for key, value in data.items():
            if key == "dimensions" and isinstance(value, dict):
                for dim_key, dim_value in value.items():
                    field_values[dim_key].add(str(dim_value))
            else:
                field_values[key].add(str(value))

    print("\n\n===== ATTRIBUTE INVENTORY =====\n")

    for field in sorted(field_values):
        values = list(field_values[field])

        print(f"[{field}]")

        for value in values[:8]:
            print(f"  - {value}")

        if len(values) > 8:
            print(f"  ... ({len(values)} unique values)")

        print()


if __name__ == "__main__":
    main()