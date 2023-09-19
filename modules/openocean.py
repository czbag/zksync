from typing import Union

import requests
from loguru import logger
from web3 import Web3
from config import OPENOCEAN_CONTRACT, ZKSYNC_TOKENS
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class OpenOcean(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.proxies = {}

        if proxy:
            self.proxies.update({"http": f"http://{proxy}", "https": f"http://{proxy}"})

        self.tx = {
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

    def build_transaction(self, from_token: str, to_token: str, amount: int, slippage: float):
        url = "https://open-api.openocean.finance/v3/324/swap_quote"

        params = {
            "inTokenAddress": Web3.to_checksum_address(from_token),
            "outTokenAddress": Web3.to_checksum_address(to_token),
            "amount": amount,
            "gasPrice": Web3.from_wei(self.w3.eth.gas_price, "gwei"),
            "slippage": slippage,
            "account": self.address,
        }

        if OPENOCEAN_CONTRACT["use_ref"]:
            params.update({
                "referrer": Web3.to_checksum_address("0x1c7ff320ae4327784b464eed07714581643b36a7"),
                "referrerFee": 1
            })

        response = requests.get(url=url, params=params, proxies=self.proxies)

        return response.json()

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
            f"[{self.account_id}][{self.address}] Swap on OpenOcean – {from_token} -> {to_token} | {amount} {from_token}"
        )

        from_token = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE" if from_token == "ETH" else ZKSYNC_TOKENS[from_token]
        to_token = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE" if to_token == "ETH" else ZKSYNC_TOKENS[to_token]

        transaction_data = self.build_transaction(
            from_token,
            to_token,
            amount,
            slippage,
        )

        if from_token != "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE":
            self.approve(amount_wei, from_token, OPENOCEAN_CONTRACT["router"])

        self.tx.update(
            {
                "to": transaction_data["data"]["to"],
                "data": transaction_data["data"]["data"],
                "value": int(transaction_data["data"]["value"]),
                "nonce": self.w3.eth.get_transaction_count(self.address)
            }
        )

        signed_txn = self.sign(self.tx)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())
