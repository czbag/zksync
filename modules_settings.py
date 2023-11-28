import asyncio
from modules import *


async def bridge_zksync(account_id, key, proxy):
    """
    Deposit from official bridge
    ______________________________________________________
    all_amount - bridge from min_percent to max_percent
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    min_percent = 5
    max_percent = 10

    zksync = ZkSync(account_id, key, proxy, "ethereum")
    await zksync.deposit(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


async def withdraw_zksync(account_id, key, proxy):
    """
    Withdraw from official bridge
    ______________________________________________________
    all_amount - withdraw from min_percent to max_percent
    """

    min_amount = 0.0012
    max_amount = 0.0012
    decimal = 4

    all_amount = False

    min_percent = 10
    max_percent = 10

    zksync = ZkSync(account_id, key, proxy, "zksync")
    await zksync.withdraw(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


async def bridge_orbiter(account_id, key, proxy):
    """
    Bridge from orbiter
    ______________________________________________________
    from_chain – ethereum, polygon_zkevm, arbitrum, optimism, zksync | Select one
    to_chain – ethereum, polygon_zkevm, arbitrum, optimism, zksync | Select one
    """

    from_chain = "zksync"
    to_chain = "base"

    min_amount = 0.005
    max_amount = 0.0051
    decimal = 4

    all_amount = False

    min_percent = 5
    max_percent = 10

    orbiter = Orbiter(account_id, key, from_chain, proxy)
    await orbiter.bridge(to_chain, min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


async def wrap_eth(account_id, key, proxy):
    """
    Wrap ETH
    ______________________________________________________
    all_amount - wrap from min_percent to max_percent
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    min_percent = 5
    max_percent = 5

    zksync = ZkSync(account_id, key, proxy, "zksync")
    await zksync.wrap_eth(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


async def unwrap_eth(account_id, key, proxy):
    """
    Unwrap ETH
    ______________________________________________________
    all_amount - unwrap from min_percent to max_percent
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    min_percent = 100
    max_percent = 100

    zksync = ZkSync(account_id, key, proxy, "zksync")
    await zksync.unwrap_eth(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


async def swap_syncswap(account_id, key, proxy):
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

    min_percent = 10
    max_percent = 10

    syncswap = SyncSwap(account_id, key, proxy)
    await syncswap.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def liquidity_syncswap(account_id, key, proxy):
    """
    Add liqudity on SyncSwap

    amount in ETH, USDC amount not need (auto swap)
    """
    min_amount = 0.01
    max_amount = 0.02
    decimal = 6

    all_amount = True

    min_percent = 50
    max_percent = 50

    syncswap = SyncSwap(account_id, key, proxy)
    await syncswap.add_liquidity(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


async def swap_mute(account_id, key, proxy):
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

    min_percent = 10
    max_percent = 10

    mute = Mute(account_id, key, proxy)
    await mute.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent,
                    max_percent)


async def swap_spacefi(account_id, key, proxy):
    """
    Make swap on SpaceFi
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC, USDT, BUSD, OT, MATIC, WBTC | Select one
    to_token – Choose DESTINATION token ETH, USDC, USDT, BUSD, OT, MATIC, WBTC | Select one

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

    min_percent = 10
    max_percent = 10

    spacefi = SpaceFi(account_id, key, proxy)
    await spacefi.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent,
                       max_percent)


async def liquidity_spacefi(account_id, key, proxy):
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
    await spacefi.add_liquidity(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


async def swap_pancake(account_id, key, proxy):
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

    min_percent = 10
    max_percent = 10

    pancake = Pancake(account_id, key, proxy)
    await pancake.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent,
                       max_percent)


