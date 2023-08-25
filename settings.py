import asyncio

from modules import *

# RANDOM WALLETS MODE
RANDOM_WALLET = False  # True or False

# SLEEP MODE
IS_SLEEP = True  # True or False

SLEEP_FROM = 300  # Second
SLEEP_TO = 700  # Second

# PROXY MODE
USE_PROXY = True

# GWEI CONTROL MODE
CHECK_GWEI = False  # True or False
MAX_GWEI = 20


def bridge_zksync(account_id, key, proxy):
    """
    Deposit from official bridge
    ______________________________________________________
    all_amount - Bridge 90% ETH
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    zksync = ZkSync(account_id, key, proxy, "ethereum")
    zksync.deposit(min_amount, max_amount, decimal, all_amount)


def withdraw_zksync(account_id, key, proxy):
    """
    Withdraw from official bridge
    ______________________________________________________
    all_amount - Withdraw 90% ETH
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = False

    zksync = ZkSync(account_id, key, proxy, "zksync")
    zksync.withdraw(min_amount, max_amount, decimal, all_amount)


def bridge_orbiter(account_id, key, proxy):
    """
    Bridge from orbiter
    ______________________________________________________
    from_chain – ethereum, polygon_zkevm, arbitrum, optimism, zksync | Select one
    to_chain – ethereum, polygon_zkevm, arbitrum, optimism, zksync | Select one
    """

    from_chain = "zksync"
    to_chain = "ethereum"

    min_amount = 1
    max_amount = 3
    decimal = 4

    orbiter = Orbiter(account_id, key, from_chain, proxy)
    orbiter.bridge(to_chain, min_amount, max_amount, decimal)


def wrap_eth(account_id, key, proxy):
    """
    Wrap ETH
    ______________________________________________________
    all_amount True - wrap 90% ETH
    """
    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = False

    zksync = ZkSync(account_id, key, proxy, "zksync")
    zksync.wrap_eth(min_amount, max_amount, decimal, all_amount)


def unwrap_eth(account_id, key, proxy):
    """
    Unwrap ETH
    ______________________________________________________
    all_amount True - unwrap 100% ETH
    """
    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    zksync = ZkSync(account_id, key, proxy, "zksync")
    zksync.unwrap_eth(min_amount, max_amount, decimal, all_amount)


def swap_syncswap(account_id, key, proxy):
    """
    Make swap on SyncSwap

    from_token – Choose SOURCE token ETH, USDC, USDT, BUSD, MAV, OT, MATIC, WBTC | Select one
    to_token – Choose DESTINATION token ETH, USDC, USDT, BUSD, MAV, OT, MATIC, WBTC | Select one

    Disclaimer – Don't use stable coin in from and to token | from_token USDC to_token USDT DON'T WORK!!!
    ______________________________________________________
    all_amount - Swap 90% ETH or 100% ANY_TOKEN
    """

    from_token = "ETH"
    to_token = "USDC"

    min_amount = 1
    max_amount = 2
    decimal = 6
    slippage = 1

    all_amount = False

    syncswap = SyncSwap(account_id, key, proxy)
    syncswap.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount)


def liquidity_syncswap(account_id, key, proxy):
    """
    Add liqudity on SyncSwap

    amount in ETH, USDC amount not need (auto swap)
    """
    min_amount = 0.01
    max_amount = 0.02
    decimal = 6

    syncswap = SyncSwap(account_id, key, proxy)
    syncswap.add_liquidity(min_amount, max_amount, decimal)


def swap_mute(account_id, key, proxy):
    """
    Make swap on Mute
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC, WBTC | Select one
    to_token – Choose DESTINATION token ETH, USDC, WBTC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - Swap 90% ETH or 100% ANY_TOKEN
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    mute = Mute(account_id, key, proxy)
    mute.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount)


def swap_spacefi(account_id, key, proxy):
    """
    Make swap on SpaceFi
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC, USDT, BUSD, OT, MATIC, WBTC | Select one
    to_token – Choose DESTINATION token ETH, USDC, USDT, BUSD, OT, MATIC, WBTC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - Swap 90% ETH or 100% ANY_TOKEN
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    spacefi = SpaceFi(account_id, key, proxy)
    spacefi.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount)


def liquidity_spacefi(account_id, key, proxy):
    """
    Make swap on SyncSwap

    from_token – Choose SOURCE token ETH, USDC, USDT, BUSD, MAV, OT, MATIC, WBTC | Select one
    to_token – Choose DESTINATION token ETH, USDC, USDT, BUSD, MAV, OT, MATIC, WBTC | Select one

    amount in ETH, you need have usdc
    """
    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6

    spacefi = SpaceFi(account_id, key, proxy)
    spacefi.add_liquidity(min_amount, max_amount, decimal)


def swap_pancake(account_id, key, proxy):
    """
    Make swap on PancakeSwap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - Swap 90% ETH or 100% ANY_TOKEN
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.001
    max_amount = 0.002
    decimal = 6
    slippage = 1

    all_amount = True

    pancake = Pancake(account_id, key, proxy)
    pancake.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount)


def swap_woofi(account_id, key, proxy):
    """
    Make swap on WooFi
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one
    ______________________________________________________
    all_amount - Swap 90% ETH or 100% ANY_TOKEN
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    woofi = WooFi(account_id, key, proxy)
    woofi.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount)


