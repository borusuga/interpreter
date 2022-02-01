class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'cell({self.x}, {self.y})'

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.x == other.x and self.y == other.y
        return False


class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __repr__(self):
        return f'wall: ({self.x1} {self.y1}) | ({self.x2} {self.y2})'

    # def __eq__(self, other):
    #     if isinstance(other, Wall):
    #         return self.x1 == other.x1 \
    #                and self.y1 == other.y1 \
    #                and self.x2 == other.x2 \
    #                and self.y2 == self.y2
    #     return False
