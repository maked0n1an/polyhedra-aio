import json
import random
import asyncio
import aiohttp
import time

from web3 import Web3
from loguru import logger
from fake_useragent import UserAgent
from eth_account.messages import encode_defunct
from web3.eth import AsyncEth
from eth_utils import *
from moralis import evm_api

from input_data.config import *
from modules.help import Help
from util.data import *
from util.chain import Chain
from util.file_utils import *


class ZkMessage(Help):
    def __init__(self, private_key, wallet_name, chain: str, to_chain: str, proxy=None):
        self.privatekey = private_key
        self.wallet_name = wallet_name
        self.chain = chain
        self.to_chain = random.choice(to_chain) if type(to_chain) == list else to_chain
        self.w3 = Web3(Web3.AsyncHTTPProvider(DATA[self.chain]['rpc']),
                    modules={'eth': (AsyncEth,)}, middlewares=[])
        self.scan = DATA[self.chain]['scan']
        self.account = self.w3.eth.account.from_key(self.privatekey)
        self.address = self.account.address
        self.proxy = proxy or None
        self.logger = write_to_logs(self.wallet_name)
    
    async def auth(self):
        ua = UserAgent()
        ua = ua.random
        headers = {
            'authority': 'api.zkbridge.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://zkbridge.com',
            'referer': 'https://zkbridge.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': ua,
        }

        json_data = {
            'publicKey': self.address.lower(),
        }
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                            'https://api.zkbridge.com/api/signin/validation_message',
                            json=json_data, headers=headers, proxy=self.proxy) as response:
                        if response.status == 200:
                            msg = json.loads(await response.text())
                            msg = msg['message']
                            msg = encode_defunct(text=msg)
                            sign = self.w3.eth.account.sign_message(msg, private_key=self.privatekey)
                            signature = self.w3.to_hex(sign.signature)
                            json_data = {
                                'publicKey': self.address,
                                'signedMessage': signature,
                            }
                            return signature, ua
            except Exception as e:
                self.logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - {e}')
                await asyncio.sleep(5)

    async def sign(self):
        # sign msg
        signature, ua = await self.auth()
        headers = {
            'authority': 'api.zkbridge.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://zkbridge.com',
            'referer': 'https://zkbridge.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': ua,
        }
        json_data = {
            'publicKey': self.address.lower(),
            'signedMessage': signature,
        }
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post('https://api.zkbridge.com/api/signin',
                                            json=json_data, headers=headers, proxy=self.proxy) as response:
                        if response.status == 200:
                            token = (json.loads(await response.text()))['token']
                            headers['authorization'] = f'Bearer {token}'
                            return headers
                        await asyncio.sleep(random.randint(1, 10))

            except Exception as e:
                self.logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - {e}')
                await asyncio.sleep(5)

    async def profile(self):
        headers = await self.sign()
        params = ''
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.zkbridge.com/api/user/profile',
                                       params=params, headers=headers, proxy=self.proxy) as response:
                    if response.status == 200:
                        self.logger.success(f'{self.wallet_name} | {self.address} | {self.chain} - успешно авторизовался...')
                        return headers
        except Exception as e:
            self.logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - {e}')
            return False

    async def check_status_lz(self):
        contract_msg = Web3.to_checksum_address(sender_msgs[self.chain])
        mailer = self.w3.eth.contract(address=contract_msg, abi=mailer_abi)
        try:
            if not await mailer.functions.layerZeroPaused().call():
                self.logger.success(f'{self.wallet_name} | {self.address} | {self.chain} - L0 активен...')
                return True
            else:
                self.logger.info(f'{self.wallet_name} | {self.address} | {self.chain} - L0 не активен, жду 30 секунд...')
                await asyncio.sleep(30)
        except Exception as e:
            await asyncio.sleep(2)

    async def msg(self, headers, contract_msg, msg, from_chain, to_chain, tx_hash):

        timestamp = time.time()

        json_data = {
            'message': msg,
            'mailSenderAddress': contract_msg,
            'receiverAddress': self.address,
            'receiverChainId': to_chain,
            'sendTimestamp': timestamp,
            'senderAddress': self.address,
            'senderChainId': from_chain,
            'senderTxHash': tx_hash,
            'sequence': random.randint(4500, 5000),
            'receiverDomainName': '',
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.zkbridge.com/api/user/profile',
                                       json=json_data, headers=headers, proxy=self.proxy) as response:
                    if response.status == 200:
                        self.logger.success(f'{self.wallet_name} | {self.address} | {self.chain} - cообщение подтвержденно...')
                        return True
        except Exception as e:
            self.logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - {e}')
            return False

    async def create_msg(self):
        n = random.randint(1, 10)
        string = []
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(word_site) as response:
                    if response.status == 200:
                        for i in range(n):
                            WORDS = [g for g in (await response.text()).split()]
                            string.append(random.choice(WORDS))

                        msg = ' '.join(string)
                        return msg
        except Exception as e:
            await asyncio.sleep(1)
            return await self.create_msg()

    async def send_msg(self):
        time_ = random.randint(DELAY[0], DELAY[1])
        self.logger.info(f'{self.wallet_name} | {self.address} - Начинаю работу через {time_} cекунд...')
        await asyncio.sleep(time_)
        data = await self.profile()
        if data:
            headers = data
        else:
            return self.privatekey, self.address, 'error - not auth'
        contract_msg = Web3.to_checksum_address(sender_msgs[self.chain])
        lz_id = stargate_ids[self.to_chain]
        to_chain_id = chain_ids[self.to_chain]
        from_chain_id = chain_ids[self.chain]
        message = await self.create_msg()
        dst_address = Web3.to_checksum_address(dst_addresses[self.to_chain])
        lzdst_address = Web3.to_checksum_address(lzdst_addresses[self.to_chain])
        mailer = self.w3.eth.contract(address=contract_msg, abi=mailer_abi)
        native_ = DATA[self.chain]['token']

        while True:
            try:
                zkFee = await mailer.functions.fees(to_chain_id).call()
                lz_status = await self.check_status_lz()
                fee = await mailer.functions.estimateLzFee(lz_id, self.address, message).call()
                value = fee + zkFee
                self.logger.info(
                    f'{self.wallet_name} | {self.address} | {self.chain} - начинаю отправку сообщения в {self.to_chain} через L0, предполагаемая комса - {(fee + zkFee) / 10 ** 18} {native_}...')
                nonce = await self.w3.eth.get_transaction_count(self.address)
                
                tx = await mailer.functions.sendMessage(to_chain_id, dst_address, lz_id, lzdst_address, fee,
                                                        self.address,
                                                        message).build_transaction({
                    'from': self.address,
                    'value': value,
                    'gas': await mailer.functions.sendMessage(to_chain_id, dst_address, lz_id, lzdst_address, fee,
                                                              self.address,
                                                              message).estimate_gas(
                        {'from': self.address, 'nonce': nonce,
                         'value': value}),
                    'nonce': nonce,
                    'maxFeePerGas': int(await self.w3.eth.gas_price),
                    'maxPriorityFeePerGas': int((await self.w3.eth.gas_price) * 0.8)
                })

                tx = await self.set_gas_price_for_bsc_or_core(tx)

                sign = self.account.sign_transaction(tx)
                hash_ = await self.w3.eth.send_raw_transaction(sign.rawTransaction)
                status = await self.check_status_tx(self.wallet_name, self.address, self.chain, hash_)
                await self.sleep_indicator(self.chain)
                if status == 1:
                    self.logger.success(
                        f'{self.wallet_name} | {self.address} | {self.chain} - успешно отправил сообщение {message} в {self.to_chain} : {self.scan}{self.w3.to_hex(hash_)}...')
                    await asyncio.sleep(5)
                    msg = await self.msg(headers, contract_msg, message, from_chain_id, to_chain_id,
                                         self.w3.to_hex(hash_))
                    if msg:
                        await self.sleep_indicator(self.chain)
                        return self.privatekey, self.address, f'success sending message to {self.to_chain}'
                else:
                    self.logger.info(f'{self.wallet_name} | {self.address} | {self.chain} - пробую еще раз отправлять сообщение...')
                    await self.send_msg()

            except Exception as e:
                error = str(e)
                if 'nonce too low' in error or 'already known' in error or 'Message already executed' in error:
                    await asyncio.sleep(5)
                    await self.send_msg()
                elif 'INTERNAL_ERROR: insufficient funds' in error or 'insufficient funds for gas * price + value' in error:
                    self.logger.error(
                        f'{self.wallet_name} | {self.address} | {self.chain} - не хватает денег на газ, заканчиваю работу через 5 секунд...')
                    await asyncio.sleep(5)
                    return self.privatekey, self.address, 'error - not gas'
                else:
                    self.logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - {e}...')
                    return self.privatekey, self.address, 'error'