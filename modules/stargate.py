import random
from typing import Union

from loguru import logger
from web3 import Web3
from config import STARGATE_CONTRACT, STARGATE_ABI, ZKSYNC_TOKENS
from utils.gas_checker import check_gas
from utils.sleeping import sleep
from .account import Account
from .syncswap import SyncSwap


class Stargate(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.proxy = proxy

        self.brdige_contract = self.get_contract(STARGATE_CONTRACT, STARGATE_ABI)
        self.tx = {
            "chainId": self.w3.eth.chain_id,
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price
        }

    def get_lz_estimate_fee(self, amount: int):
        get_fee = self.brdige_contract.functions.estimateSendFee(
            Web3.to_checksum_address(ZKSYNC_TOKENS["MAV"]),
            102,
            self.address,
            amount,
            False,
            "0x",
            {
                "callerBps": 0,
                "caller": "0x0000000000000000000000000000000000000000",
                "partnerId": "0x0000",
            }
        ).call()

        return get_fee[0]

    def swap(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
            slippage: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        syncswap = SyncSwap(self.account_id, self.private_key, self.proxy)
        syncswap.swap(
            "ETH",
            "MAV",
            min_amount,
            max_amount,
            decimal,
            slippage,
            all_amount,
            min_percent,
            max_percent
        )

        balance = self.get_balance(ZKSYNC_TOKENS["MAV"])

        if balance["balance_wei"] > 0:
            return True
        return False

    @check_gas
    def bridge(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
            slippage: int,
            sleep_from: int,
            sleep_to: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        balance = self.get_balance(ZKSYNC_TOKENS["MAV"])

        logger.info(f"[{self.account_id}][{self.address}] Make stargate bridge {balance['balance']} MAV to BNB")

        if balance["balance_wei"] > 0:
            self.approve(balance["balance_wei"], ZKSYNC_TOKENS["MAV"], STARGATE_CONTRACT)

            fee = self.get_lz_estimate_fee(balance["balance_wei"])

            self.tx.update({"value": fee})
            self.tx.update({"nonce": self.w3.eth.get_transaction_count(self.address)})

            transaction = self.brdige_contract.functions.sendOFT(
                Web3.to_checksum_address(ZKSYNC_TOKENS["MAV"]),
                102,
                self.address,
                balance["balance_wei"],
                0,
                self.address,
                "0x0000000000000000000000000000000000000000",
                "0x000100000000000000000000000000000000000000000000000000000000000186a0",
                {
                    "callerBps": 0,
                    "caller": "0x0000000000000000000000000000000000000000",
                    "partnerId": "0x0000",
                }
            ).build_transaction(self.tx)

            signed_txn = self.sign(transaction)

            txn_hash = self.send_raw_transaction(signed_txn)

            self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.error(f"[{self.account_id}][{self.address}] Insufficient funds!")

            result_swap = self.swap(min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent)

            if result_swap:
                sleep(sleep_from, sleep_to)

                self.bridge(
                    min_amount,
                    max_amount,
                    decimal,
                    slippage,
                    sleep_from,
                    sleep_to,
                    all_amount,
                    min_percent,
                    max_percent
                )
            else:
                logger.error(f"[{self.account_id}][{self.address}] Insufficient funds for swap!")
