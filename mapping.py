import dataclasses
from dataclasses import dataclass, field
from functools import cached_property
from typing import Dict, List, Optional, Tuple
from presets import cat_preset, presets_with_defaults
import bisect
import json
import os
import sys


FLIPPED_REGIONS = {'left-eye', 'right-ear'}


@dataclass
class GridSize:
    width: int
    height: int


@dataclass
class Coord:
    col: int
    row: int


@dataclass
class FilledMapping:
    map: [int]

    def json(self):
        return json.dumps(
            dataclasses.asdict(self),
            indent=None,
            separators=(',', ':'))


@dataclass
class Mapping:
    map: [int]

    def fill(self, grid_size: GridSize) -> FilledMapping:
        grid_length = grid_size.width * grid_size.height
        assert len(self.map) == grid_length
        next_unfilled = max(self.map) + 1
        filled = []
        for led in self.map:
            if led == -1:
                led = next_unfilled
                next_unfilled += 1
            filled.append(led)
        assert next_unfilled == grid_length, f'{next_unfilled} != {grid_length}'
        return FilledMapping(map=filled)


@dataclass
class MappingWithRegions1D:
    map: [int]
    region_bounds_by_name: Dict[str, Tuple[int, int]]

    def filled_mapping(self):
        return FilledMapping(map=self.map)

    @classmethod
    def default(cls, led_count: int):
        return cls(
            map=list(range(led_count)),
            region_bounds_by_name={})


@dataclass
class Region:
    id: int
    by_column: Dict[int, Tuple[int, int]]
    name: Optional[str] = None

    @classmethod
    def from_json_items(cls, *,
                        id: int, name: Optional[str] = None,
                        by_column: Dict[str, List[int]]) -> 'Region':
        by_column_mapped = {}
        for k, v in by_column.items():
            start, end = v
            by_column_mapped[int(k)] = start, end
        return cls(id=id, name=name, by_column=by_column_mapped)

    @property
    def name_or_id(self) -> str:
        if self.name is None:
            return str(self.id)
        return self.name


@dataclass
class CatParams:
    column_heights: [int]
    regions_1d: [Region] = field(default_factory=list)
    first_column_flipped: bool = False

    @classmethod
    def from_json_items(cls, *, column_heights, regions_1d=None, first_column_flipped=False):
        if regions_1d is None:
            regions_1d = []
        return cls(
            column_heights=column_heights,
            regions_1d=[
                Region.from_json_items(id=id, **region)
                for id, region in enumerate(regions_1d)],
            first_column_flipped=bool(first_column_flipped))

    @cached_property
    def led_count(self) -> int:
        return sum(self.column_heights)

    @cached_property
    def grid_size(self) -> GridSize:
        return GridSize(
            width=len(self.column_heights),
            height=max(self.column_heights))

    @cached_property
    def padding_lengths(self) -> [(int, int)]:
        padding = [self.grid_size.height - col_height for col_height in self.column_heights]
        return padding

    def region_1d_by_id(self, id: int) -> Region:
        return self.regions_1d[id]


def basic_padding(padding_lengths: [int]):
    return [(0, length) for length in padding_lengths]


