import copy
import sys

from loguru import logger

out_file = ''

with open(f"{out_file}input_data/proxies.txt", "r") as f:
    PROXIES = [row.strip() for row in f]

with open(f"{out_file}input_data/private_keys.txt", "r") as f:
    PRIVATE_KEYS = [row.strip() for row in f]

with open(f"{out_file}input_data/wallet_names.txt", "r") as f:
    WALLET_NAMES = [row.strip() for row in f]
    
def write_to_logs(address, wallet_name):    
    write_to_main_log()
    logger.add(
        rf"logs\log_{wallet_name}.log",
        format="<white>{time: MM/DD/YYYY HH:mm:ss}</white> | <level>"
        "{level: <8}</level> | <cyan>"
        "</cyan> <white>{message}</white>",
    )

    return logger

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