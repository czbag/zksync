import random
import sys

import questionary
from questionary import Choice

from config import ACCOUNTS
from utils.gas_checker import check_gas
from utils.get_proxy import get_proxy
from settings import *
from utils.sleeping import sleep


def get_module():
    result = questionary.select(
        "Select a method to get started",
        choices=[
            Choice("1) Make bridge ZkSync", bridge_zksync),
            Choice("2) Make withdraw from ZkSync", withdraw_zksync),
            Choice("3) Make bridge on Orbiter", bridge_orbiter),
            Choice("4) Make swap on SyncSwap", swap_syncswap),
            Choice("5) Add liquidity on SyncSwap", liquidity_syncswap),
            Choice("6) Make swap on Mute", swap_mute),
            Choice("7) Make swap on Space.fi", swap_spacefi),
            Choice("8) Add liquidity on Space.fi", liquidity_spacefi),
            Choice("9) Make swap on PancakeSwap", swap_pancake),
            Choice("10) Make swap on WooFi", swap_woofi),
            Choice("11) Make swap on Velocore", swap_velocore),
            Choice("12) Make bungee refuel", bungee_refuel),
            Choice("13) Send message L2Telegraph", send_message),
            Choice("14) Mint and bridge NFT L2Telegraph", bridge_nft),
            Choice("15) Mint NFT", mint_nft),
            Choice("16) Deploy contract and mint token", deploy_contract_zksync),
            Choice("17) Dmail sending mail", send_mail),
            Choice("18) Multiswap", swap_multiswap),
            Choice("19) Stargate bridge MAV", stargate_bridge),
            Choice("20) Use custom routes", custom_routes),
            Choice("21) Check transaction count", "tx_checker"),
            Choice("22) Exit", "exit"),
        ],
        qmark="🛠 ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        print("\n❤️ Subscribe to me – https://t.me/sybilwave\n")
        print("🤑 Donate me: 0x00000b0ddce0bfda4531542ad1f2f5fad7b9cde9")
        sys.exit()
    return result


@check_gas
def main(module):
    proxy = get_proxy() if USE_PROXY else None

    if RANDOM_WALLET:
        random.shuffle(RANDOM_WALLET)

    for j, key in enumerate(ACCOUNTS):
        module(key, proxy)
        if j + 1 < len(ACCOUNTS) and IS_SLEEP:
            sleep(SLEEP_FROM, SLEEP_TO)


if __name__ == '__main__':
    print("❤️ Subscribe to me – https://t.me/sybilwave\n")

    module = get_module()
    if module == "tx_checker":
        get_tx_count()
    else:
        main(module)

    print("\n❤️ Subscribe to me – https://t.me/sybilwave\n")
    print("🤑 Donate me: 0x00000b0ddce0bfda4531542ad1f2f5fad7b9cde9")
