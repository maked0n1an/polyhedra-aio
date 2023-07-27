import asyncio
import csv
import random
import sys
import concurrent.futures

from termcolor import colored
from art import text2art
from web3 import Web3
from loguru import logger as global_logger

from input_data.config import *
from modules.zk_bridge import ZkBridge
from modules.zk_message import ZkMessage
from modules.help import Help
from util.activity import Activity
from util.data import *
from util.session import Session
from util.chain import Chain
from util.file_utils import *
from util.operations import *

async def run_wallet(wallet_name, private_key, proxy, i):
    session = Session.get_web3_session_via_proxy(proxy)
    web3 = Web3(provider=Web3.HTTPProvider(DATA[Chain.BSC]['rpc'], session=session))
    only_ip_proxy = proxy.split('@')[1]

    address = web3.eth.account.from_key(private_key).address
    logger.success(f"Current proxy  ({i}/{len(PROXIES)}): {only_ip_proxy}")
    logger.success(f"Current wallet ({i}/{len(PRIVATE_KEYS)}): {wallet_name} : {address}")

    activities_list = [
        Activity.GREENFIELD_TESTNET_MINT,
        Activity.OP_BNB_OPERATIONS,
        # Activity.PANDRA_CODECONQUEROR_OPERATIONS,
        # Activity.PANDRA_PIXELBROWLER_OPERATIONS,
        # Activity.PANDRA_MELODYMAVEN_OPERATIONS,
        # Activity.PANDRA_ECOGUARDIAN_OPERATIONS,
        Activity.MAINNET_ALPHA_NFT_CORE_DAO_OPERATIONS,
        Activity.BSC_POLYGON_ZKMESSENGER,
        Activity.ZK_LIGHT_CLIENT_NFT_OPERATIONS,
        Activity.BNB_CHAIN_LUBAN_NFT_OPERATIONS
    ]

    random.shuffle(activities_list)

    for activity in activities_list:
        await run_activity(activity, wallet_name, private_key, proxy, address)

async def run_activity(activity: Activity, wallet_name, private_key, proxy, address):
    i = 0

    if activity == Activity.GREENFIELD_TESTNET_MINT:
        logger.info(f"{address}: Запущен минт Greenfield NFT")
        await do_greenfield_mint_nft(private_key=private_key, wallet_name=wallet_name, proxy=proxy)

    if activity == Activity.OP_BNB_OPERATIONS:
        logger.info(f"{address}: Запущен минт и бридж opBNB NFT")        
        await do_op_bnb_operations(private_key=private_key, wallet_name=wallet_name, proxy=proxy)
        
    if activity == Activity.PANDRA_CODECONQUEROR_OPERATIONS:
        i += 1
        logger.info(f"{address}: Запущен минт и бридж Pandra CodeConqueror ({i}/4 из Pandra'с)")
        await do_pandra_codeconquer_operations(private_key=private_key, wallet_name=wallet_name, proxy=proxy) 

    if activity == Activity.PANDRA_PIXELBROWLER_OPERATIONS:
        i += 1
        logger.info(f"{address}: Запущен минт и бридж Pandra PixelBowler ({i}/4 из Pandra'с)")
        await do_pandra_pixelbowler_operations(private_key=private_key, wallet_name=wallet_name, proxy=proxy) 

    if activity == Activity.PANDRA_MELODYMAVEN_OPERATIONS:
        i += 1
        logger.info(f"{address}: Запущен минт и бридж Pandra MelodyMaven ({i}/4 из Pandra'с)")
        await do_pandra_melodymaven_operations(private_key=private_key, wallet_name=wallet_name, proxy=proxy) 

    if activity == Activity.PANDRA_ECOGUARDIAN_OPERATIONS:
        i += 1
        logger.info(f"{address}: Запущен минт и бридж Pandra EcoGuardian ({i}/4 из Pandra'с)")
        await do_pandra_ecoguardian_operations(private_key=private_key, wallet_name=wallet_name, proxy=proxy) 

    if activity == Activity.MAINNET_ALPHA_NFT_CORE_DAO_OPERATIONS:
        logger.info(f"{address}: Запущен минт и бридж Alpha NFT Core DAO")
        await do_alpha_nft_core_dao_operations(private_key=private_key, wallet_name=wallet_name, proxy=proxy) 
        
    if activity == Activity.BSC_POLYGON_ZKMESSENGER:
        logger.info(f"{address}: Запущена активность с отправкой сообщений ZkMessenger")
        await do_messenger(private_key=private_key, wallet_name=wallet_name, proxy=proxy) 
        logger.info(f"{address}: skipped this activity")

    if activity == Activity.BNB_CHAIN_LUBAN_NFT_OPERATIONS:
        logger.info(f"{address}: Запущен минт и бридж BNB Luban NFT")
        await do_bnb_luban_operations(private_key=private_key, wallet_name=wallet_name, proxy=proxy) 

    if activity == Activity.ZK_LIGHT_CLIENT_NFT_OPERATIONS:
        logger.info(f"{address}: Запущен минт и бридж ZkLightClient NFT")
        await do_zk_light_client_operations(private_key=private_key, wallet_name=wallet_name, proxy=proxy) 
    
    return i

async def main():
    if MORALIS_API_KEY == '':
        logger.error("Don't imported Moralis API key!...")
        return
    if len(PRIVATE_KEYS) == 0:
        logger.error("Don't imported private keys in 'private_keys.txt'!")
        return
    if len(PROXIES) == 0:
        logger.error("Don't imported proxies in 'proxies.txt'!")
        return
    if len(WALLET_NAMES) == 0:
        logger.error("Please insert names into wallet_names.txt")
        return
    if len(PRIVATE_KEYS) != len(WALLET_NAMES):
        logger.error("The wallet names' amount must be equal to private keys' amount")
        return

    logger.info('The bot has been started')

    wallet_key_proxy_tuple = {
        pair: proxy for pair, proxy in zip(zip(WALLET_NAMES, PRIVATE_KEYS), PROXIES * len(PRIVATE_KEYS))
    }
    tasks = []

    if IS_SHUFFLE_KEYS:
        random.shuffle(wallet_key_proxy_tuple)

    # for i, (private_key, proxy) in enumerate(key_proxy_pairs, 1):
    #     tasks.append(asyncio.create_task(run_wallet(private_key, wallet_name, proxy, i)))

    for i, ((wallet_name, private_key), proxy) in enumerate(wallet_key_proxy_tuple.items(), 1):
        task = asyncio.create_task(run_wallet(wallet_name, private_key, proxy, i))
        tasks.append(task)    

    # for (private_key, proxy), activities_list_item in zip(key_proxy_pairs, activities_list):
    #     tasks.append(asyncio.create_task(run_wallet(private_key, proxy, activities_list_item )))

    res = await asyncio.gather(*tasks)

    logger.info("The bot has ended its work")

if __name__ == "__main__":
    authors = ["@1liochka1", "@maked0n1an"]
    random.shuffle(authors)
    art = text2art(text="DropBot", font="standart")
    print(colored(art, "cyan"))
    print(colored(f"Authors: {authors[0]}, {authors[1]}\n", "cyan"))
    # logger.add(
    #     sys.stderr,
    #     format="<lm>{time:YYYY-MM-DD HH:mm:ss}</lm> | <level>{level: <8}</level>| <lw>{message}</lw>",
    # )
    log_file_name = 'main.log'
        
    main_log(log_file_name)

    asyncio.run(main())