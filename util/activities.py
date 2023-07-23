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
        delay=DELAY,
        proxy=proxy)
    
    await zk.mint()

async def do_op_bnb_operations(private_key, proxy):    
    zk = ZkBridge(private_key=private_key, 
        chain=OP_BNB_BRIDGE_CHAIN[0], 
        to_chain=OP_BNB_BRIDGE_CHAIN[1], 
        nft='ZkBridge on opBNB',
        delay=DELAY,
        proxy=proxy)    

    await zk.bridge_nft()
