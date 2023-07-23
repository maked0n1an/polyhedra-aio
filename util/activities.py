import asyncio
from loguru import logger

from input_data.config import *
from modules.zk_bridge import ZkBridge
from modules.zk_message import ZkMessage
from util.chain import Chain
from util.activity import Activity

async def do_op_bnb_operations(private_key, proxy, address):    
    logger.info(f"{address}: Запущен opBNB NFT mint and bridge")
    zk = ZkBridge(privatekey=private_key, 
        delay=DELAY, 
        chain=OP_BNB_BRIDGE[0], 
        to_chain=OP_BNB_BRIDGE[1], 
        api=MORALIS_API_KEY, 
        nft='ZkBridge on opBNB',
        proxy=proxy)    

    # await zk.mint()
    await zk.bridge_nft()
