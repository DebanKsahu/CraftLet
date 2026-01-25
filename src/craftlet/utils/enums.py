from enum import StrEnum


class ModuleType(StrEnum):
    STDLIB_MODULE = "Standard Library Module"
    BUILT_IN_MODULE = "Built In Python Module"
    VENV_MODULE = "Venv Module"
    LOCAL_MODULE = "Project/User Module"
