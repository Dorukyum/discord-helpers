class StatusCycle:
    def __init__(self, *args):
        self.list = list(args)
        self.index = 0

    @property
    def current(self):
        return self.list[self.index]

    def __str__(self):
        return self.current

    def next(self):
        self.index += 1
        try:
            return self.current
        except IndexError:
            self.index = 0
            return self.current
