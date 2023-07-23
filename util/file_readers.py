out_file = ''

# прокси - по желанию, но рекомендую при большом количестве кошельков,
# нужно вставить в формате log:pass@ip:port в файле proxyy.txt
with open(f"{out_file}input_data/proxies.txt", "r") as f:
    PROXIES = [row.strip() for row in f]

with open(f"{out_file}input_data/private_keys.txt", "r") as f:
    PRIVATE_KEYS = [row.strip() for row in f]