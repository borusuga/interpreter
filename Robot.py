from math import cos, sqrt, acos

from d_classes.Cell import *
from json_convert import *


class Robot:
    def __init__(self, x: int, y: int, rotation: int, map_: list, walls: list, finish: Cell):
        """
        Parameters:
            x(int): x coordinate (top-right)
            y(int): y coordinate (top)
            rotation(int): rotation from 0 (top) to 5 (top-left) counterclockwise
            map_(dict): two-dimensional dict of Cell object
        """
        self.x = x
        self.y = y
        self.rotation = rotation
        self.map = map_
        self.walls = walls
        self.finish_cell = finish
        self.log = [f'Started at {self.x},{self.y} : {self.rotation}']
        self.sonar_level = 0
        self.sonar_cells = dict()
        self.sonar_forbitten_cells = list()

    def __repr__(self):
        return f'''(x:{self.x}, y:{self.y}), rotation:{self.rotation}'''

    def next(self):
        """Return a Cell towards robot"""
        x = self.x
        y = self.y
        if self.rotation == 0:
            y += 1
        elif self.rotation == 1:
            x += 1
        elif self.rotation == 2:
            x += 1
            y -= 1
        elif self.rotation == 3:
            y -= 1
        elif self.rotation == 4:
            x -= 1
        elif self.rotation == 5:
            x -= 1
            y += 1
        next_cell = Cell(x, y)
        if next_cell in self.map:
            return Cell(x, y)
        else:
            return None

    def go(self):
        if self.is_finish():
            self.log.append(f'ERROR GO. Remain at finish cell({self.x}, {self.y}) : {self.rotation}')
            return 0
        next_cell = self.next()
        if next_cell is None:
            self.log.append(f'ERROR GO. Remain at cell({self.x}, {self.y}) : {self.rotation}')
            return 0
        for wall in self.walls:
            if Cell(self.x, self.y) == Cell(wall.x1, wall.y1) and next_cell == Cell(wall.x2, wall.y2) \
                    or next_cell == Cell(wall.x1, wall.y1) and Cell(self.x, self.y) == Cell(wall.x2, wall.y2):
                self.log.append(f'ERROR GO. Remain at cell({self.x}, {self.y}) : {self.rotation}')
                return 0
        self.x = next_cell.x
        self.y = next_cell.y
        self.log.append(f'GO. Move to cell({self.x}, {self.y}) : {self.rotation}')
        self.sonar_level = 0
        self.sonar_cells.clear()
        if self.is_finish():
            self.log.append(f'FINISH. Moved to the final cell({self.x}, {self.y})')
        return 1

    def rl(self):
        self.rotation = (self.rotation + 5) % 6
        self.sonar_level = 0
        self.sonar_cells.clear()
        self.sonar_forbitten_cells.clear()
        self.log.append(f'ROTATION LEFT. Remain at cell({self.x}, {self.y}) : {self.rotation}')
        return 1

    def rr(self):
        self.rotation = (self.rotation + 1) % 6
        self.sonar_level = 0
        self.sonar_cells.clear()
        self.sonar_forbitten_cells.clear()
        self.log.append(f'ROTATION RIGHT. Remain at cell({self.x}, {self.y}) : {self.rotation}')
        return 1

    def is_finish(self):
        return self.finish_cell == Cell(self.x, self.y)

    def compass(self):
        pi = 3.14
        ax = self.finish_cell.x - self.x
        ay = self.finish_cell.y - self.y
        bx = 0
        by = 0
        if self.rotation == 0:
            by += 1
        elif self.rotation == 1:
            bx += 1
        elif self.rotation == 2:
            bx += 1
            by -= 1
        elif self.rotation == 3:
            by -= 1
        elif self.rotation == 4:
            bx -= 1
        elif self.rotation == 5:
            bx -= 1
            by += 1
        ab = ax * bx + ay * by + (ax * by + ay * bx) * cos(pi / 3)
        a = sqrt(ax * ax + ay * ay + (ax * ay + ay * ax) * cos(pi / 3))
        b = sqrt(bx * bx + by * by + (bx * by + by * bx) * cos(pi / 3))
        cosin = ab / (a * b)
        angle = int(acos(cosin) * 180 / pi) * 60
        self.log.append(f'COMPASS. Angle from cell({self.x}, {self.y}) to final cell: {angle}')
        return angle

    def sonar(self):
        numb = 0
        if self.sonar_level == 0:
            main = Cell(self.x, self.y)  # клетка спереди
            ignore = Cell(self.x, self.y)  # клетка сзади
            if self.rotation == 0:
                ignore.y -= 1
                main.y += 1
            elif self.rotation == 1:
                ignore.x -= 1
                main.x += 1
            elif self.rotation == 2:
                ignore.x -= 1
                ignore.y += 1
                main.x += 1
                main.y -= 1
            elif self.rotation == 3:
                ignore.y += 1
                main.y -= 1
            elif self.rotation == 4:
                ignore.x += 1
                main.x -= 1
            elif self.rotation == 5:
                ignore.x += 1
                ignore.y -= 1
                main.x -= 1
                main.y += 1
            self.sonar_cells[self.sonar_level] = [Cell(self.x, self.y)]
            self.sonar_cells[self.sonar_level + 1] = list()
            for near_cell in get_nearby(self.sonar_cells[self.sonar_level][0]):
                if near_cell != ignore:
                    for wall in self.walls:
                        if Cell(self.x, self.y) == Cell(wall.x1, wall.y1) and near_cell == Cell(wall.x2, wall.y2) or \
                                near_cell == Cell(wall.x1, wall.y1) and Cell(self.x, self.y) == Cell(wall.x2, wall.y2):
                            numb += 1
                            self.sonar_forbitten_cells.append(near_cell)
                        else:
                            if near_cell in self.map:
                                self.sonar_cells[self.sonar_level + 1].append(near_cell)
                                if near_cell == main and near_cell == self.finish_cell:  # если клетка спереди финишная, то блокируем сонар (значение больше или равно 20)
                                    numb += 20
                            else:
                                numb += 1  # добавление краёв карты
            self.log.append(f'SONAR. From cell({self.x}, {self.y}) with sonar level={self.sonar_level}: walls count={numb}')
            self.sonar_level += 1
            return numb
        else:
            self.sonar_cells[self.sonar_level + 1] = list()
            for cell in self.sonar_cells[self.sonar_level]:
                for near_cell in get_nearby(cell):
                    for wall in self.walls:
                        if Cell(cell.x, cell.y) == Cell(wall.x1, wall.y1) and near_cell == Cell(wall.x2, wall.y2) or \
                                near_cell == Cell(wall.x1, wall.y1) and Cell(cell.x, cell.y) == Cell(wall.x2, wall.y2):
                            numb += 1
                            self.sonar_forbitten_cells.append(near_cell)
                        else:
                            if (near_cell in self.map) and \
                                    (near_cell not in self.sonar_cells[self.sonar_level + 1]) and \
                                    (near_cell not in self.sonar_cells[self.sonar_level]) and \
                                    (near_cell not in self.sonar_cells[self.sonar_level - 1]) and \
                                    (near_cell not in self.sonar_forbitten_cells):
                                self.sonar_cells[self.sonar_level + 1].append(near_cell)
                            elif near_cell not in self.sonar_cells[self.sonar_level - 1] and \
                                    (near_cell not in self.sonar_forbitten_cells):
                                numb += 1  # добавление краёв карты
            self.log.append(f'SONAR. From cell({self.x}, {self.y}) with sonar level={self.sonar_level}: walls count={numb}')
            self.sonar_level += 1
            return numb

def get_nearby(cell):
    ret = list()
    ret.append(Cell(cell.x, cell.y + 1))
    ret.append(Cell(cell.x + 1, cell.y))
    ret.append(Cell(cell.x + 1, cell.y - 1))
    ret.append(Cell(cell.x, cell.y - 1))
    ret.append(Cell(cell.x - 1, cell.y))
    ret.append(Cell(cell.x - 1, cell.y + 1))
    return ret


if __name__ == '__main__':
    map_, walls, finish, r = convert('robo_data/example1.json')
    robot = Robot(r['x'], r['y'], r['rotation'], map_, walls, finish)
    robot.sonar()
    robot.sonar()
    robot.compass()
    robot.go()
    robot.rl()
    robot.rl()
    robot.go()
    print(robot)
