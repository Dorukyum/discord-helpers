class StatusCycle:
    def __init__(self, *args: str) -> None:
        self.list = list(args)
        self.index = 0

    @property
    def current(self) -> str:
        return self.list[self.index]

    def __str__(self) -> str:
        return self.current

    def next(self) -> str:
        self.index += 1
        try:
            return self.current
        except IndexError:
            self.index = 0
            return self.current
