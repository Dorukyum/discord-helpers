from typing import List


class StatusCycle:
    def __init__(self, *statuses: str) -> None:
        self.statuses: List[str] = list(statuses)
        self.index: int = 0

    @property
    def current(self) -> str:
        return self.statuses[self.index]

    def __str__(self) -> str:
        return self.current

    def next(self) -> str:
        self.index += 1
        try:
            return self.current
        except IndexError:
            self.index = 0
            return self.current
