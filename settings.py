from modules import *

# RANDOM WALLETS MODE
RANDOM_WALLET = False  # True or False

# SLEEP MODE
IS_SLEEP = True  # True or False

SLEEP_FROM = 100  # Second
SLEEP_TO = 1200  # Second

# PROXY MODE
USE_PROXY = True

# GWEI CONTROL MODE
CHECK_GWEI = False  # True or False
MAX_GWEI = 40

# ROUTES SETTINGS
"""
You can use these methods: bridge_zksync, bridge_orbiter, swap_syncswap, swap_mute, swap_spacefi, swap_pancake
"""
RANDOM_ROUTES = False
ROUTES = ["swap_syncswap", "swap_pancake", "swap_syncswap"]
ROUTE_SLEEP_FROM = 10
ROUTE_SLEEP_TO = 20


def bridge_zksync(key, proxy):
    """
    Deposit from official bridge
    ______________________________________________________
    amount – Amount of bridge (2, 5), type in uniform(2, 5) | number after uniform() – decimal point
    """

    min_bridge = 0.035
    max_bridge = 0.038
    decimal = 4

    zksync = ZkSync(key, proxy)
    zksync.deposit(min_bridge, max_bridge, decimal)


def bridge_orbiter(key, proxy):
    """
    Bridge from orbiter
    ______________________________________________________
    from_chain – ethereum, polygon_zkevm, arbitrum, optimism, zksync | Select one
    to_chain – ethereum, polygon_zkevm, arbitrum, optimism, zksync | Select one
    ______________________________________________________
    amount – Amount of bridge (2, 5), type in uniform(2, 5) | number after uniform() – decimal point
    amount – Limit range amount for bridge – minimum 0.005, maximum 5
    """

    from_chain = "zksync"
    to_chain = "ethereum"

    min_bridge = 1
    max_bridge = 3
    decimal = 4

    orbiter = Orbiter(key, from_chain, proxy)
    orbiter.bridge(to_chain, min_bridge, max_bridge, decimal)


def swap_syncswap(key, proxy):
    """
    Make swap on syncswap

    from_token – Choose SOURCE token ETH/USDC | Select one
    to_token – Choose DESTINATION token ETH/USDC | Select one
    ______________________________________________________
    amount – Amount of swap (2, 5), type in uniform(2, 5) | number after uniform() – decimal point
    """

    from_token = "ETH"
    to_token = "USDC"

    min_swap = 0.001
    max_swap = 0.002
    decimal = 4

    syncswap = SyncSwap(key, proxy)
    syncswap.swap(from_token, to_token, min_swap, max_swap, decimal)


def swap_mute(key, proxy):
    """
    Make swap on mute
    ______________________________________________________
    from_token – Choose SOURCE token ETH/USDC | Select one
    to_token – Choose DESTINATION token ETH/USDC | Select one
    ______________________________________________________
    amount – Amount of swap (2, 5), type in uniform(2, 5) | number after uniform() – decimal point
    """

    from_token = "USDC"
    to_token = "ETH"

    min_swap = 1
    max_swap = 2
    decimal = 4

    mute = Mute(key, proxy)
    mute.swap(from_token, to_token, min_swap, max_swap, decimal)


def swap_spacefi(key, proxy):
    """
    Make swap on space.fi
    ______________________________________________________
    from_token – Choose SOURCE token ETH/USDC | Select one
    to_token – Choose DESTINATION token ETH/USDC | Select one
    ______________________________________________________
    amount – Amount of swap (2, 5), type in uniform(2, 5) | number after uniform() – decimal point
    """

    from_token = "ETH"
    to_token = "USDC"

    min_swap = 0.001
    max_swap = 0.002
    decimal = 4

    spacefi = SpaceFi(key, proxy)
    spacefi.swap(from_token, to_token, min_swap, max_swap, decimal)


def swap_pancake(key, proxy):
    """
    Make swap on PancakeSwap
    ______________________________________________________
    from_token – Choose SOURCE token ETH/USDC | Select one
    to_token – Choose DESTINATION token ETH/USDC | Select one
    ______________________________________________________
    amount – Amount of swap (2, 5), type in uniform(2, 5) | number after uniform() – decimal point
    """

    from_token = "USDC"
    to_token = "ETH"

    min_swap = 20
    max_swap = 21
    decimal = 4

    spacefi = Pancake(key, proxy)
    spacefi.swap(from_token, to_token, min_swap, max_swap, decimal)
