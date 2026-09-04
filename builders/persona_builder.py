from typing import Any


IDENTITY_FIELDS = [
    "age_bracket",
    "region",
    "gender_identity",
    "primary_language",
    "english_proficiency",
    "multilingualism",
    "domain",
    "domain_characteristics",
    "cultural_background",
    "demo_generation",
]


BEHAVIOR_FIELDS = [
    # decision / value orientation
    "risk_tolerance",
    "values_priority",
    "safety_sensitivity",

    # familiarity / interests
    "fam_sports_science",
    "topic_sports",
    "topic_fitness",

    # character traits
    "trait_capacity_for_love",
    "trait_kindness",
    "trait_social_intelligence",
    "trait_teamwork",
    "trait_fairness",
    "trait_leadership",
    "trait_forgiveness",
    "trait_humility",
    "trait_prudence",
    "trait_self_regulation",
    "trait_appreciation_of_beauty",
    "trait_gratitude",
    "trait_hope_optimism",
    "trait_playfulness",
    "trait_spirituality",
    "trait_ambition",
    "trait_empathy",
    "trait_resilience",
    "trait_discipline",
    "trait_generosity",
    "trait_loyalty",
    "trait_competitiveness",
    "trait_adaptability",

    # values
    "val_career_success",
    "val_achievement",
    "val_recognition",
]


class PersonaBuilder:
    def __init__(self, persona_data: dict[str, Any]):
        self.persona_data = persona_data
        self.dimensions = persona_data.get("dimensions", {})

    def build(self) -> dict[str, Any]:
        return {
            "persona_id": self.persona_data.get("persona_id"),
            "display_name": self.persona_data.get("display_name"),
            "identity_profile": self._select_fields(IDENTITY_FIELDS),
            "behavior_profile": self._select_fields(BEHAVIOR_FIELDS),
        }

    def _select_fields(self, fields: list[str]) -> dict[str, Any]:
        result = {}

        for field in fields:
            value = self._get_value(field)

            if self._is_valid(value):
                result[field] = value

        return result

    def _get_value(self, field: str) -> Any:
        if field in self.persona_data:
            return self.persona_data[field]

        return self.dimensions.get(field)

    @staticmethod
    def _is_valid(value: Any) -> bool:
        if value is None:
            return False

        if isinstance(value, str):
            normalized = value.strip().lower()

            if normalized in {
                "",
                "none",
                "null",
                "unknown",
                "not applicable",
                "n/a",
                "unfamiliar",
            }:
                return False

        return True