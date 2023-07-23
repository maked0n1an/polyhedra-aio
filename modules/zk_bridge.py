import json
import random
import asyncio
import aiohttp

from web3 import Web3
from fake_useragent import UserAgent
from loguru import logger
from eth_account.messages import encode_defunct
from web3.eth import AsyncEth
from eth_utils import *
from moralis import evm_api

from input_data.config import *
from modules.help import Help
from util.data import *
from util.chain import Chain


class ZkBridge(Help):
    def __init__(self, private_key, chain: Chain, to_chain: Chain, nft, proxy=None):
        self.private_key = private_key
        self.chain = chain
        self.to_chain = random.choice(to_chain) if type(to_chain) == list else to_chain
        self.w3 = Web3(Web3.AsyncHTTPProvider(DATA[self.chain]['rpc']),
                    modules={'eth': (AsyncEth,)}, middlewares=[])
        self.account = self.w3.eth.account.from_key(self.private_key)
        self.address = self.account.address
        self.nft = random.choice(nft) if type(nft) == list else nft
        self.delay = START_DELAY
        self.moralisapi = MORALIS_API_KEY
        self.proxy = proxy or None
        self.nft_address = nfts_addresses[self.nft][self.chain]
        self.bridge_address = nft_lz_bridge_addresses[self.chain] if self.nft == 'Pandra' and self.to_chain != Chain.COMBO else nft_bridge_addresses[self.chain]

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
                    async with session.post('https://api.zkbridge.com/api/signin/validation_message',
                                            json=json_data, headers=headers, proxy=self.proxy) as response:
                        if response.status == 200:
                            msg = json.loads(await response.text())
                            msg = msg['message']
                            msg = encode_defunct(text=msg)
                            sign = self.w3.eth.account.sign_message(msg, private_key=self.private_key)
                            signature = self.w3.to_hex(sign.signature)
                            json_data = {
                                'publicKey': self.address,
                                'signedMessage': signature,
                            }
                            return signature, ua
            except Exception as e:
                logger.error(f'{self.address}:{self.chain.name} - {e}')
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

            except Exception as e:
                logger.error(F'{self.address}:{self.chain.name} - {e}')
                await asyncio.sleep(5)

    async def profile(self):
        headers = await self.sign()
        params = ''
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.zkbridge.com/api/user/profile',
                                       params=params, headers=headers, proxy=self.proxy) as response:
                    if response.status == 200:
                        logger.success(f'{self.address}:{self.chain.name} - успешно авторизовался...')
                        return headers
        except Exception as e:
            logger.error(f'{self.address}:{self.chain.name} - {e}')
            return False

    async def balance_and_get_id(self):
        if self.chain not in [Chain.CORE, Chain.CELO]:
            try:
                api_key = self.moralisapi
                params = {
                    "chain": self.chain.name.lower(), #if u have problem here, check https://docs.moralis.io/web3-data-api/evm/reference/wallet-api/get-nfts-by-wallet
                    "format": "decimal",
                    "token_addresses": [
                        self.nft_address
                    ],
                    "media_items": False,
                    "address": self.address}

                result = evm_api.nft.get_wallet_nfts(api_key=api_key, params=params)

                id_ = int(result['result'][0]['token_id'])
                if id_:
                    logger.success(f'{self.address}:{self.chain.name} - успешно найдена {self.nft} {id_}')
                    return id_
            except Exception as e:
                if 'list index out of range' in str(e):
                    logger.error(f'{self.address}:{self.chain.name} - на кошельке отсутсвует {self.nft}...')
                    return None
                else:
                    logger.error(f'{self.address}:{self.chain.name} - {e}...')
        else:
            try:
                contract = self.w3.eth.contract(address=self.nft_address, abi=zk_nft_abi)
                balance = await contract.functions.balanceOf(self.address).call()
                if balance > 0:
                    totalSupply = await contract.functions.totalSupply().call()
                    id_ = (await contract.functions.tokensOfOwnerIn(self.address, totalSupply - 500, totalSupply).call())[
                        0]
                    return id_
                else:
                    logger.error(f'{self.address}:{self.chain.name} - на кошельке отсутсвует {self.nft}...')
                    return None
            except Exception as e:
                logger.error(f'{self.address}:{self.chain.name} - {e}...')
                await asyncio.sleep(1)

    async def mint(self):
        while True:
            zkNft = self.w3.eth.contract(address=Web3.to_checksum_address(self.nft_address), abi=zk_nft_abi)
            headers = await self.profile()
            if headers is None:
                logger.error("Headers are not set up")
                return False
            try:
                nonce = await self.w3.eth.get_transaction_count(self.address)
                await asyncio.sleep(2)

                tx = await zkNft.functions.mint().build_transaction({
                    'from': self.address,
                    'gas': await zkNft.functions.mint().estimate_gas(
                        {'from': self.address, 'nonce': nonce}),
                    'nonce': nonce,
                    'maxFeePerGas': int(await self.w3.eth.gas_price),
                    'maxPriorityFeePerGas': int((await self.w3.eth.gas_price) * 0.8)
                })
                
                tx = await self.set_gas_price_for_bsc_or_core(tx) 
                scan = DATA[self.chain]['scan']

                logger.info(f'{self.address}:{self.chain.name} - начался минт {self.nft}...')
                sign = self.account.sign_transaction(tx)
                hash = await self.w3.eth.send_raw_transaction(sign.rawTransaction)
                status = await self.check_status_tx(hash, self.chain.name)
                await self.sleep_indicator(5, chain_name=self.chain.name)
                if status == 1:
                    logger.success(
                        f'{self.address}:{self.chain.name} - успешно заминтил {self.nft} : {scan}{self.w3.to_hex(hash)}...')
                    await self.sleep_indicator(random.randint(self.delay[0], self.delay[1]), chain_name=self.chain.name)
                    return headers
                else:
                    logger.info(f'{self.address}:{self.chain.name} - пробую минт еще раз...')
                    await self.mint()
            except Exception as e:
                error = str(e)
                if 'nonce too low' in error or 'already known' in error:
                    logger.success(f'{self.address}:{self.chain.name} - ошибка при минте, пробую еще раз...')
                    await asyncio.sleep(10)
                    await self.mint()
                if 'INTERNAL_ERROR: insufficient funds' in error or 'insufficient funds for gas * price + value' in error:
                    logger.error(
                        f'{self.address}:{self.chain.name} - не хватает денег на газ, заканчиваю работу через 5 секунд...')
                    await asyncio.sleep(5)
                    return False
                elif 'Each address may claim one NFT only. You have claimed already' in error:
                    logger.error(f'{self.address}:{self.chain.name} - {self.nft} можно клеймить только один раз!...')
                    return False
                else:
                    logger.error(f'{self.address}:{self.chain.name} - {e}...')
                    return False

    async def bridge_nft(self):
        time_ = random.randint(self.delay[0], self.delay[1])
        logger.info(f'Начинаю работу через {time_} cекунд...')
        await asyncio.sleep(time_)
        id_ = await self.balance_and_get_id()

        headers = await self.profile()
        if headers is None:
            return False
        
        if id_ == None:
            headers = await self.mint()
            if headers:
                await asyncio.sleep(5)
                id_ = await self.balance_and_get_id()
                if not id_:
                    return self.private_key, self.address, f'not {self.nft} on wallet'
            else:
                return self.private_key, self.address, f'error {self.nft}'

        zkNft = self.w3.eth.contract(address=Web3.to_checksum_address(self.nft_address), abi=zk_nft_abi)

        async def approve_nft(gwei=None):
            # approve
            while True:
                if id_ is False:
                    return False
                try:
                    nonce = await self.w3.eth.get_transaction_count(self.address)
                    await asyncio.sleep(2)

                    tx = await zkNft.functions.approve(
                            Web3.to_checksum_address(self.bridge_address), id_).build_transaction({
                        'from': self.address,
                        'gas': await zkNft.functions.approve(Web3.to_checksum_address(self.bridge_address),
                                                                id_).estimate_gas(
                            {'from': self.address, 'nonce': nonce}),
                        'nonce': nonce,
                        'maxFeePerGas': int(await self.w3.eth.gas_price),
                        'maxPriorityFeePerGas': int((await self.w3.eth.gas_price) * 0.8)
                    })

                    tx = await self.set_gas_price_for_bsc_or_core(tx)
                    scan = DATA[self.chain]['scan']

                    logger.info(f'{self.address}:{self.chain.name} - начинаю апрув {self.nft} {id_}...')
                    sign = self.account.sign_transaction(tx)
                    hash = await self.w3.eth.send_raw_transaction(sign.rawTransaction)
                    status = await self.check_status_tx(hash, self.chain.name)
                    await self.sleep_indicator(5, chain_name=self.chain.name)
                    if status == 1:
                        logger.success(
                            f'{self.address}:{self.chain.name} - успешно апрувнул {self.nft} {id_} : {scan}{self.w3.to_hex(hash)}...')
                        await self.sleep_indicator(random.randint(1, 10), chain_name=self.chain.name)
                        return True
                    else:
                        logger.info(f'{self.address}:{self.chain.name} - пробую апрув еще раз...')
                        await approve_nft()
                except Exception as e:
                    error = str(e)
                    if 'nonce too low' in error or 'already known' in error:
                        logger.info(f'{self.address}:{self.chain.name} - ошибка при апруве, пробую еще раз...')
                        await approve_nft()
                    if 'INTERNAL_ERROR: insufficient funds' in error or 'insufficient funds for gas * price + value' in error:
                        logger.error(
                            f'{self.address}:{self.chain.name} - не хватает денег на газ, заканчиваю работу через 5 секунд...')
                        await asyncio.sleep(5)
                        return False
                    else:
                        logger.error(f'{self.address}:{self.chain.name} - {e}...')
                        await asyncio.sleep(2)
                        return False

        async def bridge_():
            bridge = self.w3.eth.contract(address=Web3.to_checksum_address(self.bridge_address),
                        abi=bridge_lz_abi if self.nft == 'Pandra' and self.to_chain != Chain.COMBO else bridge_abi)

            logger.info(f'{self.address}:{self.chain.name} - начинаю бридж {self.nft} {id_}...')
            while True:
                try:
                    if self.nft == 'Pandra' and self.to_chain != Chain.COMBO:
                        nonce = await self.w3.eth.get_transaction_count(self.address)
                        await asyncio.sleep(2)
                        args = Web3.to_checksum_address(self.nft_address), id_, stargate_ids[
                            self.to_chain], self.address, '0x000100000000000000000000000000000000000000000000000000000000001b7740'
                        lzfee = (await bridge.functions.estimateFee(*args).call())
                        tx = await bridge.functions.transferNFT(*args).build_transaction({
                            'from': self.address,
                            'value': lzfee,
                            'nonce': nonce,
                            'maxFeePerGas': int(await self.w3.eth.gas_price),
                            'maxPriorityFeePerGas': int((await self.w3.eth.gas_price) * 0.8)
                        })
                        tx['gas'] = await self.w3.eth.estimate_gas(tx)
                    else:
                        to_chain = chain_ids[self.to_chain]
                        # to_chain = DATA[self.to_chain]['chain_id'] #chain_ids[self.to]
                        fee = await bridge.functions.fee(to_chain).call()
                        enco = f'0x000000000000000000000000{self.address[2:]}'
                        nonce = await self.w3.eth.get_transaction_count(self.address)

                        tx = await bridge.functions.transferNFT(
                            Web3.to_checksum_address(self.nft_address), id_, to_chain,
                                enco).build_transaction({
                                'from': self.address,
                                'value': fee,
                                'gas': await bridge.functions.transferNFT(
                                    Web3.to_checksum_address(self.nft_address), id_, to_chain,
                                    enco).estimate_gas({'from': self.address, 'nonce': nonce, 'value': fee}),
                                'nonce': nonce,
                                'maxFeePerGas': int(await self.w3.eth.gas_price),
                                'maxPriorityFeePerGas': int((await self.w3.eth.gas_price) * 0.8)
                        })

                    tx = await self.set_gas_price_for_bsc_or_core(tx)
                    scan = DATA[self.chain]['scan']

                    sign = self.account.sign_transaction(tx)
                    hash = await self.w3.eth.send_raw_transaction(sign.rawTransaction)
                    status = await self.check_status_tx(hash, self.chain.name)
                    await self.sleep_indicator(5, chain_name=self.chain.name)
                    if status == 1:
                        logger.success(
                            f'{self.address}:{self.chain.name} - успешно бриджанул {self.nft} {id_} в {self.to_chain.name}: {scan}{self.w3.to_hex(hash)}...')
                        await self.sleep_indicator(random.randint(self.delay[0], self.delay[1]), chain_name=self.chain.name)
                        return self.private_key, self.address, f'successfully bridged {self.nft} to {self.to_chain.name}'
                    else:
                        logger.info(f'{self.address}:{self.chain.name} - пробую бриджить еще раз...')
                        await bridge_()
                except Exception as e:
                    error = str(e)
                    if 'INTERNAL_ERROR: insufficient funds' in error or 'insufficient funds for gas * price + value' in error:
                        logger.error(
                            f'{self.address}:{self.chain.name} - не хватает денег на газ, заканчиваю работу через 5 секунд...')
                        await asyncio.sleep(5)
                        return self.private_key, self.address, f'error bridge {self.nft} - not gas'
                    if 'nonce too low' in error or 'already known' in error:
                        logger.info(f'{self.address}:{self.chain.name} - ошибка при бридже, пробую еще раз...')
                        await bridge_()
                    else:
                        logger.error(f'{self.address}:{self.chain.name} - {e}')
                        return self.private_key, self.address, f'error bridge {self.nft} - {e}'

        if await approve_nft(self):
            return await bridge_()
        else:
            return self.private_key, self.address, f'error approve {self.nft}'