import asyncio

from modules import *

# RANDOM WALLETS MODE
RANDOM_WALLET = False  # True or False

# SLEEP MODE
IS_SLEEP = False  # True or False

SLEEP_FROM = 5  # Second
SLEEP_TO = 5  # Second

# PROXY MODE
USE_PROXY = False

# GWEI CONTROL MODE
CHECK_GWEI = False  # True or False
MAX_GWEI = 20


def bridge_zksync(key, proxy):
    """
    Deposit from official bridge
    ______________________________________________________
    all_amount - Bridge 90% ETH
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    zksync = ZkSync(key, proxy, "ethereum")
    zksync.deposit(min_amount, max_amount, decimal, all_amount)


def withdraw_zksync(key, proxy):
    """
    Withdraw from official bridge
    ______________________________________________________
    all_amount - Withdraw 90% ETH
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = False

    zksync = ZkSync(key, proxy, "zksync")
    zksync.withdraw(min_amount, max_amount, decimal, all_amount)


def bridge_orbiter(key, proxy):
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

    orbiter = Orbiter(key, from_chain, proxy)
    orbiter.bridge(to_chain, min_amount, max_amount, decimal)


def swap_syncswap(key, proxy):
    """
    Make swap on SyncSwap

    from_token – Choose SOURCE token ETH, USDC, USDT, BUSD, MAV, OT, MATIC, WBTC | Select one
    to_token – Choose DESTINATION token ETH, USDC, USDT, BUSD, MAV, OT, MATIC, WBTC | Select one

    Disclaimer – Don't use stable coin in from and to token | from_token USDC to_token USDT DON'T WORK!!!
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

    syncswap = SyncSwap(key, proxy)
    syncswap.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount)


def liquidity_syncswap(key, proxy):
    """
    Add liqudity on SyncSwap

    amount in ETH, USDC amount not need (auto swap)
    """
    min_amount = 0.01
    max_amount = 0.02
    decimal = 6

    syncswap = SyncSwap(key, proxy)
    syncswap.add_liquidity(min_amount, max_amount, decimal)


def swap_mute(key, proxy):
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

    mute = Mute(key, proxy)
    mute.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount)


def swap_spacefi(key, proxy):
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

    spacefi = SpaceFi(key, proxy)
    spacefi.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount)


def liquidity_spacefi(key, proxy):
    """
    Make swap on SyncSwap

    from_token – Choose SOURCE token ETH, USDC, USDT, BUSD, MAV, OT, MATIC, WBTC | Select one
    to_token – Choose DESTINATION token ETH, USDC, USDT, BUSD, MAV, OT, MATIC, WBTC | Select one

    amount in ETH, you need have usdc
    """
    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6

    spacefi = SpaceFi(key, proxy)
    spacefi.add_liquidity(min_amount, max_amount, decimal)


def swap_pancake(key, proxy):
    """
    Make swap on PancakeSwap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC, USDT, BUSD, WBTC | Select one
    to_token – Choose DESTINATION token ETH, USDC, USDT, BUSD, WBTC | Select one

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

    pancake = Pancake(key, proxy)
    pancake.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount)


def swap_woofi(key, proxy):
    """
    Make swap on WooFi
    ______________________________________________________
    from_token – Choose SOURCE token ETH/USDC | Select one
    to_token – Choose DESTINATION token ETH/USDC | Select one
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

    woofi = WooFi(key, proxy)
    woofi.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount)


def swap_velocore(key, proxy):
    """
    Make swap on Velocore
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC, BUSD, WBTC | Select one
    to_token – Choose DESTINATION token ETH, USDC, BUSD, WBTC | Select one

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

    velocore = Velocore(key, proxy)
    velocore.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount)


def bungee_refuel(key, proxy):
    """
    Make refuel on Bungee
    ______________________________________________________
    to_chain – Choose DESTINATION chain: BSC, OPTIMISM, GNOSIS, POLYGON, BASE, ARBITRUM, AVALANCHE, AURORA, ZK_EVM
    ______________________________________________________
    random_amount – True - amount random from min to max | False - use min amount
    """

    to_chain = "BSC"

    random_amount = False

    bungee = Bungee(key, proxy)
    bungee.refuel(to_chain, random_amount)


def stargate_bridge(key, proxy):
    """
    Make stargate MAV token bridge to BSC
    ______________________________________________________
    all_amount - Swap 90% ETH to MAV and bridge
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = False

    st = Stargate(key, proxy)
    st.bridge(min_amount, max_amount, decimal, all_amount)


def swap_multiswap(key, proxy):
    """
    Multi-Swap module: Automatically performs the specified number of swaps in one of the dexes.
    ______________________________________________________
    use_dex - Choose any dex: syncswap, mute, spacefi, pancake, woofi, velocore
    quantity_swap - Quantity swaps
    ______________________________________________________
    all_amount - If True, swap 90% ETH to USDC, after swap 100% USDC to ETH
    If False, swap 10-90% ETH to USDC, after swap USDC 10-90% to ETH remaining number of times
    """
    use_dex = ["syncswap", "mute", "spacefi"]
    quantity_swap = 2

    sleep_from = 10
    sleep_to = 30

    slippage = 1

    all_amount = False

    multi = Multiswap(key, proxy)
    multi.swap(use_dex, sleep_from, sleep_to, quantity_swap, slippage, all_amount)


def deploy_contract_zksync(key, proxy):
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

    zksync = ZkSync(key, proxy, "zksync")
    zksync.deploy_contract(token_name, token_symbol, min_mint, max_mint)


def custom_routes(key, proxy):
    """
    You can use these methods:
    bridge_zksync, withdraw_zksync, bridge_orbiter, swap_syncswap,
    swap_mute, swap_spacefi, swap_pancake, swap_woofi, swap_velocore,
    deploy_contract, send_mail, mint_nft, send_message, bridge_nft
    """
    use_modules = [swap_spacefi, swap_mute, swap_syncswap, swap_velocore, swap_woofi, swap_pancake]

    sleep_from = 10
    sleep_to = 10

    random_module = False

    routes = Routes(key, proxy)
    routes.start(use_modules, sleep_from, sleep_to, random_module)


#########################################
########### NO NEED TO CHANGE ###########
#########################################

def send_mail(key, proxy):
    dmail = Dmail(key, proxy)
    dmail.send_mail()


def send_message(key, proxy):
    l2telegraph = L2Telegraph(key, proxy)
    l2telegraph.send_message()


def bridge_nft(key, proxy):
    l2telegraph = L2Telegraph(key, proxy)
    l2telegraph.bridge()


def mint_nft(key, proxy):
    mint_nft = Minter(key, proxy)
    mint_nft.mint()


def get_tx_count():
    asyncio.run(check_tx())
