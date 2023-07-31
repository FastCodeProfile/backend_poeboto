import asyncio
import json
import os

import httpx


async def upload_proxies():
    host = "http://127.0.0.1:8000/api/v1/proxies/add_proxy"
    workdir = "./proxies/"
    proxies = os.listdir(workdir)
    for proxy in proxies:
        with open(workdir + proxy, "r", encoding="utf-8") as f:
            proxy_json = json.load(f)

        async with httpx.AsyncClient() as client:
            res = await client.post(
                host,
                json={
                    "scheme": proxy_json["scheme"],
                    "rotation_url": proxy_json["rotation_url"],
                    "ip": proxy_json["ip"],
                    "port": proxy_json["port"],
                    "username": proxy_json["username"],
                    "password": proxy_json["password"],
                },
            )

            print(res.text)


asyncio.run(upload_proxies())
