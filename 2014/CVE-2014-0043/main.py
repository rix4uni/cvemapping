import aiohttp
import asyncio
import argparse
from zipfile import ZipFile
import os
from click import Argument
import requests
import random

def get_classes(jar_file):
    with ZipFile(jar_file) as zip:
        for name in zip.namelist():
            if not name.endswith('.class'):
                continue
            yield name.replace('/', '.')[:-6]


def get_cookies():
    if not 'cookie' in os.environ:
        return None
    cookies = {}
    for c in os.environ['cookie'].split(';'):
        key, _, value = c.partition('=')
        cookies[key.strip()]=value
    return cookies


async def test_class(session, base_url, classname):
    global tested, present
    async with session.get(f"{base_url}/{classname}/", allow_redirects=False, headers={
        "Cookie": os.environ.get('cookie')
    }) as resp:
        if 'Location' in resp.headers and resp.headers['Location'].startswith('https://login.microsoftonline.com'):
            print("Unauthorized")
            return
        tested += 1
        if resp.status == 404:
            status = "N"
        elif resp.status == 302:
            status = "Y"
            present += 1
        else:
            status = f"?, {resp.status}"
        return status, classname, resp

tested = 0
present = 0

async def test_classes(input_file, sample_size=None):
    global tested, present
    tested = 0
    present = 0
    async with aiohttp.ClientSession() as session:
        classes = list(get_classes(args.input_file))
        if sample_size:
            classes = random.sample(classes, sample_size)
        present = 0
        for c in classes:
            yield await test_class(session, base_url, c)

base_url = "https://example.com/wicket/resource/"


async def main(args):
    if args.input_file:
        async for status, c, _ in test_classes(args.input_file, sample_size=args.sample_size):
            print(status, c)
        percentage = present*100/tested
        print(f"Tested: {tested}, Present: {present} ({percentage})")
    elif args.string:
        async with aiohttp.ClientSession() as session:
            status, c, _ = await test_class(session, base_url, args.string)
            print(status, c)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-i", "--input_file")
    parser.add_argument("-s", "--sample-size", type=int)
    parser.add_argument("--string")
    args = parser.parse_args()

    asyncio.run(main(args))
