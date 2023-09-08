import json
import time
import random
import asyncio
import aiohttp
import requests
import copy
import os

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


class ZkBridge(Help):
    def __init__(self, private_key, wallet_name, chain: Chain, to_chain: Chain, nft, proxy=None):
        self.private_key = private_key
        self.wallet_name = wallet_name
        self.chain = chain
        self.to_chain = random.choice(to_chain) if type(to_chain) == list else to_chain
        self.w3 = Web3(Web3.AsyncHTTPProvider(DATA[self.chain]['rpc']),
                    modules={'eth': (AsyncEth,)}, middlewares=[])
        self.account = self.w3.eth.account.from_key(self.private_key)
        self.address = self.account.address
        self.nft = random.choice(nft) if type(nft) == list else nft
        self.nft_address = nfts_addresses[self.nft][self.chain]
        self.bridge_address = nft_lz_bridge_addresses[self.chain] if self.nft == 'Pandra' and self.to_chain not in non_lz_chains else nft_bridge_addresses[self.chain]
        self.moralisapi = MORALIS_API_KEY
        self.proxy = proxy or None
        self.logger = write_to_logs(self.wallet_name)

    def _setup_headers_and_useragent(self):
        ua = UserAgent()
        ua = ua.random
        headers = {
            'authority': 'api.zkbridge.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7',
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

        return ua, headers

    async def auth(self):
        ua, headers = self._setup_headers_and_useragent()

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
                            return signature, ua, headers
            except Exception as e:
                self.logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - {e}')
                await asyncio.sleep(5)

    async def sign(self):
        # sign msg
        signature, ua, headers = await self.auth()
        
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

    async def balance_and_get_id(self):
        if self.chain not in [Chain.CORE, Chain.CELO, Chain.BSC_TESTNET, Chain.COMBO_TESTNET, Chain.OP_BNB]:
            try:
                api_key = self.moralisapi
                params = {
                    "chain": self.chain, #if u have problem here, check https://docs.moralis.io/web3-data-api/evm/reference/wallet-api/get-nfts-by-wallet
                    "format": "decimal",
                    "token_addresses": [
                        self.nft_address
                    ],
                    "media_items": False,
                    "address": self.address}

                result = evm_api.nft.get_wallet_nfts(api_key=api_key, params=params)

                id_ = int(result['result'][0]['token_id'])
                if id_:
                    self.logger.success(f'{self.wallet_name} | {self.address} | {self.chain} - успешно найдена "{self.nft}"[{id_}]')
                    return id_  
            except Exception as e:
                if 'list index out of range' in str(e):
                    self.logger.warning(f'{self.wallet_name} | {self.address} | {self.chain} - на кошельке отсутсвует "{self.nft}"...')
                    return None
                else:
                    self.logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - {e}...')         
        else:
            try:
                token_id = await self.check_nft_presence(self.w3, self.nft_address, self.address, zk_nft_abi)
                return token_id  
            except Exception as e:
                if 'list index out of range' in str(e):
                    self.logger.warning(f'{self.wallet_name} | {self.address} | {self.chain} - на кошельке отсутсвует "{self.nft}"...')
                    return None
                else:
                    self.logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - {e}...')                     

    async def mint(self):
        while True:
            zkNft = self.w3.eth.contract(address=Web3.to_checksum_address(self.nft_address), abi=zk_nft_abi)
            headers = await self.profile()
            if headers is None:
                self.logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - headers are not set up')
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

                self.logger.info(f'{self.wallet_name} | {self.address} | {self.chain} - начался минт "{self.nft}"...')
                sign = self.account.sign_transaction(tx)
                tx_hash = await self.w3.eth.send_raw_transaction(sign.rawTransaction)
                status = await self.check_status_tx(self.wallet_name, self.address, self.chain, tx_hash)
                await self.sleep_indicator(self.chain)
                if status == 1:
                    self.logger.success(
                        f'{self.wallet_name} | {self.address} | {self.chain} - успешно заминтил "{self.nft}" : {scan}{self.w3.to_hex(tx_hash)}...')

                    time_ = random.randint(DELAY[0], DELAY[1]) 

                    if self.chain in [Chain.POLYGON, Chain.CORE] and self.to_chain in non_lz_chains:                        
                        time_ = BIG_DELAY

                    self.logger.info(f'{self.wallet_name} | {self.address} - начинаю работу через {time_} cекунд...')
                    await self.sleep_indicator(self.chain, time_)         
                    
                    return headers
                else:
                    self.logger.info(f'{self.wallet_name} | {self.address} | {self.chain} - пробую минт еще раз...')
                    await self.mint()
            except Exception as e:
                error = str(e)
                if 'nonce too low' in error or 'already known' in error:
                    self.logger.success(f'{self.wallet_name} | {self.address} | {self.chain} - ошибка при минте, пробую еще раз...')
                    await asyncio.sleep(10)
                    await self.mint()
                if 'INTERNAL_ERROR: insufficient funds' in error or 'insufficient funds for gas * price + value' in error:
                    self.logger.error(
                        f'{self.wallet_name} | {self.address} | {self.chain} - не хватает денег на газ, заканчиваю работу через 5 секунд...')
                    await asyncio.sleep(5)
                    return False
                elif 'Each address may claim one NFT only. You have claimed already' in error:
                    self.logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - "{self.nft}" можно клеймить только один раз!...')
                    return False
                else:
                    self.logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - {e}...')
                    return False

    async def claim_nft(self, sender_tx_hash):
        try:
            ua = UserAgent()
            ua = ua.random
            headers = {
                'authority': 'api.zkbridge.com',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7',
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
                'tx_hash': sender_tx_hash,
                'chain_id': chain_ids[self.chain]
            }

            response = requests.post(
                'https://api.zkbridge.com/api/v2/receipt_proof/generate',
                headers=headers,
                json=json_data
            )

            src_chain_id = json.loads(response.text)['chain_id']
            src_block_hash = json.loads(response.text)['block_hash']
            log_index = json.loads(response.text)['proof_index']
            mpt_proof = json.loads(response.text)['proof_blob']

            self.w3 = Web3(Web3.AsyncHTTPProvider(DATA[self.to_chain]['rpc']),
                        modules={'eth': (AsyncEth,)}, middlewares=[])

            self.account = self.w3.eth.account.from_key(self.private_key)
            self.address = self.account.address

            claim_address = self.w3.to_checksum_address(nft_claim_addresses[self.to_chain])
            claim_contract = self.w3.eth.contract(address=claim_address, abi=claim_abi)

            nonce = await self.w3.eth.get_transaction_count(self.address)
            chain_id = DATA[self.to_chain]['chain_id']

            await self.sleep_indicator(self.chain, 5)
            self.logger.info(f'{self.wallet_name} | {self.address} | {self.to_chain} - билдим транзакцию...')

            tx = await claim_contract.functions.validateTransactionProof(src_chain_id, src_block_hash, log_index, mpt_proof
                                                                ).build_transaction({
                'from': self.address,
                'gasPrice': await self.w3.eth.gas_price,
                'chainId': chain_id,
                'nonce': nonce
            })

            self.logger.info(f'{self.wallet_name} | {self.address} | {self.to_chain} - сбилдили транзакцию...')

            await self.sleep_indicator(self.chain, 3)
            self.logger.info(f'{self.wallet_name} | {self.address} | {self.to_chain} - начался клейм "{self.nft}"...')

            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.private_key)
            tx_hash = await self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            scan = DATA[self.to_chain]['scan']
            status = await self.check_status_tx(self.wallet_name, self.address, self.to_chain, tx_hash)
            
            if status == 1:
                self.logger.success(f'{self.wallet_name} | {self.address} | {self.to_chain} - успешно заклеймил "{self.nft}": {scan}{self.w3.to_hex(tx_hash)}...')
                time_ = random.randint(DELAY[0], DELAY[1])

                self.logger.info(f'{self.wallet_name} | {self.address} - начинаю работу через {time_} cекунд...')
                await self.sleep_indicator(self.chain, time_)  

                return True
        except Exception as e:
            error = str(e)
            if 'nonce too low' in error or 'already known' in error:
                self.logger.success(f'{self.wallet_name} | {self.address} | {self.chain} - ошибка при минте, пробую еще раз...')
                await asyncio.sleep(10)
                await self.mint()
            elif 'INTERNAL_ERROR: insufficient funds' in error or 'insufficient funds for gas * price + value' in error:
                self.logger.error(
                    f'{self.wallet_name} | {self.address} | {self.chain} - не хватает денег на газ, заканчиваю работу через 5 секунд...')
                await asyncio.sleep(5)
                return False
            elif 'Each address may claim one NFT only. You have claimed already' in error:
                self.logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - "{self.nft}" можно клеймить только один раз!...')
                return False
            elif 'chain_id' in error:
                self.logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - "{self.nft}" не клеймим, ибо смотреть ошибку при бридже выше...')
                return False
            else:
                self.logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - {e}...')
                return False

    async def bridge_nft(self):
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
                    return self.private_key, self.address, f'not "{self.nft}" on wallet'
            else:
                return self.private_key, self.address, f'error "{self.nft}"'

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
                        'maxPriorityFeePerGas': int((await self.w3.eth.gas_price) * 0.9)
                    })

                    tx = await self.set_gas_price_for_bsc_or_core(tx)
                    scan = DATA[self.chain]['scan']

                    self.logger.info(f'{self.wallet_name} | {self.address} | {self.chain} - начинаю апрув "{self.nft}"[{id_}]...')
                    sign = self.account.sign_transaction(tx)
                    tx_hash = await self.w3.eth.send_raw_transaction(sign.rawTransaction)
                    status = await self.check_status_tx(self.wallet_name, self.address, self.chain, tx_hash)
                    await self.sleep_indicator(self.chain)
                    if status == 1:
                        self.logger.success(
                            f'{self.wallet_name} | {self.address} | {self.chain} - успешно апрувнул "{self.nft}"[{id_}] : {scan}{self.w3.to_hex(tx_hash)}...')
                        await self.sleep_indicator(self.chain)
                        return True
                    else:
                        self.logger.info(f'{self.wallet_name} | {self.address} | {self.chain} - пробую апрув еще раз...')
                        await approve_nft()
                except Exception as e:
                    error = str(e)
                    if 'nonce too low' in error or 'already known' in error:
                        self.logger.info(f'{self.wallet_name} | {self.address} | {self.chain} - ошибка при апруве, пробую еще раз...')
                        await approve_nft()
                    if 'INTERNAL_ERROR: insufficient funds' in error or 'insufficient funds for gas * price + value' in error:
                        self.logger.error(
                            f'{self.wallet_name} | {self.address} | {self.chain} - не хватает денег на газ, заканчиваю работу через 5 секунд...')
                        await asyncio.sleep(5)
                        return False
                    else:
                        self.logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - {e}...')
                        await asyncio.sleep(2)
                        return False

        async def bridge_():
            bridge = self.w3.eth.contract(address=Web3.to_checksum_address(self.bridge_address),
                        abi=bridge_lz_abi if self.nft == 'Pandra' and self.to_chain not in non_lz_chains else bridge_abi)

            self.logger.info(f'{self.wallet_name} | {self.address} | {self.chain} - начинаю бридж "{self.nft}"[{id_}]...')
            while True:
                try:
                    if self.nft == 'Pandra' and self.to_chain not in (Chain.COMBO_TESTNET, Chain.OP_BNB):
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
                    tx_hash = await self.w3.eth.send_raw_transaction(sign.rawTransaction)
                    status = await self.check_status_tx(self.wallet_name, self.address, self.chain, tx_hash)
                    await self.sleep_indicator(self.chain)
                    
                    if status == 1:
                        self.logger.success(
                            f'{self.wallet_name} | {self.address} | {self.chain} - успешно бриджанул "{self.nft}"[{id_}] в {self.to_chain}: {scan}{self.w3.to_hex(tx_hash)}...')
                        time_ = random.randint(DELAY[0], DELAY[1])

                        self.logger.info(f'{self.wallet_name} | {self.address} - начинаю работу через {time_} cекунд...')
                        await self.sleep_indicator(self.chain, time_)  

                        return self.w3.to_hex(tx_hash)
                    else:
                        self.logger.info(f'{self.wallet_name} | {self.address} | {self.chain} - пробую бриджить еще раз...')
                        await bridge_()
                except Exception as e:
                    error = str(e)
                    if 'INTERNAL_ERROR: insufficient funds' in error or 'insufficient funds for gas * price + value' in error:
                        self.logger.error(
                            f'{self.wallet_name} | {self.address} | {self.chain} - не хватает денег на газ, заканчиваю работу через 5 секунд...')
                        await asyncio.sleep(5)
                        return self.private_key, self.address, f'error bridge "{self.nft}" - not gas'
                    if 'nonce too low' in error or 'already known' in error:
                        self.logger.info(f'{self.wallet_name} | {self.address} | {self.chain} - ошибка при бридже, пробую еще раз...')
                        await bridge_()
                    else:
                        self.logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - {e}')
                        return self.private_key, self.address, f'error bridge "{self.nft}" - {e}'

        if await approve_nft(self):
            return await bridge_()
        else:
            return self.private_key, self.address, f'error approve "{self.nft}"'