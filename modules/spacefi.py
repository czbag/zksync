import time
from typing import Union, Dict

from loguru import logger
from config import SPACEFI_ROUTER_ABI, SPACEFI_CONTRACTS, ZKSYNC_TOKENS
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class SpaceFi(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.swap_contract = self.get_contract(SPACEFI_CONTRACTS["router"], SPACEFI_ROUTER_ABI)

    async def get_min_amount_out(self, from_token: str, to_token: str, amount: int, slippage: float):
        min_amount_out = await self.swap_contract.functions.getAmountsOut(
            amount,
            [
                self.w3.to_checksum_address(from_token),
                self.w3.to_checksum_address(to_token)
            ]
        ).call()
        return int(min_amount_out[1] - (min_amount_out[1] / 100 * slippage))

    async def swap_to_token(self, from_token: str, to_token: str, amount: int, slippage: int):
        tx_data = await self.get_tx_data(amount)

        deadline = int(time.time()) + 1000000

        min_amount_out = await self.get_min_amount_out(
            ZKSYNC_TOKENS[from_token],
            ZKSYNC_TOKENS[to_token],
            amount,
            slippage
        )

        contract_txn = await self.swap_contract.functions.swapExactETHForTokens(
            min_amount_out,
            [self.w3.to_checksum_address(ZKSYNC_TOKENS[from_token]),
             self.w3.to_checksum_address(ZKSYNC_TOKENS[to_token])],
            self.address,
            deadline
        ).build_transaction(tx_data)

        return contract_txn

    async def swap_to_eth(self, from_token: str, to_token: str, amount: int, slippage: int):
        token_address = self.w3.to_checksum_address(ZKSYNC_TOKENS[from_token])

        await self.approve(amount, token_address, SPACEFI_CONTRACTS["router"])

        tx_data = await self.get_tx_data()

        deadline = int(time.time()) + 1000000

        min_amount_out = await self.get_min_amount_out(
            ZKSYNC_TOKENS[from_token],
            ZKSYNC_TOKENS[to_token],
            amount,
            slippage
        )

        contract_txn = await self.swap_contract.functions.swapExactTokensForETH(
            amount,
            min_amount_out,
            [self.w3.to_checksum_address(ZKSYNC_TOKENS[from_token]),
             self.w3.to_checksum_address(ZKSYNC_TOKENS[to_token])],
            self.address,
            deadline
        ).build_transaction(tx_data)

        return contract_txn

    @retry
    @check_gas
    async def swap(
            self,
            from_token: str,
            to_token: str,
            min_amount: float,
            max_amount: float,
            decimal: int,
            slippage: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
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
            f"[{self.account_id}][{self.address}] Swap on SpaceFi – {from_token} -> {to_token} | {amount} {from_token}"
        )

        if from_token == "ETH":
            contract_txn = await self.swap_to_token(from_token, to_token, amount_wei, slippage)
        else:
            contract_txn = await self.swap_to_eth(from_token, to_token, amount_wei, slippage)

        signed_txn = await self.sign(contract_txn)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

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

        deadline = int(time.time()) + 1000000

        await self.approve(2 ** 128, ZKSYNC_TOKENS["USDC"], SPACEFI_CONTRACTS["router"])

        tx_data = await self.get_tx_data(amount_wei)

        transaction = await self.swap_contract.functions.addLiquidityETH(
            self.w3.to_checksum_address(ZKSYNC_TOKENS["USDC"]),
            amount_wei,
            0,
            0,
            self.address,
            deadline
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())