async def swap_woofi(account_id, key, proxy):
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
    await woofi.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_odos(account_id, key, proxy):
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

    all_amount = True

    min_percent = 1
    max_percent = 1

    odos = Odos(account_id, key, proxy)
    await odos.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_zkswap(account_id, key, proxy):
    """
    Make swap on ZkSwap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one

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

    min_percent = 100
    max_percent = 100

    zkswap = ZKSwap(account_id, key, proxy)
    await zkswap.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_xyswap(account_id, key, proxy):
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
    to_token = "WETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 1
    max_percent = 1

    xyswap = XYSwap(account_id, key, proxy)
    await xyswap.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent,
                      max_percent)


async def swap_openocean(account_id, key, proxy):
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
    max_percent = 1

    openocean = OpenOcean(account_id, key, proxy)
    await openocean.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_inch(account_id, key, proxy):
    """
    Make swap on 1inch
    ______________________________________________________
    from_token – Choose SOURCE token ETH, WETH, USDC, USDT, BUSD | Select one
    to_token – Choose DESTINATION token ETH, WETH, USDC, USDT, BUSD | Select one

    Disclaimer - If you use True for use_fee, you support me 1% of the transaction amount
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

    min_percent = 1
    max_percent = 1

    inch_dex = Inch(account_id, key, proxy)
    await inch_dex.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent,
                        max_percent)


async def swap_maverick(account_id, key, proxy):
    """
    Make swap on Maverick
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one
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

    min_percent = 100
    max_percent = 100

    maverick = Maverick(account_id, key, proxy)
    await maverick.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent,
                        max_percent)


async def swap_vesync(account_id, key, proxy):
    """
    Make swap on VeSync
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

    min_percent = 10
    max_percent = 10

    vesync = VeSync(account_id, key, proxy)
    await vesync.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def bungee_refuel(account_id, key, proxy):
    """
    Make refuel on Bungee
    ______________________________________________________
    to_chain – Choose DESTINATION chain: BSC, OPTIMISM, GNOSIS, POLYGON, BASE, ARBITRUM, AVALANCHE, AURORA, ZK_EVM

    Disclaimer - The chain will be randomly selected
    ______________________________________________________
    random_amount – True - amount random from min to max | False - use min amount
    """

    chain_list = ["GNOSIS"]

    random_amount = False

    bungee = Bungee(account_id, key, proxy)
    await bungee.refuel(chain_list, random_amount)


async def stargate_bridge(account_id, key, proxy):
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

    all_amount = True

    min_percent = 10
    max_percent = 20

    stargate = Stargate(account_id, key, proxy)
    await stargate.bridge(
        min_amount, max_amount, decimal, slippage, sleep_from, sleep_to, all_amount, min_percent, max_percent
    )


async def deposit_eralend(account_id, key, proxy):
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
    await eralend.deposit(
        min_amount, max_amount, decimal, sleep_from, sleep_to, make_withdraw, all_amount, min_percent, max_percent
    )


async def deposit_basilisk(account_id, key, proxy):
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
    await basilisk.deposit(
        min_amount, max_amount, decimal, sleep_from, sleep_to, make_withdraw, all_amount, min_percent, max_percent
    )


async def deposit_reactorfusion(account_id, key, proxy):
    """
    Make deposit on ReactorFusion
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
    await reactorfusion.deposit(
        min_amount, max_amount, decimal, sleep_from, sleep_to, make_withdraw, all_amount, min_percent, max_percent
    )


async def deposit_zerolend(account_id, key, proxy):
    """
    Make deposit on ZeroLend
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

    zerolend = ZeroLend(account_id, key, proxy)
    await zerolend.deposit(
        min_amount, max_amount, decimal, sleep_from, sleep_to, make_withdraw, all_amount, min_percent, max_percent
    )


async def deposit_rocketsam(account_id, key, proxy):
    """
    Make deposit on RocketSam
    ______________________________________________________
    make_withdraw - True, if need withdraw after deposit

    all_amount - deposit from min_percent to max_percent
    """
    contracts = [
        "0xbc6C8BbBD06b6785cF898C3a69DbAE56527dEF10",
        "0x267e930bb2cb5d3d62564c20b947ad8839c8f7b6",
        "0xb959a457c54b03d8bf1d126c3baca8ee2cd967f2",
        "0x5b35d48acdc790ebb94523a100a20e97c937de29",
        "0x65b82bd5a83ff082f723ebf4187b7739ad13e230",
        "0xe771b992d2af7d0d99bc93c83cc9c254787e47a8",
        "0x0b6662b53560ca1b4b22e15bd3cf692e864a733c",
        "0xe6bcb3c91982f5f63e4b19b8130a10767762e2a9",
        "0x07068c8e44a4f4816b3921178ccec6cd4d9a4e14",
        "0x59f6cef0843f3506b214055ad6fd3c385f83d1ad",
    ]

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 5

    sleep_from = 30
    sleep_to = 300

    make_withdraw = False

    all_amount = True

    min_percent = 1
    max_percent = 1

    rocketsam = RocketSam(account_id, key, proxy)
    await rocketsam.deposit(
        contracts, min_amount, max_amount, decimal, sleep_from, sleep_to,
        make_withdraw, all_amount, min_percent, max_percent
    )


