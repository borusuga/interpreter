import json
import os.path

from d_classes.Cell import *


def convert(file: str) -> tuple:
    """
    Convert .json file to map and robot initial data tuple
    Raises:
        FileNotFoundError
    """
    if os.path.isfile(file):
        with open(file, "r") as f:
            data = json.load(f)
            map_json_data = data["map"]
            robot_json_data = data["robot"]
            walls_json_data = data["walls"]
            map_list = map_from_json(map_json_data)
            walls_list = walls_from_json(walls_json_data)
            finish_cell = Cell(data["finish"]["x"], data["finish"]["y"])
            return map_list, walls_list, finish_cell, robot_json_data
    else:
        raise FileNotFoundError


def map_from_json(data: list) -> list:
    """
    Raises:
        ValueError
    """
    ret = list()
    try:
        for pair in data:
            x = int(pair['x'])
            y = int(pair['y'])
            ret.append(Cell(x, y))
    except:
        raise ValueError
    return ret


def walls_from_json(data: list):
    ret = list()
    for coords in data:
        ret.append(Wall(int(coords['x1']),
                        int(coords['y1']),
                        int(coords['x2']),
                        int(coords['y2'])))
    return ret


if __name__ == '__main__':
    filename = 'robo_data/example1.json'
    convert(filename)
