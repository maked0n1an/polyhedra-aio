import copy
import sys
import random
import time

from loguru import logger

out_file = ''

with open(f"{out_file}input_data/proxies.txt", "r") as f:
    PROXIES = [row.strip() for row in f]

with open(f"{out_file}input_data/private_keys.txt", "r") as f:
    PRIVATE_KEYS = [row.strip() for row in f]

with open(f"{out_file}input_data/wallet_names.txt", "r") as f:
    WALLET_NAMES = [row.strip() for row in f]

loggers = {}

def initial_delay():
    delay = random.randint(2000,
        2050)
    logger.info(f"Waiting {delay} seconds to start bot work")
    time.sleep(delay)

def write_to_logs(wallet_name):
    if wallet_name not in loggers:
        wallet_logger = logger.bind(wallet_name=wallet_name)       
        wallet_logger.add(
            rf"logs\log_{wallet_name}.log",
            format="<white>{time: MM/DD/YYYY HH:mm:ss}</white> | <level>"
            "{level: <8}</level> | <cyan>"
            "</cyan> <white>{message}</white>",
            filter=lambda record: record["extra"].get("wallet_name") == wallet_name
        )        
        loggers[wallet_name] = wallet_logger
        return wallet_logger
    else:
        return loggers[wallet_name]
        
def write_to_main_log():
    logger.remove()
    logger.add(
        sys.stderr,
        format="<white>{time: MM/DD/YYYY HH:mm:ss}</white> | <level>"
        "{level: <8}</level> | <cyan>"
        "</cyan> <white>{message}</white>",
    )
    logger.add(
        "main.log",
        format="<white>{time: MM/DD/YYYY HH:mm:ss}</white> | <level>"
        "{level: <8}</level> | <cyan>"
        "</cyan> <white>{message}</white>",
    )
    
    return logger