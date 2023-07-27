import copy
import sys

from loguru import logger as global_logger

out_file = ''

with open(f"{out_file}input_data/proxies.txt", "r") as f:
    PROXIES = [row.strip() for row in f]

with open(f"{out_file}input_data/private_keys.txt", "r") as f:
    PRIVATE_KEYS = [row.strip() for row in f]

with open(f"{out_file}input_data/wallet_names.txt", "r") as f:
    WALLET_NAMES = [row.strip() for row in f]
    
def write_to_logs(address, wallet_name):
    new_logger = global_logger.bind()
    new_logger.remove()
    new_logger.add(
        f"{out_file}logs/log_{wallet_name}.log",
        format="<white>{time: MM/DD/YYYY HH:mm:ss}</white> | <level>"
        "{level: <8}</level> | <cyan>"
        "</cyan> <white>{message}</white>",
    )

    return new_logger

def main_log(log_file_name):
    main_logger = global_logger.bind()
    main_logger.remove()
    global_logger.add(
        sys.stderr,
        format="<white>{time: MM/DD/YYYY HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan></cyan> <white>{message}</white>",
    )
    global_logger.add(
        log_file_name,
        format="<white>{time: MM/DD/YYYY HH:mm:ss}</white> | <level>"
        "{level: <8}</level> | <cyan>"
        "</cyan> <white>{message}</white>",
    )

    return main_logger