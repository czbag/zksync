import asyncio
import time
import random
from typing import Union, Dict

from loguru import logger
from web3 import AsyncWeb3
from eth_account import Account as EthereumAccount
from web3.exceptions import TransactionNotFound
from web3.middleware import async_geth_poa_middleware

from config import RPC, ERC20_ABI, ZKSYNC_TOKENS
from settings import GAS_MULTIPLIER
from utils.sleeping import sleep


class Account:
    def __init__(self, account_id: int, private_key: str, chain: str, proxy: Union[None, str]) -> None:
        self.account_id = account_id
        self.private_key = private_key
        self.chain = chain
        self.explorer = RPC[chain]["explorer"]
        self.token = RPC[chain]["token"]

        request_kwargs = {}
        
        if proxy:
            request_kwargs = {"proxy": f"http://{proxy}"}

        self.w3 = AsyncWeb3(
            AsyncWeb3.AsyncHTTPProvider(random.choice(RPC[chain]["rpc"])),
            middlewares=[async_geth_poa_middleware],
            request_kwargs=request_kwargs
        )
        self.account = EthereumAccount.from_key(private_key)
        self.address = self.account.address

    async def get_tx_data(self, value: int = 0):
        tx = {
            "chainId": await self.w3.eth.chain_id,
            "from": self.address,
            "value": value,
            "gasPrice": await self.w3.eth.gas_price,
            "nonce": await self.w3.eth.get_transaction_count(self.address),
        }
        return tx

    def get_contract(self, contract_address: str, abi=None):
        contract_address = self.w3.to_checksum_address(contract_address)

        if abi is None:
            abi = ERC20_ABI

        contract = self.w3.eth.contract(address=contract_address, abi=abi)

        return contract

    async def get_balance(self, contract_address: str) -> Dict:
        contract_address = self.w3.to_checksum_address(contract_address)
        contract = self.get_contract(contract_address)

        symbol = await contract.functions.symbol().call()
        decimal = await contract.functions.decimals().call()
        balance_wei = await contract.functions.balanceOf(self.address).call()

        balance = balance_wei / 10 ** decimal

        return {"balance_wei": balance_wei, "balance": balance, "symbol": symbol, "decimal": decimal}

    async def get_amount(
            self,
            from_token: str,
            min_amount: float,
            max_amount: float,
            decimal: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ) -> [int, float, float]:
        random_amount = round(random.uniform(min_amount, max_amount), decimal)
        random_percent = random.randint(min_percent, max_percent)
        percent = 1 if random_percent == 100 else random_percent / 100

        if from_token == "ETH":
            balance = await self.w3.eth.get_balance(self.address)
            amount_wei = int(balance * percent) if all_amount else self.w3.to_wei(random_amount, "ether")
            amount = self.w3.from_wei(int(balance * percent), "ether") if all_amount else random_amount
        else:
            balance = await self.get_balance(ZKSYNC_TOKENS[from_token])
            amount_wei = int(balance["balance_wei"] * percent) \
                if all_amount else int(random_amount * 10 ** balance["decimal"])
            amount = balance["balance"] * percent if all_amount else random_amount
            balance = balance["balance_wei"]

        return amount_wei, amount, balance

    async def check_allowance(self, token_address: str, contract_address: str) -> float:
        token_address = self.w3.to_checksum_address(token_address)
        contract_address = self.w3.to_checksum_address(contract_address)

        contract = self.w3.eth.contract(address=token_address, abi=ERC20_ABI)
        amount_approved = await contract.functions.allowance(self.address, contract_address).call()

        return amount_approved

    async def approve(self, amount: int, token_address: str, contract_address: str):
        token_address = self.w3.to_checksum_address(token_address)
        contract_address = self.w3.to_checksum_address(contract_address)

        contract = self.w3.eth.contract(address=token_address, abi=ERC20_ABI)

        allowance_amount = await self.check_allowance(token_address, contract_address)

        if amount > allowance_amount or amount == 0:
            logger.success(f"[{self.account_id}][{self.address}] Make approve")

            approve_amount = 2 ** 128 if amount > allowance_amount else 0

            tx_data = await self.get_tx_data()

            transaction = await contract.functions.approve(
                contract_address,
                approve_amount
            ).build_transaction(tx_data)

            signed_txn = await self.sign(transaction)

            txn_hash = await self.send_raw_transaction(signed_txn)

            await self.wait_until_tx_finished(txn_hash.hex())

            await sleep(5, 20)

    async def wait_until_tx_finished(self, hash: str, max_wait_time=180):
        start_time = time.time()
        while True:
            try:
                receipts = await self.w3.eth.get_transaction_receipt(hash)
                status = receipts.get("status")
                if status == 1:
                    logger.success(f"[{self.account_id}][{self.address}] {self.explorer}{hash} successfully!")
                    return True
                elif status is None:
                    await asyncio.sleep(0.3)
                else:
                    logger.error(f"[{self.account_id}][{self.address}] {self.explorer}{hash} transaction failed!")
                    return False
            except TransactionNotFound:
                if time.time() - start_time > max_wait_time:
                    print(f'FAILED TX: {hash}')
                    return False
                await asyncio.sleep(1)

    async def sign(self, transaction):
        gas = await self.w3.eth.estimate_gas(transaction)
        gas = int(gas * GAS_MULTIPLIER)

        transaction.update({"gas": gas})

        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)

        return signed_txn

    async def send_raw_transaction(self, signed_txn):
        txn_hash = await self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return txn_hash
