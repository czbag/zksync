import asyncio
from modules import *


def bridge_zksync(account_id, key, proxy):
    """
    Deposit from official bridge
    ______________________________________________________
    all_amount - bridge from min_percent to max_percent
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    min_percent = 60
    max_percent = 80

    zksync = ZkSync(account_id, key, proxy, "ethereum")
    zksync.deposit(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


def withdraw_zksync(account_id, key, proxy):
    """
    Withdraw from official bridge
    ______________________________________________________
    all_amount - withdraw from min_percent to max_percent
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = False

    min_percent = 60
    max_percent = 80

    zksync = ZkSync(account_id, key, proxy, "zksync")
    zksync.withdraw(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


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
    all_amount - wrap from min_percent to max_percent
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = False

    min_percent = 60
    max_percent = 80

    zksync = ZkSync(account_id, key, proxy, "zksync")
    zksync.wrap_eth(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


def unwrap_eth(account_id, key, proxy):
    """
    Unwrap ETH
    ______________________________________________________
    all_amount - unwrap from min_percent to max_percent
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    min_percent = 60
    max_percent = 80

    zksync = ZkSync(account_id, key, proxy, "zksync")
    zksync.unwrap_eth(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


def swap_syncswap(account_id, key, proxy):
    """
    Make swap on SyncSwap

    from_token – Choose SOURCE token ETH, USDC, USDT, BUSD, MAV, OT, MATIC, WBTC | Select one
    to_token – Choose DESTINATION token ETH, USDC, USDT, BUSD, MAV, OT, MATIC, WBTC | Select one

    Disclaimer – Don't use stable coin in from and to token | from_token USDC to_token USDT DON'T WORK!!!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 1
    max_amount = 2
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 60
    max_percent = 80

    syncswap = SyncSwap(account_id, key, proxy)
    syncswap.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)


def liquidity_syncswap(account_id, key, proxy):
    """
    Add liqudity on SyncSwap

    amount in ETH, USDC amount not need (auto swap)
    """
    min_amount = 0.01
    max_amount = 0.02
    decimal = 6

    all_amount = True

    min_percent = 5
    max_percent = 10

    syncswap = SyncSwap(account_id, key, proxy)
    syncswap.add_liquidity(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


def swap_mute(account_id, key, proxy):
    """
    Make swap on Mute
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC, WBTC | Select one
    to_token – Choose DESTINATION token ETH, USDC, WBTC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 60
    max_percent = 80

    mute = Mute(account_id, key, proxy)
    mute.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)


def swap_spacefi(account_id, key, proxy):
    """
    Make swap on SpaceFi
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC, USDT, BUSD, OT, MATIC, WBTC | Select one
    to_token – Choose DESTINATION token ETH, USDC, USDT, BUSD, OT, MATIC, WBTC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 60
    max_percent = 80

    spacefi = SpaceFi(account_id, key, proxy)
    spacefi.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)


def liquidity_spacefi(account_id, key, proxy):
    """
    Add liqudity on SpaceFi
    """
    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6

    all_amount = True

    min_percent = 1
    max_percent = 1

    spacefi = SpaceFi(account_id, key, proxy)
    spacefi.add_liquidity(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


def swap_pancake(account_id, key, proxy):
    """
    Make swap on PancakeSwap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.001
    max_amount = 0.002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 60
    max_percent = 80

    pancake = Pancake(account_id, key, proxy)
    pancake.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)


def swap_woofi(account_id, key, proxy):
    """
    Make swap on WooFi
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 60
    max_percent = 80

    woofi = WooFi(account_id, key, proxy)
    woofi.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)


def swap_velocore(account_id, key, proxy):
    """
    Make swap on Velocore
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC, BUSD, WBTC | Select one
    to_token – Choose DESTINATION token ETH, USDC, BUSD, WBTC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "USDC"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = False

    min_percent = 60
    max_percent = 80

    velocore = Velocore(account_id, key, proxy)
    velocore.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)


def swap_odos(account_id, key, proxy):
    """
    Make swap on Odos
    ______________________________________________________
    from_token – Choose SOURCE token ETH, WETH, USDC, USDT, BUSD, MAV, OT, MATIC, WBTC | Select one
    to_token – Choose DESTINATION token ETH, WETH, USDC, USDT, BUSD, MAV, OT, MATIC, WBTC | Select one

    Disclaimer - If you use True for use_fee, you support me 1% of the transaction amount
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "WETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = False

    min_percent = 100
    max_percent = 100

    odos = Odos(account_id, key, proxy)
    odos.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


def swap_zkswap(account_id, key, proxy):
    """
    Make swap on ZkSwap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "USDC"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 60
    max_percent = 80

    zkswap = ZKSwap(account_id, key, proxy)
    zkswap.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)


def swap_xyswap(account_id, key, proxy):
    """
    Make swap on XYSwap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, WETH, USDC, USDT, BUSD, OT | Select one
    to_token – Choose DESTINATION token ETH, WETH, USDC, USDT, BUSD, OT | Select one

    Disclaimer - If you use True for use_fee, you support me 1% of the transaction amount
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "USDC"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 5
    max_percent = 10

    xyswap = XYSwap(account_id, key, proxy)
    xyswap.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)


