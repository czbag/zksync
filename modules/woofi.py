import random
import time

from loguru import logger
from web3 import Web3
from config import WOOFI_CONTRACTS, WOOFI_ROUTER_ABI, ZKSYNC_TOKENS
from .account import Account


class WooFi(Account):
    def __init__(self, private_key: str, proxy: str) -> None:
        super().__init__(private_key=private_key, proxy=proxy, chain="zksync")

    def swap(self, from_token: str, to_token: str, min_swap: float, max_swap: float, decimal: int):
        amount = round(random.uniform(min_swap, max_swap), decimal)

        logger.info(f"[{self.address}] Swap – {from_token} -> {to_token} | {amount} {from_token}")

        swap_contract = self.get_contract(WOOFI_CONTRACTS["router"], WOOFI_ROUTER_ABI)

        tx = {
            "from": self.address,
            "gas": random.randint(2900000, 3100000),
            "gasPrice": Web3.to_wei("0.25", "gwei"),
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

        if from_token == "ETH":
            from_token_address = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
            to_token_address = Web3.to_checksum_address(ZKSYNC_TOKENS[to_token])
            amount = Web3.to_wei(amount, "ether")
            balance = self.w3.eth.get_balance(self.address)
            tx.update({"value": amount})
        else:
            from_token_address = Web3.to_checksum_address(ZKSYNC_TOKENS[from_token])
            to_token_address = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
            token_contract = self.get_contract(from_token_address)
            amount = int(amount * 10 ** token_contract.functions.decimals().call())
            balance = self.get_balance(from_token_address)["balance_wei"]

            self.approve(amount, from_token_address, WOOFI_CONTRACTS["router"])
            tx.update({"nonce": self.w3.eth.get_transaction_count(self.address)})

        if amount < balance:
            contract_txn = swap_contract.functions.swap(
                from_token_address,
                to_token_address,
                amount,
                0,
                self.address,
                self.address
            ).build_transaction(tx)

            signed_txn = self.sign(contract_txn)

            txn_hash = self.send_raw_transaction(signed_txn)

            self.wait_until_tx_finished(txn_hash.hex())

        else:
            logger.error(f"[{self.address}] Insufficient funds!")