async def withdraw_rocketsam(account_id, key, proxy):
    """
    Make withdraw from RocketSam
    """
    contracts = [
        "0xbc6C8BbBD06b6785cF898C3a69DbAE56527dEF10",
        "0x267e930bb2cb5d3d62564c20b947ad8839c8f7b6",
        "0xb959a457c54b03d8bf1d126c3baca8ee2cd967f2",
        "0x5b35d48acdc790ebb94523a100a20e97c937de29",
        "0x65b82bd5a83ff082f723ebf4187b7739ad13e230",
        "0xe771b992d2af7d0d99bc93c83cc9c254787e47a8",
        "0x0b6662b53560ca1b4b22e15bd3cf692e864a733c",
        "0xe6bcb3c91982f5f63e4b19b8130a10767762e2a9",
        "0x07068c8e44a4f4816b3921178ccec6cd4d9a4e14",
        "0x59f6cef0843f3506b214055ad6fd3c385f83d1ad",
    ]

    sleep_from = 10
    sleep_to = 30

    rocketsam = RocketSam(account_id, key, proxy)
    await rocketsam.withdraw(contracts, sleep_from, sleep_to)


async def bridge_nft(account_id, key, proxy):
    """
    Make mint NFT and bridge NFT on L2Telegraph
    """

    sleep_from = 5
    sleep_to = 20

    l2telegraph = L2Telegraph(account_id, key, proxy)
    await l2telegraph.bridge(sleep_from, sleep_to)


async def mint_tavaera(account_id, key, proxy):
    """
    Mint Tavaera ID and Tavaera NFT
    """

    sleep_from = 5
    sleep_to = 20

    tavaera_nft = Tavaera(account_id, key, proxy)
    await tavaera_nft.mint(sleep_from, sleep_to)


async def mint_zkstars(account_id, key, proxy):
    """
    Mint ZkStars NFT
    """

    contracts = [
        "0xe7Ed1c47E1e2eA6e9126961df5d41798722A7656",
        "0x53424440d0ead57e599529b42807a0ba1965dd66",
        "0x406b1195f4916b13513fea102777df5bd4af06eb",
        "0xf19b7027d37c3321194d6c5f34ea2e6cbc73fa25",
        "0xd834c621dea708a21b05eaf181115793eaa2f9d9",
        "0xafec8df7b10303c3514826c9e2222a16f1486bee",
        "0x56bf83e598ce80299962be937fe0ba54f5d5e2b2",
        "0x8595d989a96cdbdc1651e3c87ea3d945e0460097",
        "0x945b1edcd03e1d1ad9255c2b28e1c22f2c819f0e",
        "0xc92fc3f19645014c392825e3cfa3597412b0d913",
        "0x808d59a747bfedd9bcb11a63b7e5748d460b614d",
        "0x8dd8706cbc931c87694e452caa0a83a564753241",
        "0x8dd3c29f039e932ebd8eac873b8b7a56d17e36c6",
        "0xca0848cadb25e6fcd9c8ce15bcb8f8da6c1fc519",
        "0x06d52c7e52e9f28e3ad889ab2083fe8dba735d52",
        "0x86f39d51c06cac130ca59eabedc9233a49fcc22a",
        "0xee0d4a8f649d83f6ba5e5c9e6c4d4f6ae846846a",
        "0xfda7967c56ce80f74b06e14ab9c71c80cb78b466",
        "0x0d99efcde08269e2941a5e8a0a02d8e5722403fc",
        "0xf72cf790ac8d93ee823014484fc74f2f1e337bf6"
    ]

    mint_min = 1
    mint_max = 1

    mint_all = False

    sleep_from = 5
    sleep_to = 10

    zkkstars = ZkStars(account_id, key, proxy)
    await zkkstars.mint(contracts, mint_min, mint_max, mint_all, sleep_from, sleep_to)


