import random
import time

from loguru import logger
from web3 import Web3
from config import ZKSYNC_TOKENS, SYNCSWAP_CLASSIC_POOL_ABI, ZERO_ADDRESS, SYNCSWAP_CONTRACTS, SYNCSWAP_ROUTER_ABI
from .account import Account
from eth_abi import abi


class SyncSwap(Account):
    def __init__(self, private_key: str, proxy: str) -> None:
        super().__init__(private_key=private_key, proxy=proxy, chain="zksync")

        self.swap_contract = self.get_contract(SYNCSWAP_CONTRACTS["router"], SYNCSWAP_ROUTER_ABI)
        self.tx = {
            "from": self.address,
            "gas": random.randint(2900000, 3100000),
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

    def get_pool(self, from_token: str, to_token: str):
        contract = self.get_contract(SYNCSWAP_CONTRACTS["classic_pool"], SYNCSWAP_CLASSIC_POOL_ABI)

        pool_address = contract.functions.getPool(
            Web3.to_checksum_address(ZKSYNC_TOKENS[from_token]),
            Web3.to_checksum_address(ZKSYNC_TOKENS[to_token])
        ).call()

        return pool_address

    def swap(
            self,
            from_token: str,
            to_token: str,
            min_amount: float,
            max_amount: float,
            decimal: int,
            all_amount: bool
    ):
        token_address = Web3.to_checksum_address(ZKSYNC_TOKENS[from_token])

        amount_wei, amount, balance = self.get_amount(from_token, min_amount, max_amount, decimal, all_amount)

        logger.info(f"[{self.address}] Swap on SyncSwap – {from_token} -> {to_token} | {amount} {from_token}")

        if amount_wei <= balance != 0:
            pool_address = self.get_pool(from_token, to_token)

            if pool_address != ZERO_ADDRESS:
                if from_token == "ETH":
                    self.tx.update({"value": amount_wei})
                else:
                    self.approve(amount_wei, token_address, Web3.to_checksum_address(SYNCSWAP_CONTRACTS["router"]))
                    self.tx.update({"nonce": self.w3.eth.get_transaction_count(self.address)})

                steps = [{
                    "pool": pool_address,
                    "data": abi.encode(["address", "address", "uint8"], [token_address, self.address, 1]),
                    "callback": ZERO_ADDRESS,
                    "callbackData": "0x"
                }]

                paths = [{
                    "steps": steps,
                    "tokenIn": ZERO_ADDRESS,
                    "amountIn": amount_wei
                }]

                deadline = int(time.time()) + 1000000

                contract_txn = self.swap_contract.functions.swap(paths, 0, deadline).build_transaction(self.tx)
                # print(contract_txn)
                signed_txn = self.sign(contract_txn)

                txn_hash = self.send_raw_transaction(signed_txn)

                self.wait_until_tx_finished(txn_hash.hex())
            else:
                logger.error(f"[{self.address}] Swap path {from_token} to {to_token} not found!")
        else:
            logger.error(f"[{self.address}] Insufficient funds!")

    def add_liquidity(self, min_amount: float, max_amount: float, decimal: int):
        amount_wei, amount, balance = self.get_amount("ETH", min_amount, max_amount, decimal, False)

        pool_address = self.get_pool("ETH", "USDC")

        self.tx.update({"value": amount_wei})

        transaction = self.swap_contract.functions.addLiquidity2(
            pool_address,
            [
                (Web3.to_checksum_address(ZERO_ADDRESS), amount_wei),
                (Web3.to_checksum_address(ZKSYNC_TOKENS["USDC"]), 0)
            ],
            abi.encode(["address"], [self.address]),
            0,
            ZERO_ADDRESS,
            "0x"
        ).build_transaction(self.tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())

