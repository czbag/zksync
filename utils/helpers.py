import json

from loguru import logger
from settings import RETRY_COUNT
from utils.sleeping import sleep


def retry(func):
    async def wrapper(*args, **kwargs):
        retries = 0
        while retries <= RETRY_COUNT:
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Error | {e}")
                await sleep(10, 20)
                retries += 1

    return wrapper


def get_run_accounts():
    with open("data/run_accounts.json", "r") as data:
        return json.load(data)


def update_run_accounts(_id: int, method: str):
    run_accounts = get_run_accounts()

    with open("data/run_accounts.json", "w") as data:
        try:
            if method == "add":
                run_accounts["accounts"].append(_id)
            else:
                run_accounts["accounts"].remove(_id)

            json.dump(run_accounts, data)
        except:
            new_data = {"accounts": []}
            json.dump(new_data, data)
