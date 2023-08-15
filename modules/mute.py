import random
import time
from loguru import logger

from web3 import Web3
from config import MUTE_ROUTER_ABI, MUTE_CONTRACTS, ZKSYNC_TOKENS
from .account import Account


class Mute(Account):
    def __init__(self, private_key: str, proxy: str) -> None:
        super().__init__(private_key=private_key, proxy=proxy, chain="zksync")

        self.swap_contract = self.get_contract(MUTE_CONTRACTS["router"], MUTE_ROUTER_ABI)
        self.tx = {
            "from": self.address,
            "gas": random.randint(2900000, 3100000),
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

    def swap_to_token(self, from_token: str, to_token: str, amount: int):
        self.tx.update({"value": amount})

        deadline = int(time.time()) + 1000000

        contract_txn = self.swap_contract.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
            0,
            [Web3.to_checksum_address(ZKSYNC_TOKENS[from_token]),
             Web3.to_checksum_address(ZKSYNC_TOKENS[to_token])],
            self.address,
            deadline,
            [False, False]
        ).build_transaction(self.tx)

        return contract_txn

    def swap_to_eth(self, from_token: str, to_token: str, amount: int):
        token_address = Web3.to_checksum_address(ZKSYNC_TOKENS[from_token])

        from_token_stable = True if from_token == "USDC" else False

        self.approve(amount, token_address, MUTE_CONTRACTS["router"])
        self.tx.update({"nonce": self.w3.eth.get_transaction_count(self.address)})

        deadline = int(time.time()) + 1000000

        contract_txn = self.swap_contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
            amount,
            0,
            [Web3.to_checksum_address(ZKSYNC_TOKENS[from_token]),
             Web3.to_checksum_address(ZKSYNC_TOKENS[to_token])],
            self.address,
            deadline,
            [from_token_stable, False]
        ).build_transaction(self.tx)

        return contract_txn

    def swap(
            self,
            from_token: str,
            to_token: str,
            min_amount: float,
            max_amount: float,
            decimal: int,
            all_amount: bool
    ):
        amount_wei, amount, balance = self.get_amount(from_token, min_amount, max_amount, decimal, all_amount)

        logger.info(f"[{self.address}] Swap on Mute – {from_token} -> {to_token} | {amount} {from_token}")

        if amount_wei <= balance != 0:
            if from_token == "ETH":
                contract_txn = self.swap_to_token(from_token, to_token, amount_wei)
            else:
                contract_txn = self.swap_to_eth(from_token, to_token, amount_wei)

            signed_txn = self.sign(contract_txn)

            txn_hash = self.send_raw_transaction(signed_txn)

            self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.error(f"[{self.address}] Insufficient funds!")
