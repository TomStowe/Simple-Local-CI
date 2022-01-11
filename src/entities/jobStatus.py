from enum import Enum

class JobStatus(Enum):
    PENDING = 0
    RUNNING = 1
    INTERRUPTED = 2
    FAILURE = 3
    TIMEOUT = 4
    SUCCESS = 5