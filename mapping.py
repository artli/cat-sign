from dataclasses import dataclass
from functools import cached_property
import bisect
import json
import sys


@dataclass
class GridSize:
    width: int
    height: int


@dataclass
class Coord:
    col: int
    row: int


@dataclass
class CatParams:
    column_heights: [int]

    @cached_property
    def led_count(self):
        return sum(self.column_heights)

    @cached_property
    def grid_size(self):
        return GridSize(
            width=len(self.column_heights),
            height=max(self.column_heights))

    @cached_property
    def padding_lengths(self):
        padding = [self.grid_size.height - col_height for col_height in self.column_heights]
        return padding


def basic_padding(padding_lengths : [int]):
    return [(0, length) for length in padding_lengths]


class PaddedCat:
    params : CatParams
    padding : [(int, int)]

    def __init__(self, cat_params, padding):
        self.params = cat_params
        self.padding = padding

    @classmethod
    def from_basic_padding(cls, cat_params):
        return cls(cat_params, basic_padding(cat_params.padding_lengths))

    @cached_property
    def _shifts(self):
        result = []
        shift = 0
        for top, bottom in self.padding:
            shift += top
            result.append(shift)
            shift += bottom
        return result

    @cached_property
    def _column_starts(self):
        starts = []
        total = 0
        for height in self.params.column_heights:
            starts.append(total)
            total += height
        return starts

    def coord(self, led: int) -> Coord:
        assert 0 <= led < self.params.led_count
        col = bisect.bisect_right(self._column_starts, led) - 1
        start = self._column_starts[col]
        row = led - start + self.padding[col][0]
        return Coord(row=row, col=col)

    def led(self, coord: Coord) -> int:
        start = self._column_starts[coord.col]
        top, bottom = self.padding[coord.col]
        if top <= coord.row < (self.params.grid_size.height - bottom):
            return start + coord.row
        return -1

    def mapping(self):
        return [
            self.led(Coord(col=col, row=row))
            for col in range(self.params.grid_size.width)
            for row in range(self.params.grid_size.height)]


def print_all_coords_for_testing(cat: PaddedCat):
    for led in range(cat.params.led_count):
        print(f'{led:4d}', cat.coord(led))


def print_mapping_for_testing(cat: PaddedCat):
    for led in cat.mapping():
        print(led)


def main():
    cat_params = CatParams(**json.load(sys.stdin))
    padded_cat = PaddedCat.from_basic_padding(cat_params)
    print_all_coords_for_testing(padded_cat)
    print('===')
    print_mapping_for_testing(padded_cat)


if __name__ == '__main__':
    main()