def swap_openocean(account_id, key, proxy):
    """
    Make swap on OpenOcean
    ______________________________________________________
    from_token – Choose SOURCE token ETH, WETH, USDC, USDT, BUSD, MAV, OT, WBTC | Select one
    to_token – Choose DESTINATION token ETH, WETH, USDC, USDT, BUSD, MAV, OT, WBTC | Select one

    Disclaimer - If you use True for use_fee, you support me 1% of the transaction amount
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "WETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 1
    max_percent = 2

    xyswap = OpenOcean(account_id, key, proxy)
    xyswap.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)


def swap_inch(account_id, key, proxy):
    """
    Make swap on 1inch
    ______________________________________________________
    from_token – Choose SOURCE token ETH, WETH, USDC, USDT, BUSD | Select one
    to_token – Choose DESTINATION token ETH, WETH, USDC, USDT, BUSD | Select one

    Disclaimer - If you use True for use_fee, you support me 1% of the transaction amount
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "WETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 1
    max_percent = 2

    inch_dex = Inch(account_id, key, proxy)
    inch_dex.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)


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
    all_amount - swap from min_percent to max_percent
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4
    slippage = 1

    sleep_from = 5
    sleep_to = 24

    all_amount = False

    min_percent = 60
    max_percent = 80

    st = Stargate(account_id, key, proxy)
    st.bridge(min_amount, max_amount, decimal, slippage, sleep_from, sleep_to, all_amount, min_percent, max_percent)


def deposit_eralend(account_id, key, proxy):
    """
    Make deposit on Eralend
    ______________________________________________________
    make_withdraw - True, if need withdraw after deposit

    all_amount - deposit from min_percent to max_percent
    """
    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 5

    sleep_from = 5
    sleep_to = 24

    make_withdraw = True

    all_amount = True

    min_percent = 5
    max_percent = 10

    eralend = Eralend(account_id, key, proxy)
    eralend.deposit(
        min_amount, max_amount, decimal, sleep_from, sleep_to, make_withdraw, all_amount, min_percent, max_percent
    )


def deposit_basilisk(account_id, key, proxy):
    """
    Make deposit on Basilisk
    ______________________________________________________
    make_withdraw - True, if need withdraw after deposit

    all_amount - deposit from min_percent to max_percent
    """
    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 5

    sleep_from = 5
    sleep_to = 24

    make_withdraw = True

    all_amount = False

    min_percent = 60
    max_percent = 80

    basilisk = Basilisk(account_id, key, proxy)
    basilisk.deposit(
        min_amount, max_amount, decimal, sleep_from, sleep_to, make_withdraw, all_amount, min_percent, max_percent
    )


def deposit_reactorfusion(account_id, key, proxy):
    """
    Make deposit on Basilisk
    ______________________________________________________
    make_withdraw - True, if need withdraw after deposit

    all_amount - deposit from min_percent to max_percent
    """
    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 5

    sleep_from = 5
    sleep_to = 24

    make_withdraw = True

    all_amount = False

    min_percent = 60
    max_percent = 80

    reactorfusion = ReactorFusion(account_id, key, proxy)
    reactorfusion.deposit(
        min_amount, max_amount, decimal, sleep_from, sleep_to, make_withdraw, all_amount, min_percent, max_percent
    )


def send_mail(account_id, key, proxy):
    """
    Dmail mail sender
    """

    random_receiver = True

    dmail = Dmail(account_id, key, proxy)
    dmail.send_mail(random_receiver)


def bridge_nft(account_id, key, proxy):
    """
    Make mint NFT and bridge NFT on L2Telegraph
    """

    sleep_from = 5
    sleep_to = 20

    l2telegraph = L2Telegraph(account_id, key, proxy)
    l2telegraph.bridge(sleep_from, sleep_to)


def mint_tavaera(account_id, key, proxy):
    """
    Mint Tavaera ID and Tavaera NFT
    """

    sleep_from = 5
    sleep_to = 20

    tavaera_nft = Tavaera(account_id, key, proxy)
    tavaera_nft.mint(sleep_from, sleep_to)


