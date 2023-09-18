import random
from typing import Union

from loguru import logger
from web3 import Web3
from config import REACTORFUSION_CONTRACTS, REACTORFUSION_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account


class ReactorFusion(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.contract = self.get_contract(REACTORFUSION_CONTRACTS["landing"], REACTORFUSION_ABI)
        self.tx = {
            "chainId": self.w3.eth.chain_id,
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address),
        }

    def get_deposit_amount(self):
        amount = self.contract.functions.balanceOf(self.address).call()
        return amount

    @retry
    @check_gas
    def deposit(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
            sleep_from: int,
            sleep_to: int,
            make_withdraw: bool,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        amount_wei, amount, balance = self.get_amount(
            "ETH",
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        logger.info(f"[{self.account_id}][{self.address}] Make deposit on ReactorFusion | {amount} ETH")

        self.tx.update({"value": amount_wei})

        transaction = self.contract.functions.mint().build_transaction(self.tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())

        if make_withdraw:
            sleep(sleep_from, sleep_to)

            self.withdraw()

    @retry
    @check_gas
    def withdraw(self):
        amount = self.get_deposit_amount()

        if amount > 0:
            logger.info(
                f"[{self.account_id}][{self.address}] Make withdraw from ReactorFusion | " +
                f"{Web3.from_wei(amount, 'ether')} ETH"
            )

            self.tx.update({"value": 0, "nonce": self.w3.eth.get_transaction_count(self.address)})

            transaction = self.contract.functions.redeem(amount).build_transaction(self.tx)

            signed_txn = self.sign(transaction)

            txn_hash = self.send_raw_transaction(signed_txn)

            self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.error(f"[{self.account_id}][{self.address}] Deposit not found")

    @retry
    @check_gas
    def enable_collateral(self):
        logger.info(f"[{self.account_id}][{self.address}] Enable collateral on ReactorFusion")

        contract = self.get_contract(REACTORFUSION_CONTRACTS["collateral"], REACTORFUSION_ABI)

        transaction = contract.functions.enterMarkets(
            [Web3.to_checksum_address(REACTORFUSION_CONTRACTS["landing"])]
        ).build_transaction(self.tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    def disable_collateral(self):
        logger.info(f"[{self.account_id}][{self.address}] Disable collateral on ReactorFusion")

        contract = self.get_contract(REACTORFUSION_CONTRACTS["collateral"], REACTORFUSION_ABI)

        transaction = contract.functions.exitMarket(
            Web3.to_checksum_address(REACTORFUSION_CONTRACTS["landing"])
        ).build_transaction(self.tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())
