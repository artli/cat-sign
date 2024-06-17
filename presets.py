import json
import copy
from typing import Optional
import random


DEFAULT_PRESETS = json.loads('''
{"0":{},"1":{"n":"Default","ledmap":1,"on":true,"bri":128,"inputLevel":128,"transition":7,"mainseg":0,"seg":[{"id":0,"start":0,"stop":300,"grp":1,"spc":0,"of":0,"on":true,"frz":false,"bri":255,"cct":127,"col":[[255,48,62],[158,195,255],[198,255,173]],"fx":9,"sx":128,"ix":24,"c1x":128,"c2x":128,"c3x":128,"pal":0,"sel":true,"rev":false,"rev2D":false,"mi":false,"rot2D":false},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0}]},"2":{"n":"Sound Reactive","on":true,"bri":128,"inputLevel":219,"transition":7,"mainseg":0,"seg":[{"id":0,"start":0,"stop":300,"grp":1,"spc":0,"of":0,"on":true,"frz":false,"bri":255,"cct":127,"col":[[255,48,62],[0,0,0],[0,0,0]],"fx":158,"sx":250,"ix":128,"c1x":192,"c2x":192,"c3x":192,"pal":11,"sel":true,"rev":false,"rev2D":false,"mi":false,"rot2D":false},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0}]},"250":{"n":"~ 06-16 19:55:27 ~","on":true,"bri":255,"inputLevel":219,"transition":7,"mainseg":0,"seg":[{"id":0,"start":0,"stop":898,"grp":1,"spc":0,"of":0,"on":true,"frz":false,"bri":255,"cct":127,"col":[[255,25,0],[0,0,0],[0,0,0]],"fx":46,"sx":0,"ix":255,"c1x":192,"c2x":192,"c3x":192,"pal":1,"sel":true,"rev":false,"rev2D":false,"mi":false,"rot2D":false},{"id":1,"start":898,"stop":1304,"grp":1,"spc":0,"of":0,"on":true,"frz":false,"bri":255,"cct":127,"col":[[255,25,0],[0,0,0],[0,0,0]],"fx":46,"sx":0,"ix":255,"c1x":0,"c2x":0,"c3x":0,"pal":1,"sel":true,"rev":false,"rev2D":false,"mi":false,"rot2D":false},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0},{"stop":0}]}}
''')

EMPTY_SEGMENT = {
    "stop": 0
}


def fill_segments(non_empty, total=32):
    return non_empty + [EMPTY_SEGMENT] * (total - len(non_empty))


def random_color(r: random.Random):
    return [random.randint(0, 255) for _ in range(3)]


def segment(id: int, *, start: int, stop: int, name: Optional[str] = None):
    r = random.Random()
    r.seed(id + 100)
    return {
        "id": id,
        "n": name,
        "start": start,
        "stop": stop,
        "grp": 1,
        "spc": 0,
        "of": 0,
        "on": True,
        "frz": False,
        "bri": 255,
        "cct": 127,
        "col": [random_color(r) for _ in range(3)],
        "fx": 0,
        "sx": 128,
        "ix": 24,
        "c1x": 128,
        "c2x": 128,
        "c3x": 128,
        "pal": 0,
        "sel": True,
        "rev": False,
        "rev2D": False,
        "mi": False,
        "rot2D": False
    }


def preset(name: str, segments, led_map: Optional[int] = None):
    return {
        "ledmap": led_map,
        "n": name,
        "on": True,
        "bri": 128,
        "inputLevel": 219,
        "transition": 7,
        "mainseg": 0,
        "seg": fill_segments(segments)
    }


def presets_with_defaults(additional_presets_by_id):
    presets: dict = copy.deepcopy(DEFAULT_PRESETS)
    presets.update(**additional_presets_by_id)
    return presets


def cat_preset(region_mapping_1d, *, led_map: int):
    cat_segments = [segment(id=0, start=0, stop=len(region_mapping_1d.map), name="background")]
    for id, (name, (start, stop)) in enumerate(region_mapping_1d.region_bounds_by_name.items(), start=1):
        cat_segments.append(segment(id=id, start=start, stop=stop, name=name))
    cat_preset = preset('cat', cat_segments, led_map=2)
    return cat_preset
