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
            Choice("4) Wrap ETH", wrap_eth),
            Choice("5) Unwrap ETH", unwrap_eth),
            Choice("6) Make swap on SyncSwap", swap_syncswap),
            Choice("7) Add liquidity on SyncSwap", liquidity_syncswap),
            Choice("8) Make swap on Mute", swap_mute),
            Choice("9) Make swap on Space.fi", swap_spacefi),
            Choice("10) Add liquidity on Space.fi", liquidity_spacefi),
            Choice("11) Make swap on PancakeSwap", swap_pancake),
            Choice("12) Make swap on WooFi", swap_woofi),
            Choice("13) Make swap on Velocore", swap_velocore),
            Choice("14) Make bungee refuel", bungee_refuel),
            Choice("15) Send message L2Telegraph", send_message),
            Choice("16) Mint and bridge NFT L2Telegraph", bridge_nft),
            Choice("17) Mint NFT", mint_nft),
            Choice("18) Deploy contract and mint token", deploy_contract_zksync),
            Choice("19) Dmail sending mail", send_mail),
            Choice("20) Multiswap", swap_multiswap),
            Choice("21) Stargate bridge MAV", stargate_bridge),
            Choice("22) Use custom routes", custom_routes),
            Choice("23) Check transaction count", "tx_checker"),
            Choice("24) Exit", "exit"),
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
def run_module(module, key, proxy):
    module(key, proxy)


def main(module):
    if RANDOM_WALLET:
        random.shuffle(ACCOUNTS)

    for j, key in enumerate(ACCOUNTS):
        proxy = get_proxy() if USE_PROXY else None

        run_module(module, key, proxy)

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
