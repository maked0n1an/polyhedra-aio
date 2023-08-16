import time
import asyncio
import random
from web3 import Web3
from loguru import logger
from input_data.config import *
from util.data import *
from util.chain import Chain


class Help:
    async def check_status_tx(self, wallet_name, address, chain, tx_hash):
        scan = DATA[chain]['scan']

        logger.info(
            f'{wallet_name} | {address} | {chain} - жду подтверждения транзакции {scan}{self.w3.to_hex(tx_hash)}...')

        start_time = int(time.time())
        while True:
            current_time = int(time.time())
            if current_time >= start_time + MAX_WAIT_TIME:
                logger.warning(
                    f'{self.wallet_name} | {self.address} | {self.chain} - транзакция не подтвердилась за {MAX_WAIT_TIME} cекунд, начинаю повторную отправку...')
                return 0
            try:
                status = (await self.w3.eth.get_transaction_receipt(tx_hash))['status']
                if status == 1:
                    return status
                await asyncio.sleep(1)
            except Exception as error:
                await asyncio.sleep(1)

    async def sleep_initial_indicator(wallet_name, address):
        secs = random.randint(INITIAL_DELAY[0], INITIAL_DELAY[1])
        logger.info(f'{wallet_name} | {address} - пауза в виде {secs} секунд...')
        await asyncio.sleep(secs)

    async def sleep_indicator(self, chain, secs=5):
        logger.info(f'{self.wallet_name} | {self.address} | {self.chain} - жду {secs} секунд...')
        await asyncio.sleep(secs)

    async def set_gas_price_for_bsc_or_core(self, tx):
        if self.chain == Chain.BSC:
            del tx['maxFeePerGas']
            del tx['maxPriorityFeePerGas']
            tx['gasPrice'] = self.w3.to_wei(1, 'gwei')
        if self.chain == Chain.CORE:
            del tx['maxFeePerGas']
            del tx['maxPriorityFeePerGas']
            tx['gasPrice'] = await self.w3.eth.gas_price

        return tx

    async def check_nft_presence(self, w3, nft_address, account_address, nft_abi):
        try:
            contract = self.w3.eth.contract(address=Web3.to_checksum_address(self.nft_address), abi=nft_abi)
            balance = await contract.functions.balanceOf(self.address).call()
            if balance > 0:
                totalSupply = await contract.functions.totalSupply().call()
                id_ = (await contract.functions.tokensOfOwnerIn(self.address, totalSupply - 2000, totalSupply).call())[0]
                self.logger.success(f'{self.wallet_name} | {self.address} | {self.chain} - успешно найдена \'{self.nft}\'[{id_}]')
                return id_
            else:
                self.logger.warning(f'{self.wallet_name} | {self.address} | {self.chain} - на кошельке отсутсвует "{self.nft}"...')
                return None
        except Exception as e:
            if 'list index out of range' in str(e):
                self.logger.warning(f'{self.wallet_name} | {self.address} | {self.chain} - на кошельке отсутсвует "{self.nft}"...')
                return None
            else:
                self.logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - {e}...')