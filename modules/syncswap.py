import time
from typing import Union, Dict

from loguru import logger
from config import (
    ZKSYNC_TOKENS,
    SYNCSWAP_CLASSIC_POOL_ABI,
    ZERO_ADDRESS,
    SYNCSWAP_CONTRACTS,
    SYNCSWAP_ROUTER_ABI,
    SYNCSWAP_CLASSIC_POOL_DATA_ABI
)
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
from eth_abi import abi


class SyncSwap(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.swap_contract = self.get_contract(SYNCSWAP_CONTRACTS["router"], SYNCSWAP_ROUTER_ABI)

    async def get_pool(self, from_token: str, to_token: str):
        contract = self.get_contract(SYNCSWAP_CONTRACTS["classic_pool"], SYNCSWAP_CLASSIC_POOL_ABI)

        pool_address = await contract.functions.getPool(
            self.w3.to_checksum_address(ZKSYNC_TOKENS[from_token]),
            self.w3.to_checksum_address(ZKSYNC_TOKENS[to_token])
        ).call()

        return pool_address

    async def get_min_amount_out(self, pool_address: str, token_address: str, amount: int, slippage: float):
        pool_contract = self.get_contract(pool_address, SYNCSWAP_CLASSIC_POOL_DATA_ABI)

        min_amount_out = await pool_contract.functions.getAmountOut(
            token_address,
            amount,
            self.address
        ).call()

        return int(min_amount_out - (min_amount_out / 100 * slippage))

    @retry
    @check_gas
    async def swap(
            self,
            from_token: str,
            to_token: str,
            min_amount: float,
            max_amount: float,
            decimal: int,
            slippage: float,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        token_address = self.w3.to_checksum_address(ZKSYNC_TOKENS[from_token])

        amount_wei, amount, balance = await self.get_amount(
            from_token,
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        logger.info(
            f"[{self.account_id}][{self.address}] Swap on SyncSwap – {from_token} -> {to_token} | {amount} {from_token}"
        )

        pool_address = await self.get_pool(from_token, to_token)

        if pool_address != ZERO_ADDRESS:
            tx_data = await self.get_tx_data()

            if from_token == "ETH":
                tx_data.update({"value": amount_wei})
            else:
                await self.approve(amount_wei, token_address, self.w3.to_checksum_address(SYNCSWAP_CONTRACTS["router"]))

            min_amount_out = await self.get_min_amount_out(pool_address, token_address, amount_wei, slippage)

            steps = [{
                "pool": pool_address,
                "data": abi.encode(["address", "address", "uint8"], [token_address, self.address, 1]),
                "callback": ZERO_ADDRESS,
                "callbackData": "0x"
            }]

            paths = [{
                "steps": steps,
                "tokenIn": ZERO_ADDRESS if from_token == "ETH" else token_address,
                "amountIn": amount_wei
            }]

            deadline = int(time.time()) + 1000000

            contract_txn = await self.swap_contract.functions.swap(
                paths,
                min_amount_out,
                deadline
            ).build_transaction(tx_data)

            signed_txn = await self.sign(contract_txn)

            txn_hash = await self.send_raw_transaction(signed_txn)

            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.error(f"[{self.account_id}][{self.address}] Swap path {from_token} to {to_token} not found!")

    @retry
    @check_gas
    async def add_liquidity(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):

        amount_wei, amount, balance = await self.get_amount(
            "ETH", min_amount, max_amount, decimal, all_amount, min_percent, max_percent
        )

        pool_address = await self.get_pool("ETH", "USDC")

        tx_data = await self.get_tx_data(amount_wei)

        transaction = await self.swap_contract.functions.addLiquidity2(
            pool_address,
            [
                (self.w3.to_checksum_address(ZERO_ADDRESS), amount_wei),
                (self.w3.to_checksum_address(ZKSYNC_TOKENS["USDC"]), 0)
            ],
            abi.encode(["address"], [self.address]),
            0,
            ZERO_ADDRESS,
            "0x"
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())
