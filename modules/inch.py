from typing import Union

import requests
from loguru import logger
from web3 import Web3
from config import INCH_CONTRACT, ZKSYNC_TOKENS
from settings import INCH_API_KEY
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class Inch(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.url = f"https://api.1inch.dev/swap/v5.2/{self.w3.eth.chain_id}"
        self.headers = { "Authorization": f"Bearer {INCH_API_KEY}", "accept": "application/json" }

        self.proxies = {}

        if proxy:
            self.proxies.update({"http": f"http://{proxy}", "https": f"http://{proxy}"})

        self.tx = {
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

    def build_tx(self, from_token: str, to_token: str, amount: int, slippage: int):
        url = f"{self.url}/swap"
        params = {
            "src": Web3.to_checksum_address(from_token),
            "dst": Web3.to_checksum_address(to_token),
            "amount": amount,
            "from": self.address,
            "slippage": slippage,
        }

        if INCH_CONTRACT["use_ref"]:
            params.update({
                "referrer": Web3.to_checksum_address("0x1c7ff320ae4327784b464eed07714581643b36a7"),
                "fee": 1
            })

        response = requests.get(url, params=params, headers=self.headers, proxies=self.proxies)

        transaction = response.json()

        return transaction

    @retry
    @check_gas
    def swap(
            self,
            from_token: str,
            to_token: str,
            min_amount: float,
            max_amount: float,
            decimal: int,
            slippage: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        amount_wei, amount, balance = self.get_amount(
            from_token,
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        logger.info(
            f"[{self.account_id}][{self.address}] Swap on 1inch – {from_token} -> {to_token} | {amount} {from_token}"
        )

        from_token = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE" if from_token == "ETH" else ZKSYNC_TOKENS[from_token]
        to_token = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE" if to_token == "ETH" else ZKSYNC_TOKENS[to_token]

        if from_token != "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE":
            self.approve(amount_wei, from_token, INCH_CONTRACT["router"])

        transaction_data = self.build_tx(from_token, to_token, amount_wei, slippage)

        transaction_data["tx"].update(
            {
                "to": Web3.to_checksum_address(transaction_data["tx"]["to"]),
                "value": int(transaction_data["tx"]["value"]),
                "gasPrice": int(transaction_data["tx"]["gasPrice"]),
                "nonce": self.w3.eth.get_transaction_count(self.address)
            }
        )

        signed_txn = self.sign(transaction_data["tx"])

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())
