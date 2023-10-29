from typing import Union, Dict

from loguru import logger
from config import STARGATE_CONTRACT, STARGATE_ABI, ZKSYNC_TOKENS
from utils.gas_checker import check_gas
from utils.sleeping import sleep
from .account import Account
from .syncswap import SyncSwap


class Stargate(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str]) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain="zksync")

        self.proxy = proxy

        self.brdige_contract = self.get_contract(STARGATE_CONTRACT, STARGATE_ABI)

    async def get_lz_estimate_fee(self, amount: int):
        get_fee = await self.brdige_contract.functions.estimateSendFee(
            self.w3.to_checksum_address(ZKSYNC_TOKENS["MAV"]),
            102,
            self.address,
            amount,
            False,
            "0x",
            {
                "callerBps": 0,
                "caller": "0x0000000000000000000000000000000000000000",
                "partnerId": "0x0000",
            }
        ).call()

        return get_fee[0]

    async def swap(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
            slippage: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        syncswap = SyncSwap(self.account_id, self.private_key, self.proxy)
        await syncswap.swap(
            "ETH",
            "MAV",
            min_amount,
            max_amount,
            decimal,
            slippage,
            all_amount,
            min_percent,
            max_percent
        )

        balance = await self.get_balance(ZKSYNC_TOKENS["MAV"])

        if balance["balance_wei"] > 0:
            return True
        return False

    @check_gas
    async def bridge(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
            slippage: int,
            sleep_from: int,
            sleep_to: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        balance = await self.get_balance(ZKSYNC_TOKENS["MAV"])

        logger.info(f"[{self.account_id}][{self.address}] Make stargate bridge {balance['balance']} MAV to BNB")

        if balance["balance_wei"] > 0:
            await self.approve(balance["balance_wei"], ZKSYNC_TOKENS["MAV"], STARGATE_CONTRACT)

            fee = await self.get_lz_estimate_fee(balance["balance_wei"])

            tx_data = await self.get_tx_data(fee)

            transaction = await self.brdige_contract.functions.sendOFT(
                self.w3.to_checksum_address(ZKSYNC_TOKENS["MAV"]),
                102,
                self.address,
                balance["balance_wei"],
                0,
                self.address,
                "0x0000000000000000000000000000000000000000",
                "0x000100000000000000000000000000000000000000000000000000000000000186a0",
                {
                    "callerBps": 0,
                    "caller": "0x0000000000000000000000000000000000000000",
                    "partnerId": "0x0000",
                }
            ).build_transaction(tx_data)

            signed_txn = await self.sign(transaction)

            txn_hash = await self.send_raw_transaction(signed_txn)

            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.error(f"[{self.account_id}][{self.address}] Insufficient funds!")

            result_swap = await self.swap(
                min_amount,
                max_amount,
                decimal,
                slippage,
                all_amount,
                min_percent,
                max_percent
            )

            if result_swap:
                await sleep(sleep_from, sleep_to)

                await self.bridge(
                    min_amount,
                    max_amount,
                    decimal,
                    slippage,
                    sleep_from,
                    sleep_to,
                    all_amount,
                    min_percent,
                    max_percent
                )
            else:
                logger.error(f"[{self.account_id}][{self.address}] Insufficient funds for swap!")
