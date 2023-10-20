from random import choice
from time import time

from web3 import Web3
from web3.eth import AsyncEth
from web3.exceptions import TransactionNotFound

from data.data import PROXIES, ARB_ADDRESS, ARB_GOVERNOR_ADDRESS
from modules.utils import check_gas, logger, sleeping, info
from config import USE_PROXY, RPC


class Account:
    def __init__(
            self,
            private_key: str,
            id: int
    ):
        request_kwargs = {}
        
        if USE_PROXY:
            proxy = PROXIES[private_key]
            _proxy = f'{proxy[proxy.find(":")+6:]}@{proxy[:proxy.find(":")+5]}'
            request_kwargs = {"proxy": f"http://{_proxy}"}

        self.id = id
        self.w3 = Web3(Web3.AsyncHTTPProvider(choice(RPC), request_kwargs=request_kwargs),
            modules={"eth": (AsyncEth,)})
        self.private_key = private_key
        self.address = Web3.to_checksum_address(self.w3.eth.account.from_key(private_key=private_key).address)
        self.arb_address = self.w3.to_checksum_address(ARB_ADDRESS)
        self.governor_address = self.w3.to_checksum_address(ARB_GOVERNOR_ADDRESS)


    async def get_max_priority_fee_per_gas(self, block: dict) -> int:
        block_number = block['number']
        latest_block_transaction_count = await self.w3.eth.get_block_transaction_count(block_number)
        max_priority_fee_per_gas_list = []

        for i in range(latest_block_transaction_count):
            try:
                transaction = await self.w3.eth.get_transaction_by_block(block_number, i)
                if 'maxPriorityFeePerGas' in transaction:
                    max_priority_fee_per_gas_list.append(transaction['maxPriorityFeePerGas'])
            except:
                continue

        if not max_priority_fee_per_gas_list:
            max_priority_fee_per_gas = await self.w3.eth.max_priority_fee
        else:
            max_priority_fee_per_gas_list.sort()
            max_priority_fee_per_gas = max_priority_fee_per_gas_list[len(max_priority_fee_per_gas_list) // 2]

        return max_priority_fee_per_gas


    @check_gas
    async def send_transaction(
            self,
            to,
            increase_gas=1.1,
            data=None,
            value=None
        ):

        try:
            tx = {
                'chainId': await self.w3.eth.chain_id,
                'nonce': await self.w3.eth.get_transaction_count(self.address),
                'from': self.address,
                'to': Web3.to_checksum_address(to),
            }

            if data:
                tx['data'] = data

            last_block = await self.w3.eth.get_block('latest')

            max_priority_fee_per_gas = await self.get_max_priority_fee_per_gas(block=last_block)

            base_fee = int(last_block['baseFeePerGas'] * increase_gas)

            max_fee_per_gas = base_fee + max_priority_fee_per_gas

            tx['maxPriorityFeePerGas'] = max_priority_fee_per_gas
            tx['maxFeePerGas'] = max_fee_per_gas

            if value:
                tx['value'] = value

            tx['gas'] = int(await self.w3.eth.estimate_gas(tx) * increase_gas)

            sign = self.w3.eth.account.sign_transaction(tx, self.private_key)

            tx_hash = await self.w3.eth.send_raw_transaction(sign.rawTransaction)

            if await self.verif_tx(tx_hash):
                return True

        except Exception as error:
            if 'insufficient funds' in str(error).lower() or 'gas required exceeds allowance' in str(error).lower():
                logger.error(f'{self.id} | doesn`t have enough ETH')
            else:
                logger.error(f'{self.id} | error: {error}')


    async def verif_tx(self, tx_hash) -> bool:
        await info(
            f"{self.id} | Waiting transaction: "
            f"https://arbiscan.io/tx/{tx_hash.hex()}", "magenta"
            )
        
        start_time = time()
        while True:
            try:
                data = await self.w3.eth.get_transaction_receipt(tx_hash)
                status = data.get("status")

                if status == 1:
                    logger.success(f'{self.id} | Transaction accepted')
                    return True
                elif not status:
                    await sleeping([0.5, 1])
                else:
                    logger.error(f'{self.id} | Transaction failed')
                    return

            except TransactionNotFound:
                if time() - start_time > 200:
                    logger.error(f'{self.id} | Transaction failed')
                    return
