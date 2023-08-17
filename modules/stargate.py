import random

from loguru import logger
from web3 import Web3
from config import STARGATE_CONTRACT, STARGATE_ABI, ZKSYNC_TOKENS
from .account import Account
from .syncswap import SyncSwap


class Stargate(Account):
    def __init__(self, private_key: str, proxy: str) -> None:
        super().__init__(private_key=private_key, proxy=proxy, chain="zksync")

        self.proxy = proxy

        self.brdige_contract = self.get_contract(STARGATE_CONTRACT, STARGATE_ABI)
        self.tx = {
            "chainId": self.w3.eth.chain_id,
            "from": self.address,
            "gas": random.randint(2900000, 3100000),
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

    def swap(self, min_amount: float, max_amount: float, decimal: int, slippage: int, all_amount: bool):
        syncswap = SyncSwap(self.private_key, self.proxy)
        syncswap.swap("ETH", "MAV", min_amount, max_amount, decimal, slippage, all_amount)

    def bridge(self, min_amount: float, max_amount: float, decimal: int, slippage: int, all_amount: bool):
        balance = self.get_balance(ZKSYNC_TOKENS["MAV"])

        logger.info(f"[{self.address}] Make stargate bridge {balance['balance']} MAV to BNB")

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
            logger.error(f"[{self.address}] Insufficient funds!")
            self.swap(min_amount, max_amount, decimal, slippage, all_amount)
            self.bridge(min_amount, max_amount, decimal, slippage, all_amount)