def swap_velocore(account_id, key, proxy):
    """
    Make swap on Velocore
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC, BUSD, WBTC | Select one
    to_token – Choose DESTINATION token ETH, USDC, BUSD, WBTC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - Swap 90% ETH or 100% ANY_TOKEN
    """

    from_token = "ETH"
    to_token = "USDC"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = False

    velocore = Velocore(account_id, key, proxy)
    velocore.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount)


def bungee_refuel(account_id, key, proxy):
    """
    Make refuel on Bungee
    ______________________________________________________
    to_chain – Choose DESTINATION chain: BSC, OPTIMISM, GNOSIS, POLYGON, BASE, ARBITRUM, AVALANCHE, AURORA, ZK_EVM

    Disclaimer - The chain will be randomly selected
    ______________________________________________________
    random_amount – True - amount random from min to max | False - use min amount
    """

    chain_list = ["BSC", "GNOSIS", "BASE", "AURORA"]

    random_amount = False

    bungee = Bungee(account_id, key, proxy)
    bungee.refuel(chain_list, random_amount)


def stargate_bridge(account_id, key, proxy):
    """
    Make stargate MAV token bridge to BSC
    ______________________________________________________
    all_amount - Swap 90% ETH to MAV and bridge
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4
    slippage = 1

    sleep_from = 5
    sleep_to = 24

    all_amount = False

    st = Stargate(account_id, key, proxy)
    st.bridge(min_amount, max_amount, decimal, slippage, sleep_from, sleep_to, all_amount)


def bridge_nft(account_id, key, proxy):
    """
    Make mint NFT and bridge NFT on L2Telegraph
    """

    sleep_from = 5
    sleep_to = 20

    l2telegraph = L2Telegraph(account_id, key, proxy)
    l2telegraph.bridge(sleep_from, sleep_to)


def swap_multiswap(account_id, key, proxy):
    """
    Multi-Swap module: Automatically performs the specified number of swaps in one of the dexes.
    ______________________________________________________
    use_dex - Choose any dex: syncswap, mute, spacefi, pancake, woofi, velocore
    quantity_swap - Quantity swaps
    ______________________________________________________
    all_amount - If True, swap 90% ETH to USDC, after swap 100% USDC to ETH
    If False, swap 10-90% ETH to USDC, after swap USDC 10-90% to ETH remaining number of times
    """
    use_dex = ["velocore", "mute"]

    min_swap = 2
    max_swap = 4

    sleep_from = 5
    sleep_to = 10

    slippage = 1

    all_amount = True

    multi = Multiswap(account_id, key, proxy)
    multi.swap(use_dex, sleep_from, sleep_to, min_swap, max_swap, slippage, all_amount)


def deploy_contract_zksync(account_id, key, proxy):
    """
    Deploy contract token and mint
    ______________________________________________________
    token_name – Any token name
    token_symbol – Any token symbol
    ______________________________________________________
    min_mint – Amount of mint 2
    amount – Amount of mint 1000
    """
    token_name = "Test"
    token_symbol = "Test"

    min_mint = 10
    max_mint = 1000

    random_token_data = True

    zksync = ZkSync(account_id, key, proxy, "zksync")
    zksync.deploy_contract(token_name, token_symbol, min_mint, max_mint, random_token_data)


def custom_routes(account_id, key, proxy):
    """
    You can use these methods:
    bridge_zksync, withdraw_zksync, bridge_orbiter, swap_syncswap, liquidity_syncswap,
    swap_mute, swap_spacefi, liquidity_spacefi, swap_pancake, swap_woofi, swap_velocore,
    bungee_refuel, deploy_contract_zksync, send_mail, mint_nft, send_message, bridge_nft,
    swap_multiswap, stargate_bridge
    """
    use_modules = [send_mail, mint_nft, bridge_nft, send_message, bungee_refuel]

    sleep_from = 70
    sleep_to = 400

    random_module = False

    routes = Routes(account_id, key, proxy)
    routes.start(use_modules, sleep_from, sleep_to, random_module)


def multi_approve(account_id, key, proxy):
    """
    Make approve all tokens from config in SyncSwap, Mute, SpaceFi, Pancake, WooFi, Velocore

    Disclaimer - You can use 0 for cancel  approve
    """
    amount = 0

    sleep_from = 30
    sleep_to = 95

    multiapprove = MultiApprove(account_id, key, proxy)
    multiapprove.start(amount, sleep_from, sleep_to)


#########################################
########### NO NEED TO CHANGE ###########
#########################################

def send_mail(account_id, key, proxy):
    dmail = Dmail(account_id, key, proxy)
    dmail.send_mail()


def send_message(account_id, key, proxy):
    l2telegraph = L2Telegraph(account_id, key, proxy)
    l2telegraph.send_message()


def mint_nft(account_id, key, proxy):
    mint_nft = Minter(account_id, key, proxy)
    mint_nft.mint()


def get_tx_count():
    asyncio.run(check_tx())
