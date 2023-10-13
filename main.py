import random
import sys

import questionary
from loguru import logger
from questionary import Choice

from config import ACCOUNTS, PROXIES
from utils.get_proxy import check_proxy
from utils.helpers import get_run_accounts, update_run_accounts
from utils.sleeping import sleep
from settings import USE_PROXY, RANDOM_WALLET, SLEEP_FROM, SLEEP_TO, QUANTITY_RUN_ACCOUNTS
from modules_settings import *


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
            Choice("13) Make swap on Odos", swap_odos),
            Choice("14) Make swap on ZkSwap", swap_zkswap),
            Choice("15) Make swap on XYSwap", swap_xyswap),
            Choice("16) Make swap on OpenOcean", swap_openocean),
            Choice("17) Make swap on 1inch", swap_inch),
            Choice("18) Make swap on Maverick", swap_maverick),
            Choice("19) Make swap on VeSync", swap_vesync),
            Choice("20) Make bungee refuel", bungee_refuel),
            Choice("21) Stargate bridge MAV", stargate_bridge),
            Choice("22) Deposit Eralend", deposit_eralend),
            Choice("23) Withdraw Eralend", withdraw_erlaned),
            Choice("24) Enable collateral on Eralend", enable_collateral_eralend),
            Choice("25) Disable collateral on Eralend", disable_collateral_eralend),
            Choice("26) Deposit Basilisk", deposit_basilisk),
            Choice("27) Withdraw Basilisk", withdraw_basilisk),
            Choice("28) Enable collateral on Basilisk", enable_collateral_basilisk),
            Choice("29) Disable collateral on Basilisk", disable_collateral_basilisk),
            Choice("30) Deposit ReactorFusion", deposit_reactorfusion),
            Choice("31) Withdraw ReactorFusion", withdraw_reactorfusion),
            Choice("32) Enable collateral on ReactorFusion", enable_collateral_reactorfusion),
            Choice("33) Disable collateral on ReactorFusion", disable_collateral_reactorfusion),
            Choice("34) Deposit ZeroLend", deposit_zerolend),
            Choice("35) Withdraw ZeroLend", withdraw_zerolend),
            Choice("36) Create NFT collection on Omnisea", create_omnisea),
            Choice("37) Mint and bridge NFT L2Telegraph", bridge_nft),
            Choice("38) Mint Tavaera ID + NFT", mint_tavaera),
            Choice("39) Mint MailZero NFT", mint_mailzero_nft),
            Choice("40) Mint NFT on NFTS2ME", mint_nft),
            Choice("41) Mint ZKS Domain", mint_zks_domain),
            Choice("42) Mint Era Domain", mint_era_domain),
            Choice("43) Send message L2Telegraph", send_message),
            Choice("44) Dmail sending mail", send_mail),
            Choice("45) Create gnosis safe", create_safe),
            Choice("46) Swap tokens to ETH", swap_tokens),
            Choice("47) MultiSwap", swap_multiswap),
            Choice("48) Use custom routes", custom_routes),
            Choice("49) MultiApprove", multi_approve),
            Choice("50) Check transaction count", "tx_checker"),
            Choice("51) Exit", "exit"),
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


async def run_module(module, account_id, key, proxy, sleep_time, start_id):
    if start_id != 1:
        await asyncio.sleep(sleep_time)

    while True:
        run_accounts = get_run_accounts()

        if len(run_accounts["accounts"]) < QUANTITY_RUN_ACCOUNTS:
            update_run_accounts(account_id, "add")

            await module(account_id, key, proxy)

            update_run_accounts(account_id, "remove")

            break
        else:
            logger.info(f'Current run accounts: {len(run_accounts["accounts"])}')
            await asyncio.sleep(60)


async def main(module):
    wallets = get_wallets()

    tasks = []

    if RANDOM_WALLET:
        random.shuffle(wallets)

    sleep_time = random.randint(SLEEP_FROM, SLEEP_TO)

    for _, account in enumerate(wallets, start=1):
        tasks.append(asyncio.create_task(
            run_module(module, account["id"], account["key"], account["proxy"], sleep_time, _)
        ))

        sleep_time += random.randint(SLEEP_FROM, SLEEP_TO)

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    print("❤️ Subscribe to me – https://t.me/sybilwave\n")

    module = get_module()
    if module == "tx_checker":
        get_tx_count()
    else:
        asyncio.run(main(module))

    print("\n❤️ Subscribe to me – https://t.me/sybilwave\n")
    print("🤑 Donate me: 0x00000b0ddce0bfda4531542ad1f2f5fad7b9cde9")
