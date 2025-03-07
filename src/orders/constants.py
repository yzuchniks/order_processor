from enum import Enum

MAX_SIZE_QUE = 50
DEFAULT_NUM_WORKERS = 5
CHANCE_ERROR = 0.3


class Status(Enum):
    PENDING = "Ожидает"
    IN_PROGRESS = "Выполняется"
    DONE = "Завершен"
    FAILED = "Ошибка при выполнении"


class RangeDelay(Enum):
    MIN_DELAY = 0.5
    MAX_DELAY = 3.0


class Retry(Enum):
    DEFAULT_RETRIES = 3
    DELAY = 1
