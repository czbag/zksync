import random
import sys
import time

import questionary
from questionary import Choice
from config import *

from settings import *
from utils.gas_cheker import wait_gas
from utils.get_proxy import get_proxy


def get_module():
    result = questionary.select(
        "Select a method to get started",
        choices=[
            Choice("Make bridge ZkSync", "bridge_zksync"),
            Choice("Make withdraw from ZkSync", "withdraw_zksync"),
            Choice("Make bridge on Orbiter", "bridge_orbiter"),
            Choice("Make swap on SyncSwap", "swap_syncswap"),
            Choice("Make swap on Mute", "swap_mute"),
            Choice("Make swap on Space.fi", "swap_spacefi"),
            Choice("Make swap on PancakeSwap", "swap_pancake"),
            Choice("Mint NFT", "mint_nft"),
            Choice("Deploy contract and mint token", "deploy_contract"),
            Choice("Dmail sending mail", "send_mail"),
            Choice("Use custom routes", "use_routes"),
            Choice("Exit", "exit"),
        ],
        qmark="🛠 ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        sys.exit(1)
    return result


def start_module(module, key, proxy):
    if module == "bridge_zksync":
        bridge_zksync(key, proxy)
    elif module == "withdraw_zksync":
        withdraw_zksync(key, proxy)
    elif module == "bridge_orbiter":
        bridge_orbiter(key, proxy)
    elif module == "swap_syncswap":
        swap_syncswap(key, proxy)
    elif module == "swap_mute":
        swap_mute(key, proxy)
    elif module == "swap_spacefi":
        swap_spacefi(key, proxy)
    elif module == "swap_pancake":
        swap_pancake(key, proxy)
    elif module == "deploy_contract":
        deploy_contract_zksync(key, proxy)
    elif module == "send_mail":
        dmail = Dmail(key, proxy)
        dmail.send_mail()
    elif module == "mint_nft":
        mint_nft = Minter(key, proxy)
        mint_nft.mint()


def main(module, key):
    proxy = None
    if USE_PROXY:
        proxy = get_proxy()
    if CHECK_GWEI:
        wait_gas()
    start_module(module, key, proxy)


if __name__ == '__main__':
    print("\n\nSubscribe to me –– https://t.me/sybilwave\n")

    module = get_module()

    if RANDOM_WALLET:
        random.shuffle(ACCOUNTS)

    if RANDOM_ROUTES:
        random.shuffle(ROUTES)

    for j, key in enumerate(ACCOUNTS):
        if module == "use_routes":
            for route in ROUTES:
                main(route, key)
                time.sleep(random.randint(ROUTE_SLEEP_FROM, ROUTE_SLEEP_TO))
        else:
            main(module, key)

        if j + 1 < len(ACCOUNTS) and IS_SLEEP:
            time.sleep(random.randint(SLEEP_FROM, SLEEP_TO))

    print("\n\nSubscribe to me –– https://t.me/sybilwave")
