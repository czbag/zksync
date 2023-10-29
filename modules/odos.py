import aiohttp

from typing import Union, Dict
from loguru import logger

from config import ZERO_ADDRESS, ZKSYNC_TOKENS, ODOS_CONTRACT
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class Odos(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.proxy = ""

        if proxy:
            self.proxy = f"http://{proxy}"

    async def quote(self, from_token: str, to_token: str, amount: int, slippage: float):
        url = "https://api.odos.xyz/sor/quote/v2"

        data = {
            "chainId": await self.w3.eth.chain_id,
            "inputTokens": [
                {
                    "tokenAddress": self.w3.to_checksum_address(from_token),
                    "amount": f"{amount}"
                }
            ],
            "outputTokens": [
                {
                    "tokenAddress": self.w3.to_checksum_address(to_token),
                    "proportion": 1
                }
            ],
            "slippageLimitPercent": slippage,
            "userAddr": self.address,
            "referralCode": 2241664650 if ODOS_CONTRACT["use_ref"] is True else 0,
            "compact": True
        }

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url=url,
                headers={"Content-Type": "application/json"},
                json=data,
                proxy=self.proxy
            )

            if response.status == 200:
                response_data = await response.json()

                return response_data
            else:
                logger.error(f"[{self.account_id}][{self.address}] Bad Odos request")

    async def assemble(self, path_id):
        url = "https://api.odos.xyz/sor/assemble"

        data = {
            "userAddr": self.address,
            "pathId": path_id,
            "simulate": False,
        }

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url=url,
                headers={"Content-Type": "application/json"},
                json=data,
                proxy=self.proxy
            )

            if response.status == 200:
                response_data = await response.json()

                return response_data
            else:
                logger.error(f"[{self.account_id}][{self.address}] Bad Odos request")

    @retry
    @check_gas
    async def swap(
            self,
            from_token: str,
            to_token: str,
            min_amount: float,
            max_amount: float,
            decimal: int,
            slippage: float,
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
            f"[{self.account_id}][{self.address}] Swap on Odos – {from_token} -> {to_token} | {amount} {from_token}"
        )

        from_token = ZERO_ADDRESS if from_token == "ETH" else ZKSYNC_TOKENS[from_token]
        to_token = ZERO_ADDRESS if to_token == "ETH" else ZKSYNC_TOKENS[to_token]

        if from_token != ZERO_ADDRESS:
            await self.approve(amount_wei, from_token, self.w3.to_checksum_address(ODOS_CONTRACT["router"]))

        quote_data = await self.quote(from_token, to_token, amount_wei, slippage)

        transaction_data = await self.assemble(quote_data["pathId"])

        transaction = transaction_data["transaction"]

        tx_data = await self.get_tx_data()
        tx_data.update(
            {
                "to": self.w3.to_checksum_address(transaction["to"]),
                "data": transaction["data"],
                "value": int(transaction["value"]),
            }
        )

        signed_txn = await self.sign(tx_data)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())