class PaddedCat:
    params: CatParams
    padding: [(int, int)]

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

    def _in_range(self, led: int):
        return 0 <= led < self.params.led_count

    def coord(self, led: int) -> Coord:
        assert self._in_range(led)
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

    def grid_mapping(self) -> Mapping:
        return Mapping(map=[
            self.led(Coord(col=col, row=row))
            for col in range(self.params.grid_size.width)
            for row in range(self.params.grid_size.height)])

    def filled_grid_mapping(self) -> FilledMapping:
        return self.grid_mapping().fill(self.params.grid_size)

    @staticmethod
    def _invert(map):
        new_map = [None] * len(map)
        for i, el in enumerate(map):
            new_map[el] = i
        assert None not in new_map
        return new_map

    SAFETY_BUFFER = 0

    def region_mapping_1d(self) -> MappingWithRegions1D:
        all_leds = set(range(self.params.led_count))
        region_leds_by_id = {}
        for region in self.params.regions_1d:
            region_leds = region_leds_by_id.setdefault(region.id, set())
            for column, (start, end) in region.by_column.items():
                column_height = self.params.column_heights[column]
                flip_column = (column % 2 == 0) == self.params.first_column_flipped
                for led_in_column in range(start, end + 1):
                    if flip_column:
                        led_in_column = column_height - 1 - led_in_column
                    led = self._column_starts[column] + led_in_column
                    assert self._in_range(led)
                    region_leds.add(led)
            if not region_leds.issubset(all_leds):
                raise ValueError(
                    f'Region {region.name_or_id} intersects with some other region by {all_leds - region_leds}')
            all_leds.difference_update(region_leds)

        assert (len(all_leds) >= self.SAFETY_BUFFER)
        split_main_segment_at = len(all_leds) - self.SAFETY_BUFFER
        map = sorted(all_leds)[:split_main_segment_at]
        # region_total_size = sum(len(v) for v in region_leds_by_id.values())
        total = len(map)
        region_bounds_by_name = []
        for id, leds in reversed(region_leds_by_id.items()):
            region = self.params.region_1d_by_id(id)
            start = total
            leds = sorted(leds)
            if region.name_or_id in FLIPPED_REGIONS:
                leds.reverse()
            map.extend(leds)
            total += len(leds)
            end = total
            region_bounds_by_name.append((region.name_or_id, (start, end)))
        map.extend(sorted(all_leds)[split_main_segment_at:])
        return MappingWithRegions1D(map=map, region_bounds_by_name=dict(reversed(region_bounds_by_name)))


def print_all_coords_for_testing(cat: PaddedCat):
    for led in range(cat.params.led_count):
        print(f'{led:4d}', cat.coord(led))


def print_mapping_for_testing(cat: PaddedCat):
    for led in cat.mapping().map:
        print(led)


def LEDMAP_FILE(n):
    return f'ledmap{n}.json'


PARAMS_FILE = 'cat.json'
REGIONS_FILE = 'regions.json'
PRESETS_FILE = 'presets.json'

DEFAULT_LEDMAP_ID = 1
CAT_LEDMAP_ID = 2
TO_UPLOAD = LEDMAP_FILE(DEFAULT_LEDMAP_ID), LEDMAP_FILE(CAT_LEDMAP_ID), PRESETS_FILE
CAT_PRESET_ID = 10


def working_dir(argv):
    if len(argv) < 2:
        return 'cat'
    return argv[1]


def change_to_working_dir():
    os.chdir(working_dir(sys.argv))


def region_bounds_by_name_to_json(region_bounds_by_name):
    return json.dumps(region_bounds_by_name)


def region_bounds_by_name_from_json(json_str):
    result = {}
    for k, v in json.loads(json_str).items():
        start, end = v
        result[k] = start, end
    return result


def main():
    change_to_working_dir()
    with open(PARAMS_FILE) as f:
        cat_params = CatParams.from_json_items(**json.load(f))
    padded_cat = PaddedCat.from_basic_padding(cat_params)
    region_mapping_1d = padded_cat.region_mapping_1d()
    with open(LEDMAP_FILE(DEFAULT_LEDMAP_ID), 'w') as f:
        f.write(MappingWithRegions1D.default(cat_params.led_count).filled_mapping().json() + '\n')
    with open(LEDMAP_FILE(CAT_LEDMAP_ID), 'w') as f:
        f.write(region_mapping_1d.filled_mapping().json() + '\n')
    with open(REGIONS_FILE, 'w') as f:
        f.write(region_bounds_by_name_to_json(region_mapping_1d.region_bounds_by_name) + '\n')
    presets = presets_with_defaults({
        str(CAT_PRESET_ID): cat_preset(region_mapping_1d, led_map=2)})
    with open(PRESETS_FILE, 'w') as f:
        f.write(json.dumps(
            presets,
            indent=None,
            separators=(',', ':')
        ) + '\n')


if __name__ == '__main__':
    main()
