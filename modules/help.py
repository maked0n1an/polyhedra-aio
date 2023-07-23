import time
import asyncio
from loguru import logger
from util.data import DATA


class Help:
    async def check_status_tx(self, tx_hash, ):
        scan = DATA[self.chain]['scan']

        logger.info(
            f'{self.address} - жду подтверждения транзакции {scan}{self.w3.to_hex(tx_hash)}...')

        start_time = int(time.time())
        while True:
            current_time = int(time.time())
            if current_time >= start_time + 150:
                logger.info(
                    f'{self.address} - транзакция не подтвердилась за 150 cекунд, начинаю повторную отправку...')
                return 0
            try:
                status = (await self.w3.eth.get_transaction_receipt(tx_hash))['status']
                if status == 1:
                    return status
                await asyncio.sleep(1)
            except Exception as error:
                await asyncio.sleep(1)

    async def sleep_indicator(self, secs):
        logger.info(f'{self.address} - жду {secs} секунд...')
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