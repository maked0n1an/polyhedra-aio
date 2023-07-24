import asyncio
from loguru import logger

from input_data.config import *
from modules.zk_bridge import ZkBridge
from modules.zk_message import ZkMessage
from util.chain import Chain
from util.activity import Activity

async def do_greenfield_mint_nft(private_key, proxy):
    zk = ZkBridge(private_key=private_key,
        chain=GREENFIELD_MINT_CHAIN, 
        to_chain=None,
        nft="Greenfield Testnet",
        proxy=proxy)
    
    await zk.mint()

async def do_op_bnb_operations(private_key, proxy):    
    zk = ZkBridge(private_key=private_key, 
        chain=OP_BNB_BRIDGE_CHAIN[0], 
        to_chain=OP_BNB_BRIDGE_CHAIN[1], 
        nft='ZkBridge on opBNB',
        proxy=proxy)  

    await zk.bridge_nft()

async def do_pandra_codeconquer_operations(private_key, proxy):
    zk = ZkBridge(private_key=private_key,
        chain=PANDRA_CODECONQUEROR_BRIDGE[0],
        to_chain=PANDRA_CODECONQUEROR_BRIDGE[1],
        nft='Pandra',
        proxy=proxy)

    await zk.bridge_nft()

async def do_pandra_pixelbowler_operations(private_key, proxy):
    zk = ZkBridge(private_key=private_key,
        chain=PANDRA_PIXELBROWLER_BRIDGE[0],
        to_chain=PANDRA_CODECONQUEROR_BRIDGE[1],
        nft='Pandra',
        proxy=proxy)
    
    await zk.bridge_nft()

async def do_pandra_melodymaven_operations(private_key, proxy):
    zk = ZkBridge(private_key=private_key,
        chain=PANDRA_MELODYMAVEN_BRIDGE[0],
        to_chain=PANDRA_MELODYMAVEN_BRIDGE[1],
        nft='Pandra',
        proxy=proxy)
    
    await zk.bridge_nft()

async def do_pandra_ecoguardian_operations(private_key, proxy):
    zk = ZkBridge(private_key=private_key,
        chain=PANDRA_ECOGUARDIAN_BRIDGE[0],
        to_chain=PANDRA_ECOGUARDIAN_BRIDGE[1],
        nft='Pandra',
        proxy=proxy)
    
    await zk.bridge_nft()