async def swap_tokens(account_id, key, proxy):
    """
    SwapTokens module: Automatically swap tokens to ETH
    ______________________________________________________
    use_dex - Choose any dex:
    syncswap, mute, spacefi, pancake, woofi, maverick, odos, zkswap, xyswap, openocean, inch, vesync
    """

    use_dex = [
        "maverick", "mute", "pancake", "syncswap",
        "woofi", "spacefi", "odos", "zkswap",
        "xyswap", "openocean", "inch", "vesync"
    ]

    use_tokens = ["USDC"]

    sleep_from = 300
    sleep_to = 600

    slippage = 1

    min_percent = 100
    max_percent = 100

    swap_tokens = SwapTokens(account_id, key, proxy)
    await swap_tokens.swap(use_dex, use_tokens, sleep_from, sleep_to, slippage, min_percent, max_percent)


async def swap_multiswap(account_id, key, proxy):
    """
    Multi-Swap module: Automatically performs the specified number of swaps in one of the dexes.
    ______________________________________________________
    use_dex - Choose any dex:
    syncswap, mute, spacefi, pancake, woofi, maverick, odos, zkswap, xyswap, openocean, inch, vesync

    quantity_swap - Quantity swaps
    ______________________________________________________
    random_swap_token - If True the swap path will be [ETH -> USDC -> USDC -> ETH] (random!)
    If False the swap path will be [ETH -> USDC -> ETH -> USDC]
    """

    use_dex = [
        "maverick", "mute", "pancake", "syncswap",
        "woofi", "spacefi", "odos", "zkswap",
        "xyswap", "openocean", "inch", "vesync"
    ]

    min_swap = 1
    max_swap = 1

    sleep_from = 300
    sleep_to = 600

    slippage = 1

    random_swap_token = True

    min_percent = 10
    max_percent = 10

    multi = Multiswap(account_id, key, proxy)
    await multi.swap(
        use_dex, sleep_from, sleep_to, min_swap, max_swap, slippage, random_swap_token, min_percent, max_percent
    )


async def mint_nft(account_id, key, proxy):
    """
    Mint NFT on NFTS2ME
    ______________________________________________________
    contracts - list NFT contract addresses
    """

    contracts = ["0x4b363957913012789874ab6796bdb7b29d4588d3"]

    minter = Minter(account_id, key, proxy)
    await minter.mint_nft(contracts)


async def custom_routes(account_id, key, proxy):
    """
    BRIDGE:
        – bridge_zksync
        – withdraw_zksync
        – bridge_orbiter
        – bungee_refuel
        – stargate_bridge
    WRAP:
        – wrap_eth
        – unwrap_eth
    DEX:
        – swap_syncswap
        – swap_maverick
        – swap_mute
        – swap_spacefi
        – swap_pancake
        – swap_woofi
        – swap_odos
        – swap_zkswap
        – swap_xyswap
        – swap_inch
        – swap_openocean
        – swap_vesync
    LIQUIDITY:
        – liquidity_syncswap
        – liquidity_spacefi
    LANDING:
        – deposit_eralend, withdraw_erlaned, enable_collateral_eralend, disable_collateral_eralend
        – deposit_basilisk, withdraw_basilisk, enable_collateral_basilisk, disable_collateral_basilisk
        – deposit_reactorfusion, withdraw_reactorfusion,
        enable_collateral_reactorfusion, disable_collateral_reactorfusion
        – deposit_zerolend
        – withdraw_zerolend
        – deposit_rocketsam
        – withdraw_rocketsam
    NFT/DOMAIN:
        – mint_zkstars
        – create_omnisea
        – bridge_nft
        – mint_tavaera
        – mint_nft
        – mint_mailzero_nft
        – mint_zks_domain
        – mint_era_domain
    ANOTHER:
        – send_message (l2Telegraph)
        – send_mail (Dmail)
        – swap_multiswap
        – swap_tokens
        – deploy_contract_zksync
        – create_safe
    ______________________________________________________
    Disclaimer - You can add modules to [] to select random ones,
    example [module_1, module_2, [module_3, module_4], module 5]
    The script will start with module 1, 2, 5 and select a random one from module 3 and 4

    You can also specify None in [], and if None is selected by random, this module will be skipped

    You can also specify () to perform the desired action a certain number of times
    example (send_mail, 1, 10) run this module 1 to 10 times
    """

    use_modules = [
        swap_tokens,
        [create_omnisea, None],
        swap_multiswap,
        mint_zkstars,
        [deposit_eralend, deposit_basilisk, deposit_reactorfusion, deposit_zerolend],
        [send_mail, None],
    ]

    sleep_from = 300
    sleep_to = 700

    random_module = True

    routes = Routes(account_id, key, proxy)
    await routes.start(use_modules, sleep_from, sleep_to, random_module)


