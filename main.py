import asyncio
import csv
import random
import sys
import concurrent.futures

from termcolor import colored
from art import text2art
from loguru import logger

from modules.zk_bridge import ZkBridge
from modules.zk_message import ZkMessage
from input_data.config import *
from util.activity import Activity
from util.data import DATA
from util.rpcs import Rpc
from util.chain import Chain
from util.file_readers import *
from util.activities import *
from info import nfts_addresses


async def run_wallet(private_key, proxy, i):
    web3 = Rpc.getWeb3(proxy, Rpc.BSC)
    only_ip_proxy = proxy.split('@')[1]

    address = web3.eth.account.from_key(private_key).address
    logger.success(f"Current proxy  ({i}/{len(PROXIES)}): {only_ip_proxy}")
    logger.success(f"Current wallet ({i}/{len(PRIVATE_KEYS)}): {address}")

    activities = [
        # Activity.GREENFIELD_TESTNET_MINT,
        Activity.OP_BNB_MINT_OPERATIONS,
        # Activity.PANDRA_CODECONQUEROR_OPERATIONS,
        # Activity.PANDRA_PIXELBROWLER_OPERATIONS,
        # Activity.PANDRA_MELODYMAVEN_OPERATIONS,
        # Activity.PANDRA_ECOGUARDIAN_OPERATIONS,
        # Activity.MAINNET_ALPHA_NFT_CORE_DAO_OPERATIONS,
        # Activity.BSC_POLYGON_ZKMESSENGER,
        # Activity.ZK_LIGHT_CLIENT_NFT_OPERATIONS,
        # Activity.BNB_CHAIN_LUBAN_NFT_OPERATIONS
    ]
    random.shuffle(activities)

    for activity in activities:
        await run_activity(activity, private_key, proxy, address)

async def run_activity(activity: Activity, private_key, proxy, address):
    if activity == Activity.OP_BNB_MINT_OPERATIONS:
        await do_op_bnb_operations(private_key=private_key, proxy=proxy, address=address)

async def main():
    if len(PRIVATE_KEYS) == 0:
        logger.error("Don't imported private keys in private_keys.txt!...")
        return
    if shuffle_keys:
        random.shuffle(PRIVATE_KEYS)
    if MORALIS_API_KEY == '':
        logger.error('Не вставлен апи ключ моралис!...')
        return

    logger.info('The bot has been started')

    key_proxy_pairs = zip(PRIVATE_KEYS, PROXIES * len(PRIVATE_KEYS))
    tasks = []

    for i, (private_key, proxy) in enumerate(key_proxy_pairs, 1):
        tasks.append(asyncio.create_task(run_wallet(private_key, proxy, i)))

    res = await asyncio.gather(*tasks)

    logger.info("The bot has ended its work")

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     key_proxy_pairs = data
    #     futures = []
    #     i = 0
    #     
        # for i, (private_key, proxy) in enumerate(key_proxy_pairs, 1):
        #     run_wallet(private_key=private_key, proxy=proxy, i=i)
    #     concurrent.futures.wait(futures)    

    # logger.success(f'Успешно сделал {len(keys)} кошельков...')
    # logger.success(f'muнетинг закончен...')
    # print(f'\n{" " * 32}автор - https://t.me/iliocka{" " * 32}\n')
    # print(f'\n{" " * 32}donate - EVM 0xFD6594D11b13C6b1756E328cc13aC26742dBa868{" " * 32}\n')
    # print(f'\n{" " * 32}donate - trc20 TMmL915TX2CAPkh9SgF31U4Trr32NStRBp{" " * 32}\n')

if __name__ == "__main__":
    authors = ["@1liochka1", "@maked0n1an"]
    random.shuffle(authors)
    art = text2art(text="DropBot", font="standart")
    print(colored(art, "light_blue"))
    print(colored(f"Authors: {authors[0]}, {authors[1]}\n", "light_cyan"))
    logger.remove()
    logger.add(
        sys.stderr,
        format="<lm>{time:YYYY-MM-DD HH:mm:ss}</lm> | <level>{level: <8}</level>| <lw>{message}</lw>",
    )
    asyncio.run(main())

