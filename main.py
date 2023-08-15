import asyncio
import random

from termcolor import colored
from art import text2art
from web3 import Web3
from loguru import logger

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
    logger.success(f"Current wallet ({i}/{len(PRIVATE_KEYS)}): {wallet_name} | {address}")

    random.shuffle(activities_list)

    await Help.sleep_initial_indicator(wallet_name, address)

    for activity in activities_list:
        await run_activity(activity, wallet_name, private_key, proxy)

async def run_activity(activity: Activity, wallet_name, private_key, proxy):

    if activity == Activity.GREENFIELD_TESTNET_MINT:
        await do_greenfield_mint_nft(wallet_name=wallet_name,private_key=private_key, proxy=proxy)

    if activity == Activity.OP_BNB_OPERATIONS:    
        await do_op_bnb_operations(private_key=private_key, wallet_name=wallet_name, proxy=proxy)
        
    if activity == Activity.PANDRA_CODECONQUEROR_OPERATIONS:
        await do_pandra_codeconquer_operations(private_key=private_key, wallet_name=wallet_name, proxy=proxy) 

    if activity == Activity.PANDRA_PIXELBROWLER_OPERATIONS:
        await do_pandra_pixelbowler_operations(private_key=private_key, wallet_name=wallet_name, proxy=proxy) 

    if activity == Activity.PANDRA_MELODYMAVEN_OPERATIONS:
        await do_pandra_melodymaven_operations(private_key=private_key, wallet_name=wallet_name, proxy=proxy) 

    if activity == Activity.PANDRA_ECOGUARDIAN_OPERATIONS:
        await do_pandra_ecoguardian_operations(private_key=private_key, wallet_name=wallet_name, proxy=proxy) 

    if activity == Activity.PANDRA_MANTLE_OPERATIONS:
        await do_pandra_mantle_operations(private_key=private_key, wallet_name=wallet_name, proxy=proxy)

    if activity == Activity.MAINNET_ALPHA_NFT_CORE_DAO_OPERATIONS:
        await do_alpha_nft_core_dao_operations(private_key=private_key, wallet_name=wallet_name, proxy=proxy) 
        
    if activity == Activity.BSC_POLYGON_ZKMESSENGER:
        await do_messenger(private_key=private_key, wallet_name=wallet_name, proxy=proxy)

    if activity == Activity.BNB_CHAIN_LUBAN_NFT_OPERATIONS:
        await do_bnb_luban_operations(private_key=private_key, wallet_name=wallet_name, proxy=proxy) 

    if activity == Activity.ZK_LIGHT_CLIENT_NFT_OPERATIONS:
        await do_zk_light_client_operations(private_key=private_key, wallet_name=wallet_name, proxy=proxy) 
    
    if activity == Activity.LEGENDARY_PANDA_GRIND_OPERATIONS:
        route_for_grind = []
        
        if PANDRA_GRIND_ROUTE == 'Uncommon':
            route_for_grind = uncommon_pandra_config
        elif PANDRA_GRIND_ROUTE == 'Rare':
            route_for_grind = rare_pandra_config
        elif PANDRA_GRIND_ROUTE == 'Epic':
            route_for_grind = epic_pandra_config
        elif PANDRA_GRIND_ROUTE == 'Legendary':
            route_for_grind = legendary_pandra_config    

        logger.info(f'Запущен гринд {PANDRA_GRIND_ROUTE} Tier Pandra')
        await do_pandra_operations(private_key=private_key, wallet_name=wallet_name, proxy=proxy, grind_list=route_for_grind)

    
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
        items = list(wallet_key_proxy_tuple.items())
        random.shuffle(items)
        wallet_key_proxy_tuple = dict(items)

    for i, ((wallet_name, private_key), proxy) in enumerate(wallet_key_proxy_tuple.items(), 1):
        task = asyncio.create_task(run_wallet(wallet_name, private_key, proxy, i))
        tasks.append(task)    

    await asyncio.gather(*tasks)

    logger.info("The bot has ended it's work")

if __name__ == "__main__":
    authors = ["@1liochka1", "@maked0n1an"]
    random.shuffle(authors)
    art = text2art(text="Polyhedra AIO", font="standart")
    print(colored(art, "cyan"))
    print(colored(f"Authors: {authors[0]}, {authors[1]}\n", "cyan"))
        
    write_to_main_log()

    asyncio.run(main())