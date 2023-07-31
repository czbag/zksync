import random

from loguru import logger
from web3 import Web3
from config import RPC, ZKSYNC_BRIDGE_ABI, ZKSYNC_BRIDGE
from .account import Account


class ZkSync(Account):
    def __init__(self, private_key: str, proxy: str) -> None:
        super().__init__(private_key=private_key, proxy=proxy, chain="ethereum")
        request_kwargs = {}
        if proxy:
            request_kwargs = {"proxies": {"https": f"http://{proxy}"}}
        self.zk_w3 = Web3(Web3.HTTPProvider(random.choice(RPC["zksync"]["rpc"]), request_kwargs=request_kwargs))

    def get_tx_data(self, value: int):
        data = {
            "chainId": self.w3.eth.chain_id,
            "nonce": self.w3.eth.get_transaction_count(self.address),
            "from": self.address,
            "value": value
        }
        return data

    def deposit(self, min_bridge: float, max_bridge: float, decimal: int):
        amount = round(random.uniform(min_bridge, max_bridge), decimal)

        logger.info(f"[{self.address}] Bridge to ZkSync | {amount} ETH")

        gas_limit = random.randint(700000, 1300000)

        contract = self.get_contract(Web3.to_checksum_address(ZKSYNC_BRIDGE),
                                     ZKSYNC_BRIDGE_ABI)
        base_cost = contract.functions.l2TransactionBaseCost(self.w3.eth.gas_price, gas_limit, 800).call()

        tx_data = self.get_tx_data(Web3.to_wei(amount, "ether") + base_cost)

        balance = self.w3.eth.get_balance(self.address)

        if tx_data['value'] >= balance:
            logger.error(f"[{self.address}] Insufficient funds!")
        else:
            transaction = contract.functions.requestL2Transaction(
                self.address,
                Web3.to_wei(amount, "ether"),
                "0x",
                gas_limit,
                800,
                [],
                self.address
            ).build_transaction(
                tx_data
            )

            signed_txn = self.sign(transaction)

            txn_hash = self.send_raw_transaction(signed_txn)

            self.wait_until_tx_finished(txn_hash.hex())
            return txn_hash.hex()
