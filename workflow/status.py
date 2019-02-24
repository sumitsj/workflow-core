from enum import Enum


class Status(Enum):
    """
    Process status
    """
    WAITING = 0
    READY = 1
    RUNNING = 2
    COMPLETED = 3
    FAILED = 101
    HOLD = 201