# async def main():
#     if len(keys) == 0:
#         logger.error('Не вставлены приватные ключи в файл keys.txt!...')
#         return
#     for i in rpcs.values():
#         if i == '':
#             logger.error('Не вставлены rpc в файле config!...')
#             return
#     if not MODE:
#         logger.error('Не выбран модуль!...')
#         return
#     if shuffle_keys:
#         random.shuffle(keys)
#     logger.info(f'Начинаю работу на {len(keys)} кошельках...')
#     batches = [keys[i:i + wallets_in_batch] for i in range(0, len(keys), wallets_in_batch)]

#     print(f'\n{" " * 32}автор - https://t.me/iliocka{" " * 32}\n')

#     tasks = []
#     for batch in batches:
#         for key in batch:
#             if proxies:
#                 proxy = random.choice(proxies)
#             else:
#                 proxy = None
#             if MODE == 'nftbridger':
#                 if MORALIS_API_KEY == '':
#                     logger.error('Не вставлен апи ключ моралис!...')
#                     return
#                 if nft not in nfts_addresses.keys():
#                     logger.error('Неправильно вставлено название нфт!...')
#                     return
#                 logger.info('Запущен режим минта и бриджа нфт...')
#                 zk = ZkBridge(key, DELAY, chain, to, MORALIS_API_KEY, proxy)
#                 tasks.append(zk.bridge_nft())

#             if MODE == 'messenger':
#                 logger.info('Запущен режим отправки сообщений...')
#                 zk = ZkMessage(key, chain, to, DELAY, proxy)
#                 tasks.append(zk.send_msg())

#         res = await asyncio.gather(*tasks)

#         for res_ in res:
#             key, address_, info = res_
#             await write_to_csv(key, address_, info)

#         tasks = []

#     logger.success(f'Успешно сделал {len(keys)} кошельков...')
#     logger.success(f'muнетинг закончен...')
#     print(f'\n{" " * 32}автор - https://t.me/iliocka{" " * 32}\n')
#     print(f'\n{" " * 32}donate - EVM 0xFD6594D11b13C6b1756E328cc13aC26742dBa868{" " * 32}\n')
#     print(f'\n{" " * 32}donate - trc20 TMmL915TX2CAPkh9SgF31U4Trr32NStRBp{" " * 32}\n')

# def bridger(mode:str):
#     tasks = []
#     for batch in batches:
#         for key in batch:            
#             if MODE == 'nftbridger':
#                 if MORALIS_API_KEY == '':
#                     logger.error('Не вставлен апи ключ моралис!...')
#                     return
#                 if nft not in nfts_addresses.keys():
#                     logger.error('Неправильно вставлено название нфт!...')
#                     return
#                 logger.info('Запущен режим минта и бриджа нфт...')
#                 zk = ZkBridge(key, DELAY, chain, to, MORALIS_API_KEY, proxy)
#                 tasks.append(zk.bridge_nft())

#             if MODE == 'messenger':
#                 logger.info('Запущен режим отправки сообщений...')
#                 zk = ZkMessage(key, chain, to, DELAY, proxy)
#                 tasks.append(zk.send_msg())

#         res = await asyncio.gather(*tasks)

#         for res_ in res:
#             key, address_, info = res_
#             await write_to_csv(key, address_, info)

#         tasks = []

# async def write_to_csv(key, address, result):
#     with open('result.csv', 'a', newline='') as file:
#         writer = csv.writer(file)

#         if file.tell() == 0:
#             writer.writerow(['key', 'address', 'result'])

#         writer.writerow([key, address, result])

# if __name__ == '__main__':
#     asyncio.run(main())