async def multi_approve(account_id, key, proxy):
    """
    Make approve all tokens from config in SyncSwap, Mute, SpaceFi, Pancake, WooFi, Velocore

    Disclaimer - You can use 0 for cancel  approve
    """

    amount = 0

    sleep_from = 30
    sleep_to = 95

    multiapprove = MultiApprove(account_id, key, proxy)
    await multiapprove.start(amount, sleep_from, sleep_to)


#########################################
########### NO NEED TO CHANGE ###########
#########################################
async def send_mail(account_id, key, proxy):
    dmail = Dmail(account_id, key, proxy)
    await dmail.send_mail()


async def send_message(account_id, key, proxy):
    l2telegraph = L2Telegraph(account_id, key, proxy)
    await l2telegraph.send_message()


async def mint_mailzero_nft(account_id, key, proxy):
    mint_nft = MailZero(account_id, key, proxy)
    await mint_nft.mint()


async def mint_zks_domain(account_id, key, proxy):
    zks_domain = ZKSDomain(account_id, key, proxy)
    await zks_domain.mint()


async def mint_era_domain(account_id, key, proxy):
    era_domain = EraDomain(account_id, key, proxy)
    await era_domain.mint()


async def withdraw_erlaned(account_id, key, proxy):
    eralend = Eralend(account_id, key, proxy)
    await eralend.withdraw()


async def enable_collateral_eralend(account_id, key, proxy):
    eralend = Eralend(account_id, key, proxy)
    await eralend.enable_collateral()


async def disable_collateral_eralend(account_id, key, proxy):
    eralend = Eralend(account_id, key, proxy)
    await eralend.disable_collateral()


async def withdraw_basilisk(account_id, key, proxy):
    basilisk = Basilisk(account_id, key, proxy)
    await basilisk.withdraw()


async def enable_collateral_basilisk(account_id, key, proxy):
    basilisk = Basilisk(account_id, key, proxy)
    await basilisk.enable_collateral()


async def disable_collateral_basilisk(account_id, key, proxy):
    basilisk = Basilisk(account_id, key, proxy)
    await basilisk.disable_collateral()


async def withdraw_reactorfusion(account_id, key, proxy):
    reactorfusion = ReactorFusion(account_id, key, proxy)
    await reactorfusion.withdraw()


async def enable_collateral_reactorfusion(account_id, key, proxy):
    reactorfusion = ReactorFusion(account_id, key, proxy)
    await reactorfusion.enable_collateral()


async def disable_collateral_reactorfusion(account_id, key, proxy):
    reactorfusion = ReactorFusion(account_id, key, proxy)
    await reactorfusion.disable_collateral()


async def withdraw_zerolend(account_id, key, proxy):
    zerolend = ZeroLend(account_id, key, proxy)
    await zerolend.withdraw()


async def create_omnisea(account_id, key, proxy):
    omnisea = Omnisea(account_id, key, proxy)
    await omnisea.create()


async def create_safe(account_id, key, proxy):
    gnosis_safe = GnosisSafe(account_id, key, proxy)
    await gnosis_safe.create_safe()


def get_tx_count():
    asyncio.run(check_tx())
