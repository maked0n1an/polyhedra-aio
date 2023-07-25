import asyncio
import csv
import random
import sys
import concurrent.futures

from termcolor import colored
from art import text2art
from loguru import logger
from web3 import Web3

from modules.zk_bridge import ZkBridge
from modules.zk_message import ZkMessage
from input_data.config import *
from util.activity import Activity
from util.data import *
from util.session import Session
from util.chain import Chain
from util.file_readers import *
from util.operations import *


async def run_wallet(private_key, proxy, i):
    session = Session.get_web3_session_via_proxy(proxy)
    web3 = Web3(provider=Web3.HTTPProvider(DATA[Chain.BSC]['rpc'], session=session))
    only_ip_proxy = proxy.split('@')[1]

    address = web3.eth.account.from_key(private_key).address
    logger.success(f"Current proxy  ({i}/{len(PROXIES)}): {only_ip_proxy}")
    logger.success(f"Current wallet ({i}/{len(PRIVATE_KEYS)}): {address}")

    activities_list = [
        # Activity.GREENFIELD_TESTNET_MINT,
        # Activity.OP_BNB_MINT_OPERATIONS,
        # Activity.PANDRA_CODECONQUEROR_OPERATIONS,
        # Activity.PANDRA_PIXELBROWLER_OPERATIONS,
        # Activity.PANDRA_MELODYMAVEN_OPERATIONS,
        # Activity.PANDRA_ECOGUARDIAN_OPERATIONS,
        # Activity.MAINNET_ALPHA_NFT_CORE_DAO_OPERATIONS,
        # Activity.BSC_POLYGON_ZKMESSENGER,
        # Activity.ZK_LIGHT_CLIENT_NFT_OPERATIONS,
        # Activity.BNB_CHAIN_LUBAN_NFT_OPERATIONS
    ]
    random.shuffle(activities_list)

    i = 0

    for activity in activities_list:
        await run_activity(activity, private_key, proxy, address)

async def run_activity(activity: Activity, private_key, proxy, address):
    i = 0

    if activity == Activity.GREENFIELD_TESTNET_MINT:
        logger.info(f"{address}: Запущен минт Greenfield NFT")
        await do_greenfield_mint_nft(private_key=private_key, proxy=proxy)    
    if activity == Activity.OP_BNB_MINT_OPERATIONS:
        logger.info(f"{address}: Запущен минт и бридж opBNB NFT")
        await do_op_bnb_operations(private_key=private_key, proxy=proxy)
    if activity == Activity.PANDRA_CODECONQUEROR_OPERATIONS:
        i += 1
        logger.info(f"{address}: Запущен минт и бридж Pandra CodeConqueror ({i}/4 из Pandra'с)")
        await do_pandra_codeconquer_operations(private_key=private_key, proxy=proxy)
    if activity == Activity.PANDRA_PIXELBROWLER_OPERATIONS:
        i += 1
        logger.info(f"{address}: Запущен минт и бридж Pandra PixelBowler ({i}/4 из Pandra'с)")
        await do_pandra_pixelbowler_operations(private_key=private_key, proxy=proxy)
    if activity == Activity.PANDRA_MELODYMAVEN_OPERATIONS:
        i += 1
        logger.info(f"{address}: Запущен минт и бридж Pandra MelodyMaven ({i}/4 из Pandra'с)")
        await do_pandra_melodymaven_operations(private_key=private_key, proxy=proxy)
    if activity == Activity.PANDRA_ECOGUARDIAN_OPERATIONS:
        i += 1
        logger.info(f"{address}: Запущен минт и бридж Pandra EcoGuardian ({i}/4 из Pandra'с)")
        await do_pandra_ecoguardian_operations(private_key=private_key, proxy=proxy)
    if activity == Activity.MAINNET_ALPHA_NFT_CORE_DAO_OPERATIONS:
        logger.info(f"{address}: Запщуен минт и бридж Alpha NFT Core DAO")
        await do_alpha_nft_core_dao_operations(private_key=private_key, proxy=proxy)
    
    return i

async def main():
    if len(PRIVATE_KEYS) == 0:
        logger.error("Don't imported private keys in 'private_keys.txt'!")
        return
    if len(PROXIES) == 0:
        logger.error("Don't imported proxies in 'proxies.txt'!")
        return
    if MORALIS_API_KEY == '':
        logger.error("Don't imported Moralis API key!...")
        return
    if shuffle_keys:
        random.shuffle(PRIVATE_KEYS)

    logger.info('The bot has been started')

    key_proxy_pairs = zip(PRIVATE_KEYS, PROXIES * len(PRIVATE_KEYS))
    tasks = []

    for i, (private_key, proxy) in enumerate(key_proxy_pairs, 1):
        tasks.append(asyncio.create_task(run_wallet(private_key, proxy, i)))

    res = await asyncio.gather(*tasks)

    logger.info("The bot has ended its work")

if __name__ == "__main__":
    authors = ["@1liochka1", "@maked0n1an"]
    random.shuffle(authors)
    art = text2art(text="DropBot", font="standart")
    print(colored(art, "cyan"))
    print(colored(f"Authors: {authors[0]}, {authors[1]}\n", "cyan"))
    logger.remove()
    logger.add(
        sys.stderr,
        format="<lm>{time:YYYY-MM-DD HH:mm:ss}</lm> | <level>{level: <8}</level>| <lw>{message}</lw>",
    )
    asyncio.run(main())