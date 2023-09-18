import json
import os
import random
from typing import Union

from web3 import Web3
from loguru import logger
from zksync2.manage_contracts.contract_encoder_base import ContractEncoder, JsonConfiguration
from zksync2.manage_contracts.precompute_contract_deployer import PrecomputeContractDeployer
from zksync2.module.module_builder import ZkSyncBuilder
from zksync2.core.types import Token, EthBlockParams
from zksync2.signer.eth_signer import PrivateKeyEthSigner
from zksync2.transaction.transaction_builders import TxCreate2Contract, TxWithdraw

from config import RPC, CONTRACT_PATH, ZKSYNC_BRIDGE_ABI, ZKSYNC_BRIDGE_CONTRACT, ZKSYNC_TOKENS, WETH_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class ZkSync(Account):
    def __init__(self, account_id: int, private_key: str, proxy: Union[None, str], chain: str) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy, chain=chain)

        request_kwargs = {}
        if proxy:
            request_kwargs = {"proxies": {"https": f"http://{proxy}"}}

        self.zk_w3 = ZkSyncBuilder.build(random.choice(RPC["zksync"]["rpc"]))
        self.zk_w3.provider = Web3.HTTPProvider(random.choice(RPC["zksync"]["rpc"]), request_kwargs=request_kwargs)

    def get_tx_data(self, value: int):
        tx = {
            "chainId": self.w3.eth.chain_id,
            "nonce": self.w3.eth.get_transaction_count(self.address),
            "from": self.address,
            "value": value
        }
        return tx

    @retry
    @check_gas
    def deposit(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
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

        logger.info(f"[{self.account_id}][{self.address}] Bridge to ZkSync | {amount} ETH")

        gas_limit = random.randint(700000, 1000000)

        contract = self.get_contract(ZKSYNC_BRIDGE_CONTRACT, ZKSYNC_BRIDGE_ABI)
        base_cost = contract.functions.l2TransactionBaseCost(self.w3.eth.gas_price, gas_limit, 800).call()

        tx_data = self.get_tx_data(amount_wei + base_cost)

        transaction = contract.functions.requestL2Transaction(
            self.address,
            Web3.to_wei(amount, "ether"),
            "0x",
            gas_limit,
            800,
            [],
            self.address
        ).build_transaction(
            tx_data
        )

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    def withdraw(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
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

        logger.info(f"[{self.account_id}][{self.address}] Bridge {amount} ETH to Ethereum")

        if amount_wei < balance:
            withdrawal_tx = TxWithdraw(
                web3=self.zk_w3,
                token=Token.create_eth(),
                amount=amount_wei,
                gas_limit=random.randint(1900000, 2200000),
                account=self.account
            )

            estimated_gas = self.zk_w3.zksync.eth_estimate_gas(withdrawal_tx.tx)

            tx = withdrawal_tx.estimated_gas(estimated_gas)

            signed = self.account.sign_transaction(tx)

            raw_tx_hash = self.zk_w3.zksync.send_raw_transaction(signed.rawTransaction)

            tx_hash = self.zk_w3.to_hex(raw_tx_hash)

            logger.success(
                f"[{self.account_id}][{self.address}] Bridged from ZkSync to " +
                f"Ethereum {amount} ETH is successfully – " +
                f"{self.explorer}{tx_hash}"
            )
        else:
            logger.error(f"Withdraw transaction to L1 network failed | error: insufficient funds!")

    @retry
    @check_gas
    def wrap_eth(self, min_amount: float, max_amount: float, decimal: int, all_amount: bool, min_percent: int,
                 max_percent: int):
        amount_wei, amount, balance = self.get_amount(
            "ETH",
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        weth_contract = self.get_contract(ZKSYNC_TOKENS["WETH"], WETH_ABI)

        logger.info(f"[{self.account_id}][{self.address}] Wrap {amount} ETH")

        tx = {
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address),
            "value": amount_wei
        }

        transaction = weth_contract.functions.deposit().build_transaction(tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    def unwrap_eth(self, min_amount: float, max_amount: float, decimal: int, all_amount: bool, min_percent: int,
                   max_percent: int):
        amount_wei, amount, balance = self.get_amount(
            "WETH",
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        weth_contract = self.get_contract(ZKSYNC_TOKENS["WETH"], WETH_ABI)

        logger.info(f"[{self.account_id}][{self.address}] Unwrap {amount} ETH")

        tx = {
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

        transaction = weth_contract.functions.withdraw(amount_wei).build_transaction(tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())


    def mint(self, contract_address: str, amount: int):
        logger.info(f"[{self.account_id}][{self.address}] Starting to mint token")

        with open(CONTRACT_PATH) as file:
            contract_abi = json.load(file)

        contract = self.get_contract(contract_address, contract_abi["abi"])

        tx = {
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.address)
        }

        contract_txn = contract.functions.mint(self.address, Web3.to_wei(amount, "ether")).build_transaction(tx)

        signed_txn = self.sign(contract_txn)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())

    @staticmethod
    def get_token_data():
        return "".join(random.sample([chr(i) for i in range(65, 91)], random.randint(3, 6)))

    @retry
    @check_gas
    def deploy_contract(
            self,
            token_name: str,
            token_symbol: str,
            min_mint: int,
            max_mint: int,
            random_token_data: bool
    ):
        logger.info(f"Starting to deploy token contract")

        token_data = self.get_token_data()

        token_name = token_data if random_token_data else token_name
        token_symbol = token_data if random_token_data else token_symbol

        contract_args = {"name_": token_name, "symbol_": token_symbol, "decimals_": 18}

        amount = random.randint(min_mint, max_mint)

        signer = PrivateKeyEthSigner(self.account, self.zk_w3.zksync.chain_id)

        nonce = self.zk_w3.zksync.get_transaction_count(
            self.address, EthBlockParams.PENDING.value
        )

        random_salt = os.urandom(32)

        deployer = PrecomputeContractDeployer(self.zk_w3)

        token_contract = ContractEncoder.from_json(self.zk_w3, CONTRACT_PATH, JsonConfiguration.STANDARD)

        encoded_constructor = token_contract.encode_constructor(**contract_args)

        precomputed_address = deployer.compute_l2_create2_address(
            sender=self.address,
            bytecode=token_contract.bytecode,
            constructor=encoded_constructor,
            salt=random_salt
        )

        gas_price = self.zk_w3.zksync.gas_price

        create2_contract = TxCreate2Contract(
            web3=self.zk_w3,
            chain_id=self.zk_w3.zksync.chain_id,
            nonce=nonce,
            from_=self.address,
            gas_limit=random.randint(2900000, 3100000),
            gas_price=gas_price,
            bytecode=token_contract.bytecode,
            salt=random_salt,
            call_data=encoded_constructor
        )

        estimate_gas = self.zk_w3.zksync.eth_estimate_gas(create2_contract.tx)

        tx_712 = create2_contract.tx712(estimate_gas)

        signed_message = signer.sign_typed_data(tx_712.to_eip712_struct())

        msg = tx_712.encode(signed_message)

        tx_hash = self.zk_w3.zksync.send_raw_transaction(msg)

        tx_receipt = self.zk_w3.zksync.wait_for_transaction_receipt(
            tx_hash, timeout=240, poll_latency=0.5
        )

        contract_address = tx_receipt["contractAddress"]

        logger.success(
            f"[{self.account_id}][{self.address}] Contract has been successfully deployed – [{contract_address}]"
        )

        if precomputed_address.lower() != contract_address.lower():
            raise RuntimeError("Precomputed contract address does now match with deployed contract address")

        self.mint(contract_address, amount)
