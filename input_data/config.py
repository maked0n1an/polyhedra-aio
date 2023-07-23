from util.chain import Chain

MINT_GREENFIELD_CHAIN = Chain.BSC
OP_BNB_MINT = Chain.BSC # DATA['bsc'] 
OP_BNB_BRIDGE = Chain.BSC, Chain.OP_BNB #'bsc', 'op_bnb'
# PANDRA_CODECONQUEROR_MINT = DATA['bsc']
# PANDRA_CODECONQUEROR_BRIDGE = DATA['bsc'], DATA['core']
# PANDRA_PIXELBROWLER_MINT = DATA['polygon']
# PANDRA_PIXELBROWLER_BRIDGE = DATA['polygon'], DATA['core']
# PANDRA_MELODYMAVEN_MINT = DATA['core']
# PANDRA_MELODYMAVEN_BRIDGE= DATA['core'], DATA['polygon']
# PANDRA_ECOGUARDIAN_MINT = DATA['celo']
# PANDRA_ECOGUARDIAN_BRIDGE= DATA['celo'], DATA['polygon']
# MAINNET_ALPHA_NFT_CORE_MINT= DATA['core']
# MAINNET_ALPHA_NFT_CORE_BRIDGE_BRIDGE = DATA['core'], DATA['polygon'] 
# BSC_POLYGON_ZKMESSENGER = DATA['bsc'], DATA['arbitrum_nova'] 
# ZK_LIGHT_CLIENT_NFT_MINT = DATA['bsc']
# ZK_LIGHT_CLIENT_NFT_BRIDGE = DATA['bsc'], DATA['polygon']

# rpc по желанию можно поменять(рекомендуется при большом количестве кошельков)
rpcs = {'bsc': 'https://rpc.ankr.com/bsc',
        'polygon': 'https://polygon-rpc.com',
        'core': 'https://rpc.coredao.org',
        'opbnb': 'https://opbnb-testnet-rpc.bnbchain.org',
        'celo': 'https://rpc.ankr.com/celo'}


# Количество кошельков для одновременного запуска, т.е если у вас 100 кошельков, и вы выбрали число 5,
# то скрипт поделит ваши кошельки на 20 частей по 5 кошельков которые будут запущены одновременно
wallets_in_batch = 5

# start_delay отвечает за начальную задержку между кошельками, нужна для одновременного запуска несколька кошелей, смотри wallets_in_batch выше
# рекомендую не менять для максимального рандома
start_delay = (1, 1)

# перемешка кошельков
# вкл - 1, выкл - 0
shuffle_keys = 1

# перерыв между действиями
DELAY = (1, 10)

# moralis api key - https://admin.moralis.io/login идем сюда и получаем апи ключ, НУЖЕН DEFAULT KEY!, нужно для нахождения id нфт
MORALIS_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjEwNzg2NDU4LWEyMWUtNDU3Mi1hNTU2LWI0OWE0ZTJhZTU3YyIsIm9yZ0lkIjoiMzQ0MTM2IiwidXNlcklkIjoiMzUzNzY3IiwidHlwZUlkIjoiNjY4MDVjNTQtMzlmYS00OGQ1LTgyMDItY2EwMjkzNmJiNzQ2IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE2ODcxMDk4MTUsImV4cCI6NDg0Mjg2OTgxNX0.6Sgw7i3Fl_5JRYV6_2Sz2SFDLp-i26xK4nPWzmcEWaQ'

# cколько максимум секунд скрипт будет ждать подтверждения транзакции
max_wait_time = 150

# режимы работы, ниже представлена подробная информация, кто будет заебывать в чате буду банить
MODE = 'messenger'   # 'messenger' / 'nftbridger'

'''
    
    квест на оптравку сообщений, скрипт будет отправлять рандомный текст
    messenger  -  chain  только из bsc polygon и сelo
                  to  только в bsc, polygon, nova, ftm, mbeam
                  из CELO в FTM, BSC, POLYGON 
    
    квест на бридж и минт нфт
    nftbridger - для каждой нфт свои чейны, если ошибетесь - работать не будет
    
    данные ниже для работы в режиме nftbridger

    greenfield   -   сhain - bsc  to - polygon
    zkLightClient   -   сhain - bsc, polygon  to - bsc, polygon
    Mainnet Alpha   -   сhain - polygon, core to - bsc
    Luban   -   сhain - bsc  to - polygon
    ZkBridge on opBNB  -  chain - bsc, polygon, core  to - bsc, polygon, core, opbnb
    Pandra  -  chain - bsc, polygon, core, celo to - bsc, polygon, core, combo, celo, gnosis, metis
'''
# cети  bsc  polygon  core  ftm  сelo  nova  combo

# из какой сети минтить и бриджить / отправлять сообщение
chain = ''

# в какую сеть бриджить / отправлять сообщение
# либо 'определенная сеть' либо ['сеть', 'сеть'] для выбора рандомной сети (если это позволяет настройка выше), не читаешь гайд получаешь бан в чате
to = ''

# выбор нфт для минта и бриджа
# список нфт 'greenfield' 'zkLightClient' 'Mainnet Alpha' 'Luban' 'ZkBridge on opBNB', 'Pandra'
nft = ''