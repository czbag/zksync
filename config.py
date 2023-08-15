import json
from pathlib import Path

with open('data/rpc.json') as file:
    RPC = json.load(file)

with open('data/abi/erc20_abi.json') as file:
    ERC20_ABI = json.load(file)

with open("accounts.txt", "r") as file:
    ACCOUNTS = [row.strip() for row in file]

with open("proxy.txt", "r") as file:
    PROXIES = [row.strip() for row in file]

with open('data/abi/zksync/bridge.json') as file:
    ZKSYNC_BRIDGE_ABI = json.load(file)

with open("data/abi/syncswap/router.json", "r") as file:
    SYNCSWAP_ROUTER_ABI = json.load(file)

with open('data/abi/syncswap/classic_pool.json') as file:
    SYNCSWAP_CLASSIC_POOL_ABI = json.load(file)

with open("data/abi/mute/router.json", "r") as file:
    MUTE_ROUTER_ABI = json.load(file)

with open("data/abi/spacefi/router.json", "r") as file:
    SPACEFI_ROUTER_ABI = json.load(file)

with open("data/abi/pancake/router.json", "r") as file:
    PANCAKE_ROUTER_ABI = json.load(file)

with open("data/abi/woofi/router.json", "r") as file:
    WOOFI_ROUTER_ABI = json.load(file)

with open("data/abi/velocore/router.json", "r") as file:
    VELOCORE_ROUTER_ABI = json.load(file)

with open("data/abi/bungee/abi.json", "r") as file:
    BUNGEE_ABI = json.load(file)

with open("data/abi/stargate/router.json", "r") as file:
    STARGATE_ABI = json.load(file)

with open("data/abi/dmail/abi.json", "r") as file:
    DMAIL_ABI = json.load(file)

with open("data/abi/l2telegraph/send_message.json", "r") as file:
    L2TELEGRAPH_MESSAGE_ABI = json.load(file)

with open("data/abi/l2telegraph/bridge_nft.json", "r") as file:
    L2TELEGRAPH_NFT_ABI = json.load(file)

with open("data/abi/minter/abi.json", "r") as file:
    MINTER_ABI = json.load(file)

ZKSYNC_BRIDGE_CONTRACT = "0x32400084c286cf3e17e7b677ea9583e60a000324"

ORBITER_CONTRACT = "0x80C67432656d59144cEFf962E8fAF8926599bCF8"

CONTRACT_PATH = Path("data/deploy/Token.json")

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

ZKSYNC_TOKENS = {
    "ETH": "0x5aea5775959fbc2557cc8789bc1bf90a239d9a91",
    "USDC": "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4",
    "USDT": "0x493257fd37edb34451f62edf8d2a0c418852ba4c",
    "BUSD": "0x2039bb4116b4efc145ec4f0e2ea75012d6c0f181",
    "MATIC": "0x28a487240e4d45cff4a2980d334cc933b7483842",
    "OT": "0xd0ea21ba66b67be636de1ec4bd9696eb8c61e9aa",
    "MAV": "0x787c09494ec8bcb24dcaf8659e7d5d69979ee508",
    "WBTC": "0xbbeb516fb02a01611cbbe0453fe3c580d7281011",
}

SYNCSWAP_CONTRACTS = {
    "router": "0x2da10A1e27bF85cEdD8FFb1AbBe97e53391C0295",
    "classic_pool": "0xf2DAd89f2788a8CD54625C60b55cD3d2D0ACa7Cb"
}

MUTE_CONTRACTS = {
    "router": "0x8B791913eB07C32779a16750e3868aA8495F5964"
}

SPACEFI_CONTRACTS = {
    "router": "0xbE7D1FD1f6748bbDefC4fbaCafBb11C6Fc506d1d"
}

PANCAKE_CONTRACTS = {
    "router": "0x5aEaF2883FBf30f3D62471154eDa3C0c1b05942d"
}

WOOFI_CONTRACTS = {
    "router": "0xfd505702b37Ae9b626952Eb2DD736d9045876417"
}

VELOCORE_CONTRACTS = {
    "router": "0xd999e16e68476bc749a28fc14a0c3b6d7073f50c"
}

BUNGEE_CONTRACT = "0x7ee459d7fde8b4a3c22b9c8c7aa52abaddd9ffd5"

STARGATE_CONTRACT = "0xdac7479e5f7c01cc59bbf7c1c4edf5604ada1ff2"

DMAIL_CONTRACT = "0x981F198286E40F9979274E0876636E9144B8FB8E"

L2TELEGRAPH_MESSAGE_CONTRACT = "0x0d4a6d5964f3b618d8e46bcfbf2792b0d769fbda"

L2TELEGRAPH_NFT_CONTRACT = "0xD43A183C97dB9174962607A8b6552CE320eAc5aA"

MINTER_CONTRACT = "0x31DCD96f29BD32F3a1856247846E9d2f95C2b639"
