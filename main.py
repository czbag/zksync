import random
import sys

import questionary
from loguru import logger
from questionary import Choice

from config import ACCOUNTS, PROXIES
from utils.get_proxy import check_proxy
from utils.sleeping import sleep
from utils.gas_checker import check_gas
from settings import *


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
            Choice("14) Make swap on Odos", swap_odos),
            Choice("15) Make swap on ZkSwap", swap_zkswap),
            Choice("16) Make swap on XYSwap", swap_xyswap),
            Choice("17) Make bungee refuel", bungee_refuel),
            Choice("18) Stargate bridge MAV", stargate_bridge),
            Choice("19) Deposit Eralend", deposit_eralend),
            Choice("20) Withdraw Eralend", withdraw_erlaned),
            Choice("21) Enable collateral on Eralend", enable_collateral_eralend),
            Choice("22) Disable collateral on Eralend", disable_collateral_eralend),
            Choice("23) Deposit Basilisk", deposit_basilisk),
            Choice("24) Withdraw Basilisk", withdraw_basilisk),
            Choice("25) Enable collateral on Basilisk", enable_collateral_basilisk),
            Choice("26) Disable collateral on Basilisk", disable_collateral_basilisk),
            Choice("27) Deposit ReactorFusion", deposit_reactorfusion),
            Choice("28) Withdraw ReactorFusion", withdraw_reactorfusion),
            Choice("29) Enable collateral on ReactorFusion", enable_collateral_reactorfusion),
            Choice("30) Disable collateral on ReactorFusion", disable_collateral_reactorfusion),
            Choice("31) Create NFT collection on Omnisea", create_omnisea),
            Choice("32) Mint and bridge NFT L2Telegraph", bridge_nft),
            Choice("33) Mint Tavaera ID + NFT", mint_tavaera),
            Choice("34) Mint NFT", mint_nft),
            Choice("35) Mint ZKS Domain", mint_zks_domain),
            Choice("36) Mint Era Domain", mint_era_domain),
            Choice("37) Send message L2Telegraph", send_message),
            Choice("38) Dmail sending mail", send_mail),
            Choice("39) MultiSwap", swap_multiswap),
            Choice("40) Use custom routes", custom_routes),
            Choice("41) MultiApprove", multi_approve),
            Choice("42) Deploy contract and mint token", deploy_contract_zksync),
            Choice("43) Check transaction count", "tx_checker"),
            Choice("44) Exit", "exit"),
        ],
        qmark="⚙️ ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        print("\n❤️ Subscribe to me – https://t.me/sybilwave\n")
        print("🤑 Donate me: 0x00000b0ddce0bfda4531542ad1f2f5fad7b9cde9")
        sys.exit()
    return result


def get_wallets():
    if USE_PROXY:
        account_with_proxy = dict(zip(ACCOUNTS, PROXIES))

        wallets = [
            {
                "id": _id,
                "key": key,
                "proxy": account_with_proxy[key]
            } for _id, key in enumerate(account_with_proxy, start=1)
        ]
    else:
        wallets = [
            {
                "id": _id,
                "key": key,
                "proxy": None
            } for _id, key in enumerate(ACCOUNTS, start=1)
        ]
    return wallets


@check_gas
def run_module(module, account_id, key, proxy):
    module(account_id, key, proxy)


def main(module):
    wallets = get_wallets()

    if RANDOM_WALLET:
        random.shuffle(wallets)

    for account in wallets:
        if account["proxy"]:
            logger.info(f"Trying to connect to the proxy [{account['proxy']}]")

            result = check_proxy(account["proxy"])

            if result is False:
                logger.error(f"Proxy error - {account['proxy']}")
                continue

            logger.success(f"Proxy [{account['proxy']}] is available")

        run_module(module, account["id"], account["key"], account["proxy"])

        if account != wallets[-1] and IS_SLEEP:
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
