import random
from typing import Union

from loguru import logger
from web3 import Web3
from config import BUNGEE_ABI, BUNGEE_CONTRACT
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
from utils.bungee_data import get_bungee_data


def get_bungee_limits() -> Union[dict, bool]:
    bungee_data = get_bungee_data()

    try:
        limits = [chain_data for chain_data in bungee_data if chain_data["name"] == "zkSync"][0]["limits"]

        return limits
    except:
        return False


class Bungee(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.contract = self.get_contract(BUNGEE_CONTRACT, BUNGEE_ABI)
        self.chain_ids = {
            "BSC": 56,
            "OPTIMISM": 10,
            "GNOSIS": 100,
            "POLYGON": 137,
            "BASE": 8453,
            "ARBITRUM": 42161,
            "AVALANCHE": 43114,
            "AURORA": 1313161554,
            "ZK_EVM": 1101,
        }

    def get_tx_data(self, amount: int):
        tx = {
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address),
            "value": amount
        }
        return tx

    @retry
    @check_gas
    def refuel(self, chain_list: list, random_amount: bool):
        limits = get_bungee_limits()

        to_chain = random.choice(chain_list)

        to_chain_limits = [
            chain for chain in limits if chain["chainId"] == self.chain_ids[to_chain] and chain["isEnabled"]
        ]

        if to_chain_limits:
            min_amount = int(to_chain_limits[0]["minAmount"])
            max_amount = int(to_chain_limits[0]["maxAmount"])

            amount = random.randint(min_amount, max_amount) if random_amount else min_amount

            logger.info(
                f"[{self.account_id}][{self.address}] Make refuel to " +
                f"{to_chain.title()} | {Web3.from_wei(amount, 'ether')} ETH"
            )

            transaction = self.contract.functions.depositNativeToken(
                self.chain_ids[to_chain],
                self.address
            ).build_transaction(self.get_tx_data(amount))

            signed_txn = self.sign(transaction)

            txn_hash = self.send_raw_transaction(signed_txn)

            self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.error(f"[{self.account_id}][{self.address}] Bungee refuel destination chain inactive!")
