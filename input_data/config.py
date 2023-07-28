from util.chain import Chain

'''
    Тут глобальные настройки для активностей 
    Пример: [activity = (from_chain, to_chain)]
    Внимание: если вам нужен минт, то просто оставляйте второе значение как None
    Пример: [MAINNET_ALPHA_NFT_CORE_MINT = Chain.BSC, None]

    Прокси - по желанию, но рекомендую при большом количестве кошельков,
    нужно вставить в формате  protocol//:log:pass@ip:port 
    в файле proxies.txt
'''
GREENFIELD_MINT_CHAIN           = Chain.BSC
OP_BNB_BRIDGE_CHAIN             = Chain.BSC, Chain.OP_BNB
PANDRA_CODECONQUEROR_BRIDGE     = Chain.BSC, Chain.CORE
PANDRA_PIXELBROWLER_BRIDGE      = Chain.POLYGON, Chain.CORE
PANDRA_MELODYMAVEN_BRIDGE       = Chain.CORE, Chain.POLYGON
PANDRA_ECOGUARDIAN_BRIDGE       = Chain.CELO, Chain.POLYGON
MAINNET_ALPHA_NFT_CORE_BRIDGE   = Chain.CORE, Chain.POLYGON
BSC_POLYGON_ZKMESSENGER         = Chain.BSC, Chain.ARBITRUM_NOVA
BNB_CHAIN_LUBAN_NFT_BRIDGE      = Chain.BSC, [Chain.POLYGON, Chain.CELO, Chain.CORE]
ZK_LIGHT_CLIENT_NFT_BRIDGE      = Chain.BSC, [Chain.POLYGON, Chain.CORE, Chain.CELO]

# Нужно ли мешать кошельки? | Да - 1, Нет - 0
IS_SHUFFLE_KEYS = 0

# Количество кошельков для одновременного запуска, т.е если у вас 100 кошельков, и вы выбрали число 5,
# то скрипт поделит ваши кошельки на 20 частей по 5 кошельков которые будут запущены одновременно
WALLETS_IN_BATCH = 5

# INITIAL_DELAY отвечает за начальную задержку между кошельками, нужна для одновременного запуска несколька кошелей, смотри wallets_in_batch выше
# рекомендую не менять для максимального рандома
INITIAL_DELAY = (800, 2000)

# перерыв между действиями
DELAY = (40, 110)

# moralis api key - https://admin.moralis.io/login идем сюда и получаем апи ключ, НУЖЕН DEFAULT KEY!, нужно для нахождения id нфт
MORALIS_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjEwNzg2NDU4LWEyMWUtNDU3Mi1hNTU2LWI0OWE0ZTJhZTU3YyIsIm9yZ0lkIjoiMzQ0MTM2IiwidXNlcklkIjoiMzUzNzY3IiwidHlwZUlkIjoiNjY4MDVjNTQtMzlmYS00OGQ1LTgyMDItY2EwMjkzNmJiNzQ2IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE2ODcxMDk4MTUsImV4cCI6NDg0Mjg2OTgxNX0.6Sgw7i3Fl_5JRYV6_2Sz2SFDLp-i26xK4nPWzmcEWaQ'

# cколько максимум секунд скрипт будет ждать подтверждения транзакции
MAX_WAIT_TIME = 150