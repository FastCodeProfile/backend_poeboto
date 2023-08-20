import asyncio
import json
import os

import httpx


async def upload_bots():
    host = "http://127.0.0.1:8000/api/v1/bots/new"
    workdir = "./bots/"
    sessions = os.listdir(workdir)
    for session in sessions:
        with open(workdir + session, "r", encoding="utf-8") as f:
            session_json = json.load(f)

        async with httpx.AsyncClient() as client:
            res = await client.post(
                host,
                json={
                    "api_id": session_json["app_id"],
                    "api_hash": session_json["app_hash"],
                    "password": session_json["twoFA"],
                    "lang_code": session_json["lang_pack"],
                    "app_version": session_json["app_version"],
                    "device_model": session_json["device"],
                    "session_string": session_json["string"],
                },
            )

            print(res.text)


asyncio.run(upload_bots())
