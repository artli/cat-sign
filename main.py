import asyncio
import requests
import sys
import os
from wled import WLED
from mapping import change_to_working_dir, REGIONS_FILE, region_bounds_by_name_from_json, TO_UPLOAD


FIRST_REGION_ID = 10


async def write_segment(client, id, name, bounds):
    start, stop = bounds
    await client.segment(segment_id=id, start=start, stop=stop)


async def test(args) -> None:
    addr, = args
    change_to_working_dir()
    with open(REGIONS_FILE) as f:
        region_bounds_by_name = region_bounds_by_name_from_json(f.read())

    async with WLED(addr) as client:
        device = await client.update()
        print('Connected;', device.info.version)
        for i, (region_name, bounds) in enumerate(region_bounds_by_name.items()):
            region_id = FIRST_REGION_ID + i
            print(f'Pushing {region_name} (id={region_id})')
            await write_segment(
                client,
                id=region_id,
                name=region_name,
                bounds=bounds)


def upload_file(*, addr, fn, remote_fn: str):
    if not remote_fn.startswith('/'):
        raise ValueError('remote filename must start with a slash', remote_fn)
    with open(fn, mode='rb') as f:
        resp = requests.post(f'http://{addr}/edit', files={'data': (remote_fn, f)})
    resp.raise_for_status()


# def reboot


def upload_file_cmd(args):
    addr, fn, remote_fn = args
    upload_file(addr=addr, fn=fn, remote_fn=remote_fn)


def upload(args):
    addr, *dir = args
    if dir:
        dir = dir[0]
    else:
        dir = 'cat'
    os.chdir(dir)
    for standard_fn in TO_UPLOAD:
        print(f'Uploading {standard_fn}')
        upload_file(addr=addr, fn=standard_fn, remote_fn='/' + standard_fn)


if __name__ == "__main__":
    cmd = sys.argv[1]
    args = sys.argv[2:]
    if cmd == "test":
        asyncio.run(test(args))
    elif cmd == "upload-file":
        upload_file_cmd(args)
    elif cmd == "upload":
        upload(args)
    else:
        raise ValueError('unknown cmd', cmd)
