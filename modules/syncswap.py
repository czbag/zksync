import random
import time

from loguru import logger
from web3 import Web3
from config import SYNCSWAP_ROUTER_ABI, ZERO_ADDRESS, SYNCSWAP_CONTRACTS, SYNCSWAP_POOL, ZKSYNC_TOKENS
from .account import Account
from eth_abi import abi


class SyncSwap(Account):
    def __init__(self, private_key: str, proxy: str) -> None:
        super().__init__(private_key, "zksync", proxy)

    def swap(self, from_token: str, to_token: str, min_swap: float, max_swap: float, decimal: int):
        amount = round(random.uniform(min_swap, max_swap), decimal)

        logger.info(f"[{self.address}] Swap – {from_token} -> {to_token} | {amount} {from_token}")

        swap_contract = self.get_contract(SYNCSWAP_CONTRACTS["router"], SYNCSWAP_ROUTER_ABI)

        tx = {
            "from": self.address,
            "gas": 3000000,
            "gasPrice": Web3.to_wei("0.25", "gwei"),
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

        if from_token == "ETH":
            token_address = ZERO_ADDRESS
            amount = Web3.to_wei(amount, "ether")
            balance = self.w3.eth.get_balance(self.address)
            tx.update({"value": amount})
        else:
            token_address = Web3.to_checksum_address(ZKSYNC_TOKENS[from_token])
            token_contract = self.get_contract(Web3.to_checksum_address(token_address))
            amount = int(amount * 10 ** token_contract.functions.decimals().call())
            balance = self.get_balance(token_address)["balance_wei"]

            self.approve(amount, token_address, SYNCSWAP_CONTRACTS["router"])
            tx.update({"nonce": self.w3.eth.get_transaction_count(self.address)})

        if amount < balance:
            steps = [{
                "pool": Web3.to_checksum_address(SYNCSWAP_POOL),
                "data": abi.encode(["address", "address", "uint8"], [token_address, self.address, 1]),
                "callback": ZERO_ADDRESS,
                "callbackData": "0x"
            }]

            deadline = int(time.time()) + 1000000

            paths = [{
                "steps": steps,
                "tokenIn": token_address,
                "amountIn": amount
            }]

            contract_txn = swap_contract.functions.swap(paths, 0, deadline).build_transaction(tx)

            signed_txn = self.sign(contract_txn)

            txn_hash = self.send_raw_transaction(signed_txn)

            self.wait_until_tx_finished(txn_hash.hex())

        else:
            logger.error(f"[{self.address}] Insufficient funds!")
