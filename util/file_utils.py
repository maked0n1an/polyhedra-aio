from loguru import logger as global_logger

out_file = ''

with open(f"{out_file}input_data/proxies.txt", "r") as f:
    PROXIES = [row.strip() for row in f]

with open(f"{out_file}input_data/private_keys.txt", "r") as f:
    PRIVATE_KEYS = [row.strip() for row in f]

with open(f"{out_file}input_data/wallets_names.txt", "r") as f:
    WALLETS_NAMES = [row.strip() for row in f]
    
def write_to_logs(logger,address, name):
    global_logger.remove()
    logger = copy.deepcopy(global_logger)
    logger.add(
        f"{out_file}logs/log_{name}.log",
        format="<white>{time: MM/DD/YYYY HH:mm:ss}</white> | <level>"
        "{level: <8}</level> | <cyan>"
        "</cyan> <white>{message}</white>",
    )

    return logger