import random
import time
from typing import Union

from loguru import logger
from web3 import Web3

from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account

from config import (
    PANCAKE_ROUTER_ABI,
    PANCAKE_CONTRACTS,
    PANCAKE_FACTORY_ABI,
    ZKSYNC_TOKENS,
    PANCAKE_QUOTER_ABI,
    ZERO_ADDRESS
)


class Pancake(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.swap_contract = self.get_contract(PANCAKE_CONTRACTS["router"], PANCAKE_ROUTER_ABI)
        self.tx = {
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

    def get_pool(self, from_token: str, to_token: str):
        factory = self.get_contract(PANCAKE_CONTRACTS["factory"], PANCAKE_FACTORY_ABI)

        pool = factory.functions.getPool(
            Web3.to_checksum_address(ZKSYNC_TOKENS[from_token]),
            Web3.to_checksum_address(ZKSYNC_TOKENS[to_token]),
            500
        ).call()

        return pool

    def get_min_amount_out(self, from_token: str, to_token: str, amount: int, slippage: float):
        quoter = self.get_contract(PANCAKE_CONTRACTS["quoter"], PANCAKE_QUOTER_ABI)

        quoter_data = quoter.functions.quoteExactInputSingle((
            Web3.to_checksum_address(ZKSYNC_TOKENS[from_token]),
            Web3.to_checksum_address(ZKSYNC_TOKENS[to_token]),
            amount,
            500,
            0
        )).call()

        return int(quoter_data[0] - (quoter_data[0] / 100 * slippage))

    def swap_to_token(self, from_token: str, to_token: str, amount: int, slippage: int):
        self.tx.update({"value": amount})

        deadline = int(time.time()) + 1000000

        min_amount_out = self.get_min_amount_out(from_token, to_token, amount, slippage)

        transaction_data = self.swap_contract.encodeABI(
            fn_name="exactInputSingle",
            args=[(
                Web3.to_checksum_address(ZKSYNC_TOKENS[from_token]),
                Web3.to_checksum_address(ZKSYNC_TOKENS[to_token]),
                500,
                self.address,
                amount,
                min_amount_out,
                0
            )]
        )

        contract_txn = self.swap_contract.functions.multicall(deadline, [transaction_data]).build_transaction(self.tx)

        return contract_txn

    def swap_to_eth(self, from_token: str, to_token: str, amount: int, slippage: int):
        self.approve(amount, ZKSYNC_TOKENS[from_token], PANCAKE_CONTRACTS["router"])
        self.tx.update({"nonce": self.w3.eth.get_transaction_count(self.address)})

        deadline = int(time.time()) + 1000000

        min_amount_out = self.get_min_amount_out(from_token, to_token, amount, slippage)

        transaction_data = self.swap_contract.encodeABI(
            fn_name="exactInputSingle",
            args=[(
                Web3.to_checksum_address(ZKSYNC_TOKENS[from_token]),
                Web3.to_checksum_address(ZKSYNC_TOKENS[to_token]),
                500,
                "0x0000000000000000000000000000000000000002",
                amount,
                min_amount_out,
                0
            )]
        )

        unwrap_data = self.swap_contract.encodeABI(
            fn_name="unwrapWETH9",
            args=[
                min_amount_out,
                self.address
            ]

        )

        contract_txn = self.swap_contract.functions.multicall(
            deadline,
            [transaction_data, unwrap_data]
        ).build_transaction(self.tx)

        return contract_txn

    @retry
    @check_gas
    def swap(
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
        amount_wei, amount, balance = self.get_amount(
            from_token,
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        logger.info(
            f"[{self.account_id}][{self.address}] Swap on Pancake – {from_token} -> {to_token} | {amount} {from_token}"
        )

        pool = self.get_pool(from_token, to_token)

        if pool != ZERO_ADDRESS:
            if from_token == "ETH":
                contract_txn = self.swap_to_token(from_token, to_token, amount_wei, slippage)
            else:
                contract_txn = self.swap_to_eth(from_token, to_token, amount_wei, slippage)

            signed_txn = self.sign(contract_txn)

            txn_hash = self.send_raw_transaction(signed_txn)

            self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.error(f"[{self.account_id}][{self.address}] Swap path {from_token} to {to_token} not found!")
