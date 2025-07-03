from enum import StrEnum, auto


class TaskStatus(StrEnum):
    IN_PROGRESS = auto()
    DONE = auto()
    ERROR = auto()
