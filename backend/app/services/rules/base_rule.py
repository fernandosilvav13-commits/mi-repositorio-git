from abc import ABC, abstractmethod


class BaseRule(ABC):
    name: str = ""
    description: str = ""
    field: str = ""

    def __init__(self, enabled: bool = False):
        self._enabled = enabled
        self._total = 0
        self._hits = 0

    @abstractmethod
    def evaluate(self, text: str, current_data: dict) -> str | None:
        ...

    def shadow_evaluate(self, text: str, current_data: dict) -> str | None:
        self._total += 1
        return self.evaluate(text, current_data)

    def record_hit(self) -> None:
        self._hits += 1

    @property
    def precision(self) -> float:
        return self._hits / self._total if self._total > 0 else 0.0

    @property
    def ready_for_activation(self) -> bool:
        return self._total >= 100 and self.precision >= 0.9

    @property
    def enabled(self) -> bool:
        return self._enabled

    def enable(self) -> None:
        self._enabled = True

    def disable(self) -> None:
        self._enabled = False
