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

with open("data/abi/syncswap/router.json", "r") as file:
    SYNCSWAP_ROUTER_ABI = json.load(file)

with open("data/abi/spacefi/router.json", "r") as file:
    SPACEFI_ROUTER_ABI = json.load(file)

with open("data/abi/mute/router.json", "r") as file:
    MUTE_ROUTER_ABI = json.load(file)

with open("data/abi/pancake/router.json", "r") as file:
    PANCAKE_ROUTER_ABI = json.load(file)

CONTRACT_PATH = Path("data/deploy/Token.json")

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

ZKSYNC_TOKENS = {
    "ETH": "0x5aea5775959fbc2557cc8789bc1bf90a239d9a91",
    "USDC": "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4"
}

SYNCSWAP_CONTRACTS = {
    "router": "0x2da10A1e27bF85cEdD8FFb1AbBe97e53391C0295",
    "WETH": "0x5aea5775959fbc2557cc8789bc1bf90a239d9a91",
}

SPACEFI_CONTRACTS = {
    "router": "0xbE7D1FD1f6748bbDefC4fbaCafBb11C6Fc506d1d"
}

MUTE_CONTRACTS = {
    "router": "0x8B791913eB07C32779a16750e3868aA8495F5964"
}

PANCAKE_CONTRACTS = {
    "router": "0x5aEaF2883FBf30f3D62471154eDa3C0c1b05942d"
}

SYNCSWAP_POOL = "0x80115c708E12eDd42E504c1cD52Aea96C547c05c"

ORBITER_CONTRACT = "0x80C67432656d59144cEFf962E8fAF8926599bCF8"
