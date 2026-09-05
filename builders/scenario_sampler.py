import random
from typing import Any


class ScenarioSampler:

    def __init__(
        self,
        task_families: dict[str, Any],
        seed: int = 42,
    ):
        self.task_families = task_families
        self.random = random.Random(seed)

    def sample_task_family(self) -> str:
        return self.random.choice(
            list(self.task_families.keys())
        )