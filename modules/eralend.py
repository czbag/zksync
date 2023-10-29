from typing import Union

from loguru import logger
from config import ERALEND_CONTRACTS, ERALEND_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account


class Eralend(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.contract = self.get_contract(ERALEND_CONTRACTS["landing"], ERALEND_ABI)

    async def get_deposit_amount(self):
        amount = await self.contract.functions.balanceOfUnderlying(self.address).call()
        return amount

    @retry
    @check_gas
    async def deposit(
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
        amount_wei, amount, balance = await self.get_amount(
            "ETH",
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        tx = {
            "chainId": await self.w3.eth.chain_id,
            "from": self.address,
            "to": self.w3.to_checksum_address(ERALEND_CONTRACTS["landing"]),
            "gasPrice": await self.w3.eth.gas_price,
            "nonce": await self.w3.eth.get_transaction_count(self.address),
            "value": amount_wei,
            "data": "0x1249c58b"
        }

        logger.info(f"[{self.account_id}][{self.address}] Make deposit on Eralend | {amount} ETH")

        signed_txn = await self.sign(tx)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

        if make_withdraw:
            await sleep(sleep_from, sleep_to)

            await self.withdraw()

    @retry
    @check_gas
    async def withdraw(self):
        amount = await self.get_deposit_amount()

        if amount > 0:
            logger.info(
                f"[{self.account_id}][{self.address}] Make withdraw from Eralend | " +
                f"{self.w3.from_wei(amount, 'ether')} ETH"
            )

            tx_data = await self.get_tx_data()

            transaction = await self.contract.functions.redeemUnderlying(amount).build_transaction(tx_data)

            signed_txn = await self.sign(transaction)

            txn_hash = await self.send_raw_transaction(signed_txn)

            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.error(f"[{self.account_id}][{self.address}] Deposit not found")

    @retry
    @check_gas
    async def enable_collateral(self):
        logger.info(f"[{self.account_id}][{self.address}] Enable collateral on Eralend")

        contract = self.get_contract(ERALEND_CONTRACTS["collateral"], ERALEND_ABI)

        tx_data = await self.get_tx_data()

        transaction = await contract.functions.enterMarkets(
            [self.w3.to_checksum_address(ERALEND_CONTRACTS["landing"])]
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    async def disable_collateral(self):
        logger.info(f"[{self.account_id}][{self.address}] Disable collateral on Eralend")

        contract = self.get_contract(ERALEND_CONTRACTS["collateral"], ERALEND_ABI)

        tx_data = await self.get_tx_data()

        transaction = await contract.functions.exitMarket(
            self.w3.to_checksum_address(ERALEND_CONTRACTS["landing"])
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())
