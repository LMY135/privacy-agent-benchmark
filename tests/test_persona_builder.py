from pathlib import Path
import yaml

from builders.persona_builder import PersonaBuilder


ROOT = Path(__file__).resolve().parents[1]
PERSONA_DIR = ROOT / "data" / "personas"


def test_build_all_personas():
    persona_files = sorted(PERSONA_DIR.glob("persona_*.yaml"))

    assert len(persona_files) == 8

    for path in persona_files:
        with open(path, "r", encoding="utf-8") as f:
            raw_persona = yaml.safe_load(f)

        persona = PersonaBuilder(raw_persona).build()

        assert persona["persona_id"] is not None
        assert "identity_profile" in persona
        assert "dialogue_behavior" in persona
        assert "memory_context" in persona


def test_persona_builder_output():
    path = PERSONA_DIR / "persona_0001.yaml"

    with open(path, "r", encoding="utf-8") as f:
        raw_persona = yaml.safe_load(f)

    persona = PersonaBuilder(raw_persona).build()

    print("\nPersona 0001:")
    print(persona)

    from pathlib import Path
import yaml

from builders.persona_builder import PersonaBuilder


ROOT = Path(__file__).resolve().parents[1]
PERSONA_DIR = ROOT / "data" / "personas"


def test_build_all_personas():
    persona_files = sorted(PERSONA_DIR.glob("persona_*.yaml"))

    assert len(persona_files) == 8

    for path in persona_files:
        with open(path, "r", encoding="utf-8") as f:
            raw_persona = yaml.safe_load(f)

        persona = PersonaBuilder(raw_persona).build()

        assert persona["persona_id"] is not None
        assert "identity_profile" in persona
        assert "dialogue_behavior" in persona
        assert "memory_context" in persona


def test_persona_builder_output():
    path = PERSONA_DIR / "persona_0001.yaml"

    with open(path, "r", encoding="utf-8") as f:
        raw_persona = yaml.safe_load(f)

    persona = PersonaBuilder(raw_persona).build()

    print("\nPersona 0001:")
    print(persona)

    print("\nTop-level keys:")
    print(raw_persona.keys())

    print("\nDimensions keys containing bfi/cog/interpersonal/register:")
    dimensions = raw_persona.get("dimensions", {})
    for key, value in dimensions.items():
        if (
            key.startswith("bfi2_")
            or key.startswith("cog_")
            or key.startswith("interpersonal_")
            or key == "register"
        ):
            print(key, "=", value)

    persona = PersonaBuilder(raw_persona).build()

    print("\nPersona 0001:")
    print(persona)