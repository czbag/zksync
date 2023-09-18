from typing import Union

import requests
from loguru import logger
from web3 import Web3
from config import XYSWAP_CONTRACT, ZKSYNC_TOKENS
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class XYSwap(Account):
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

    def get_quote(self, from_token: str, to_token: str, amount: int, slippage: float):
        url = "https://aggregator-api.xy.finance/v1/quote"

        params = {
            "srcChainId": self.w3.eth.chain_id,
            "srcQuoteTokenAddress": Web3.to_checksum_address(from_token),
            "srcQuoteTokenAmount": amount,
            "dstChainId": self.w3.eth.chain_id,
            "dstQuoteTokenAddress": Web3.to_checksum_address(to_token),
            "slippage": slippage
        }

        response = requests.get(url=url, params=params, proxies=self.proxies)

        return response.json()

    def build_transaction(self, from_token: str, to_token: str, amount: int, slippage: float, swap_provider: str):
        url = "https://aggregator-api.xy.finance/v1/buildTx"

        params = {
            "srcChainId": self.w3.eth.chain_id,
            "srcQuoteTokenAddress": Web3.to_checksum_address(from_token),
            "srcQuoteTokenAmount": amount,
            "dstChainId": self.w3.eth.chain_id,
            "dstQuoteTokenAddress": Web3.to_checksum_address(to_token),
            "slippage": slippage,
            "receiver": self.address,
            "srcSwapProvider": swap_provider,
        }

        if XYSWAP_CONTRACT["use_ref"]:
            params.update({
                "affiliate": Web3.to_checksum_address("0x1c7ff320ae4327784b464eed07714581643b36a7"),
                "commissionRate": 10000
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
            f"[{self.account_id}][{self.address}] Swap on XYSwap – {from_token} -> {to_token} | {amount} {from_token}"
        )

        from_token = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE" if from_token == "ETH" else ZKSYNC_TOKENS[from_token]
        to_token = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE" if to_token == "ETH" else ZKSYNC_TOKENS[to_token]

        quote = self.get_quote(from_token, to_token, amount_wei, slippage)

        swap_provider = quote["routes"][0]["srcSwapDescription"]["provider"]

        transaction_data = self.build_transaction(
            from_token,
            to_token,
            amount_wei,
            slippage,
            swap_provider
        )

        if from_token != "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE":
            self.approve(amount_wei, from_token, XYSWAP_CONTRACT["router"])

        self.tx.update(
            {
                "to": transaction_data["tx"]["to"],
                "data": transaction_data["tx"]["data"],
                "value": transaction_data["tx"]["value"],
                "nonce": self.w3.eth.get_transaction_count(self.address)
            }
        )

        signed_txn = self.sign(self.tx)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())
