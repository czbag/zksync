import random
import sys
from typing import Union

from loguru import logger
from web3 import Web3

from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
from config import ORBITER_CONTRACT


class Orbiter(Account):
    def __init__(self, account_id: int, private_key: str, chain: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain=chain)

        self.bridge_codes = {
            "ethereum": "9001",
            "arbitrum": "9002",
            "polygon": "9006",
            "optimism": "9007",
            "zksync": "9014",
            "nova": "9016",
            "zkevm": "9017",
            "scroll": "9019",
            "base": "9021",
            "linea": "9023",
            "zora": "9030",
        }

    async def get_tx_data(self, value: int):
        tx = {
            "chainId": await self.w3.eth.chain_id,
            "nonce": await self.w3.eth.get_transaction_count(self.address),
            "value": value,
            "from": self.address,
            "gasPrice": await self.w3.eth.gas_price,
        }
        return tx

    @retry
    @check_gas
    async def bridge(
            self,
            destination_chain: str,
            min_amount: float,
            max_amount: float,
            decimal: int,
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

        if ORBITER_CONTRACT == "":
            logger.error(f"[{self.account_id}][{self.address}] Don't have orbiter contract")
            return

        if amount < 0.005 or amount > 5:
            logger.error(
                f"[{self.account_id}][{self.address}] Limit range amount for bridge 0.005 – 5 ETH | {amount} ETH"
            )
        else:
            logger.info(
                f"[{self.account_id}][{self.address}] Bridge {self.chain} –> {destination_chain} | {amount} ETH"
            )

            amount_to_bridge = str(amount_wei).replace(str(amount_wei)[-4:], self.bridge_codes[destination_chain])

            tx_data = await self.get_tx_data(int(amount_to_bridge))
            tx_data.update({"to": ORBITER_CONTRACT})

            balance = await self.w3.eth.get_balance(self.address)

            if tx_data["value"] >= balance:
                logger.error(f"[{self.account_id}][{self.address}] Insufficient funds!")
            else:
                signed_txn = await self.sign(tx_data)

                txn_hash = await self.send_raw_transaction(signed_txn)

                await self.wait_until_tx_finished(txn_hash.hex())