def swap_multiswap(account_id, key, proxy):
    """
    Multi-Swap module: Automatically performs the specified number of swaps in one of the dexes.
    ______________________________________________________
    use_dex - Choose any dex: syncswap, mute, spacefi, pancake, woofi, velocore, odos, zkswap, xyswap, openocean, inch
    quantity_swap - Quantity swaps
    ______________________________________________________
    random_swap_token - If True the swap path will be [ETH -> USDC -> USDC -> ETH] (random!)
    If False the swap path will be [ETH -> USDC -> ETH -> USDC]
    """

    use_dex = ["velocore", "mute", "pancake", "syncswap", "woofi", "spacefi", "odos", "zkswap", "xyswap", "openocean", "inch"]

    min_swap = 4
    max_swap = 10

    sleep_from = 300
    sleep_to = 600

    slippage = 1

    random_swap_token = True

    min_percent = 10
    max_percent = 60

    multi = Multiswap(account_id, key, proxy)
    multi.swap(use_dex, sleep_from, sleep_to, min_swap, max_swap, slippage, random_swap_token, min_percent, max_percent)


def deploy_contract_zksync(account_id, key, proxy):
    """
    Deploy contract token and mint
    ______________________________________________________
    token_name – Any token name
    token_symbol – Any token symbol
    ______________________________________________________
    min_mint – Amount of mint 2
    max_mint – Amount of mint 1000
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
    bridge_zksync, withdraw_zksync, bridge_orbiter, wrap_eth, unwrap_eth, swap_syncswap, liquidity_syncswap, swap_mute,
    swap_spacefi, liquidity_spacefi, swap_pancake, swap_woofi, swap_velocore, swap_odos, swap_zkswap, swap_xyswap, swap_inch,
    swap_openocean, bungee_refuel, stargate_bridge, deposit_eralend, withdraw_erlaned, deposit_basilisk, withdraw_basilisk,
    deposit_reactorfusion, withdraw_reactorfusion,
    enable_collateral_eralend, disable_collateral_eralend
    enable_collateral_basilisk, disable_collateral_basilisk
    enable_collateral_reactorfusion, disable_collateral_reactorfusion,
    create_omnisea, bridge_nft, mint_tavaera, mint_nft,
    mint_zks_domain, mint_era_domain, send_message, send_mail, swap_multiswap, custom_routes, multi_approve,
    deploy_contract_zksync


    ______________________________________________________
    Disclaimer - You can add modules to [] to select random ones,
    example [module_1, module_2, [module_3, module_4], module 5]
    The script will start with module 1, 2, 5 and select a random one from module 3 and 4
    """

    use_modules = [
        swap_multiswap,
        [mint_tavaera, create_omnisea],
        [deposit_eralend, deposit_basilisk, deposit_reactorfusion],
        [mint_era_domain, mint_zks_domain]
    ]

    sleep_from = 300
    sleep_to = 700

    random_module = True

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


def send_message(account_id, key, proxy):
    l2telegraph = L2Telegraph(account_id, key, proxy)
    l2telegraph.send_message()


def mint_nft(account_id, key, proxy):
    mint_nft = Minter(account_id, key, proxy)
    mint_nft.mint()


def mint_zks_domain(account_id, key, proxy):
    zks_domain = ZKSDomain(account_id, key, proxy)
    zks_domain.mint()


def mint_era_domain(account_id, key, proxy):
    era_domain = EraDomain(account_id, key, proxy)
    era_domain.mint()


def withdraw_erlaned(account_id, key, proxy):
    eralend = Eralend(account_id, key, proxy)
    eralend.withdraw()


def enable_collateral_eralend(account_id, key, proxy):
    eralend = Eralend(account_id, key, proxy)
    eralend.enable_collateral()


def disable_collateral_eralend(account_id, key, proxy):
    eralend = Eralend(account_id, key, proxy)
    eralend.disable_collateral()


def withdraw_basilisk(account_id, key, proxy):
    basilisk = Basilisk(account_id, key, proxy)
    basilisk.withdraw()


def enable_collateral_basilisk(account_id, key, proxy):
    basilisk = Basilisk(account_id, key, proxy)
    basilisk.enable_collateral()


def disable_collateral_basilisk(account_id, key, proxy):
    basilisk = Basilisk(account_id, key, proxy)
    basilisk.disable_collateral()


def withdraw_reactorfusion(account_id, key, proxy):
    reactorfusion = ReactorFusion(account_id, key, proxy)
    reactorfusion.withdraw()


def enable_collateral_reactorfusion(account_id, key, proxy):
    reactorfusion = ReactorFusion(account_id, key, proxy)
    reactorfusion.enable_collateral()


def disable_collateral_reactorfusion(account_id, key, proxy):
    reactorfusion = ReactorFusion(account_id, key, proxy)
    reactorfusion.disable_collateral()


def create_omnisea(account_id, key, proxy):
    omnisea = Omnisea(account_id, key, proxy)
    omnisea.create()


def get_tx_count():
    asyncio.run(check_tx())
