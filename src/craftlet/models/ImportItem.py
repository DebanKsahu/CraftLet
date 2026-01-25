from dataclasses import dataclass
from typing import Any

from craftlet.utils.enums import ModuleType


@dataclass
class ImportItem:
    name: str
    type: ModuleType
    fullPath: str
    parent: str
    level: int

    def __eq__(self, other: Any):
        if isinstance(other, ImportItem):
            if self.fullPath == other.fullPath and self.name == other.name:
                return True
        return False
