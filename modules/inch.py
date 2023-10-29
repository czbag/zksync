from typing import Union, Dict

import aiohttp
from loguru import logger
from config import INCH_CONTRACT, ZKSYNC_TOKENS
from settings import INCH_API_KEY
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class Inch(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.headers = {"Authorization": f"Bearer {INCH_API_KEY}", "accept": "application/json"}

        self.proxy = ""

        if proxy:
            self.proxy = f"http://{proxy}"

    async def build_tx(self, from_token: str, to_token: str, amount: int, slippage: int):
        url = f"https://api.1inch.dev/swap/v5.2/{await self.w3.eth.chain_id}/swap"

        params = {
            "src": self.w3.to_checksum_address(from_token),
            "dst": self.w3.to_checksum_address(to_token),
            "amount": amount,
            "from": self.address,
            "slippage": slippage,
        }

        if INCH_CONTRACT["use_ref"]:
            params.update({
                "referrer": self.w3.to_checksum_address("0x1c7ff320ae4327784b464eed07714581643b36a7"),
                "fee": 1
            })

        async with aiohttp.ClientSession() as session:
            response = await session.get(url, params=params, headers=self.headers, proxy=self.proxy)

            transaction_data = await response.json()

            return transaction_data

    @retry
    @check_gas
    async def swap(
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
        amount_wei, amount, balance = await self.get_amount(
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
            await self.approve(amount_wei, from_token, INCH_CONTRACT["router"])

        transaction_data = await self.build_tx(from_token, to_token, amount_wei, slippage)

        tx_data = await self.get_tx_data()
        tx_data.update(
            {
                "to": self.w3.to_checksum_address(transaction_data["tx"]["to"]),
                "data": transaction_data["tx"]["data"],
                "value": int(transaction_data["tx"]["value"]),
            }
        )

        signed_txn = await self.sign(tx_data)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())
