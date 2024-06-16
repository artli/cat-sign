from dataclasses import dataclass
import json
import sys


@dataclass
class CatParams:
    column_heights: [int]


def main():
    cat_params_json = json.load(sys.stdin)
    cat_params = CatParams(**cat_params_json)
    print(cat_params)


if __name__ == '__main__':
    main()
