from util.activity import Activity
from util.chain import Chain

'''
    Тут глобальные настройки для активностей 
    Пример: [activity = (from_chain, to_chain)]
    Внимание: если вам нужен минт, то просто оставляйте второе значение как None
    Пример: [MAINNET_ALPHA_NFT_CORE_MINT = Chain.BSC, None]

    Прокси - по желанию, но рекомендую при большом количестве кошельков,
    нужно вставить в формате  protocol//:login:pass@ip:port 
    в файле proxies.txt

    Закоменти или раскоменти внизу то, что тебе (не) нужно по активностям
'''

activities_list = [
        Activity.GREENFIELD_TESTNET_MINT,
        Activity.OP_BNB_OPERATIONS,
        Activity.PANDRA_CODECONQUEROR_OPERATIONS,
        Activity.PANDRA_PIXELBROWLER_OPERATIONS,
        Activity.PANDRA_MELODYMAVEN_OPERATIONS,
        Activity.PANDRA_ECOGUARDIAN_OPERATIONS,
        Activity.PANDRA_MANTLE_OPERATIONS,
        Activity.MAINNET_ALPHA_NFT_CORE_DAO_OPERATIONS,
        Activity.BSC_POLYGON_ZKMESSENGER,
        Activity.ZK_LIGHT_CLIENT_NFT_OPERATIONS,
        Activity.BNB_CHAIN_LUBAN_NFT_OPERATIONS,
        Activity.LEGENDARY_PANDA_GRIND_OPERATIONS
    ]

# Доступные маршруты гринда: 'Uncommon' | 'Rare' | 'Epic' | 'Legendary'
PANDRA_GRIND_ROUTE = 'Uncommon'

# Нужно ли мешать кошельки? | Да - 1, Нет - 0
IS_SHUFFLE_KEYS = 1

# INITIAL_DELAY отвечает за начальную задержку между кошельками, нужна для одновременного запуска несколька кошелей, смотри wallets_in_batch выше
# рекомендую не менять для максимального рандома
INITIAL_DELAY = (100, 3000)

# перерыв между действиями
DELAY = (30, 100)

# для клейма NFT, отправленных с polygon или core
BIG_DELAY = 250 

# moralis api key - https://admin.moralis.io/login идем сюда и получаем апи ключ, НУЖЕН DEFAULT KEY!, нужно для нахождения id нфт
MORALIS_API_KEY = ''

# cколько максимум секунд скрипт будет ждать подтверждения транзакции
MAX_WAIT_TIME = 150

# ======================================== Можно менять, но будь внимателен: не забывай про запятые в массиве,
# ======================================== а также названия сетей (Chain). Рекомендую глянуть еще раз config.py и chain.py!

GREENFIELD_MINT_CHAIN           = Chain.BSC
OP_BNB_BRIDGE_CHAIN             = Chain.BSC, Chain.OP_BNB
PANDRA_CODECONQUEROR_BRIDGE     = Chain.BSC, Chain.CORE
PANDRA_PIXELBROWLER_BRIDGE      = Chain.POLYGON, Chain.CORE
PANDRA_MELODYMAVEN_BRIDGE       = Chain.CORE, Chain.POLYGON
PANDRA_ECOGUARDIAN_BRIDGE       = Chain.CELO, Chain.POLYGON
PANDRA_MANTLE_BRIDGE            = Chain.POLYGON, Chain.MANTLE
MAINNET_ALPHA_NFT_CORE_BRIDGE   = Chain.CORE, Chain.POLYGON
BSC_POLYGON_ZKMESSENGER         = Chain.BSC, Chain.ARBITRUM_NOVA
BNB_CHAIN_LUBAN_NFT_BRIDGE      = Chain.BSC, [Chain.POLYGON, Chain.CELO, Chain.CORE]
ZK_LIGHT_CLIENT_NFT_BRIDGE      = Chain.BSC, [Chain.POLYGON, Chain.CORE, Chain.CELO]

legendary_pandra_config = [ # 20 bridges + 5 mints
    #############################################========================= 
    [Chain.BSC, Chain.POLYGON],                 # ~$1.06
    [Chain.BSC, Chain.CORE],                    # ~$0.67
    [Chain.BSC, Chain.CELO],                    # ~$0.6
    [Chain.BSC, Chain.COMBO_TESTNET],           # ~$0.4
    [Chain.BSC, Chain.OP_BNB],                  # ~$0.29
    #############################################========================= 
    [Chain.POLYGON, Chain.BSC],                 # ~$1.39    
    [Chain.POLYGON, Chain.CORE],                # ~$0.50
    [Chain.POLYGON, Chain.CELO],                # ~$0.47
    [Chain.POLYGON, Chain.COMBO_TESTNET],       # ~$0.35
    [Chain.POLYGON, Chain.OP_BNB],              # ~$0.41
    #############################################========================= 
    [Chain.CORE, Chain.BSC],                    # ~$2.34
    [Chain.CORE, Chain.POLYGON],                # ~$0.89
    [Chain.CORE, Chain.POLYGON, Chain.CELO],    # ~$0.89 + $0.42 ~ $1.31
    [Chain.CORE, Chain.COMBO_TESTNET],          # ~$0.43
    [Chain.CORE, Chain.OP_BNB],                 # ~$0.43
    #############################################========================= 
    [Chain.CELO, Chain.BSC],                    # ~$2.35
    [Chain.CELO, Chain.POLYGON],                # ~$0.85
    [Chain.CELO, Chain.POLYGON, Chain.CORE],    # ~$0.89 + $0.5 ~ $1.39   
    [Chain.CELO, Chain.COMBO_TESTNET],          # ~$0.51
    [Chain.CELO, Chain.OP_BNB],                 # ~$0.51
]

epic_pandra_config = [ # 15 bridges + 5 mints
    #############################################========================= ~$2
    # [Chain.BSC, Chain.POLYGON],                 # ~$1.06
    [Chain.BSC, Chain.CORE],                    # ~$0.67
    [Chain.BSC, Chain.CELO],                    # ~$0.6
    [Chain.BSC, Chain.COMBO_TESTNET],           # ~$0.4
    [Chain.BSC, Chain.OP_BNB],                  # ~$0.29
    #############################################========================= ~$2.6
    # [Chain.POLYGON, Chain.BSC],                 # ~$1.39    
    [Chain.POLYGON, Chain.CORE],                # ~$0.50
    [Chain.POLYGON, Chain.CELO],                # ~$0.47
    [Chain.POLYGON, Chain.COMBO_TESTNET],       # ~$0.35
    [Chain.POLYGON, Chain.OP_BNB],              # ~$0.41
    # [Chain.POLYGON, Chain.MANTLE],              # ~$0.83
    #############################################========================= ~$1.9
    # [Chain.CORE, Chain.BSC],                    # ~$2.34
    [Chain.CORE, Chain.POLYGON],                # ~$0.89 + 
    # [Chain.CORE, Chain.POLYGON, Chain.CELO],    # ~$0.89 + $0.42 ~ $1.31
    [Chain.CORE, Chain.COMBO_TESTNET],          # ~$0.43 + 
    # [Chain.CORE, Chain.OP_BNB],                 # ~$0.43 + 
    #############################################========================= ~$1.9
    # [Chain.CELO, Chain.BSC],                    # ~$2.35
    [Chain.CELO, Chain.POLYGON],                # ~$0.85
    # [Chain.CELO, Chain.POLYGON, Chain.CORE],    # ~$0.89 + $0.5 ~ $1.39   
    [Chain.CELO, Chain.COMBO_TESTNET],          # ~$0.51
    [Chain.CELO, Chain.OP_BNB],                 # ~$0.51 
    #############################################========================= =$0
    [Chain.BSC_TESTNET, Chain.OP_BNB],          
    [Chain.BSC_TESTNET, Chain.COMBO_TESTNET],
]

rare_pandra_config = [ # 10 bridges + 5 mints 
    #############################################========================= 
    # [Chain.BSC, Chain.POLYGON],                 # ~$1.06
    # [Chain.BSC, Chain.CORE],                    # ~$0.67
    [Chain.BSC, Chain.CELO],                    # ~$0.6
    [Chain.BSC, Chain.COMBO_TESTNET],           # ~$0.4
    # [Chain.BSC, Chain.OP_BNB],                  # ~$0.29
    #############################################========================= 
    # [Chain.POLYGON, Chain.BSC],                 # ~$1.39    
    [Chain.POLYGON, Chain.CORE],                # ~$0.50
    [Chain.POLYGON, Chain.CELO],                # ~$0.47
    [Chain.POLYGON, Chain.COMBO_TESTNET],       # ~$0.35
    [Chain.POLYGON, Chain.OP_BNB],              # ~$0.41
    # [Chain.POLYGON, Chain.MANTLE],              # ~$0.83
    #############################################========================= 
    # [Chain.CORE, Chain.BSC],                    # ~$2.34
    # [Chain.CORE, Chain.POLYGON],                # ~$0.89
    # [Chain.CORE, Chain.POLYGON, Chain.CELO],    # ~$0.89 + $0.42 ~ $1.31
    [Chain.CORE, Chain.COMBO_TESTNET],          # ~$0.43
    [Chain.CORE, Chain.OP_BNB],                 # ~$0.43
    #############################################========================= 
    # [Chain.CELO, Chain.BSC],                    # ~$2.35
    # [Chain.CELO, Chain.POLYGON],                # ~$0.85
    # [Chain.CELO, Chain.POLYGON, Chain.CORE],    # ~$0.89 + $0.5 ~ $1.39   
    [Chain.CELO, Chain.COMBO_TESTNET],          # ~$0.51
    [Chain.CELO, Chain.OP_BNB],                 # ~$0.51 
    #############################################========================= =$0
    [Chain.BSC_TESTNET, Chain.OP_BNB],          
    [Chain.BSC_TESTNET, Chain.COMBO_TESTNET],          
]

uncommon_pandra_config = [ # 5 bridges + 5 mints 
    #############################################========================= 
    # [Chain.BSC, Chain.POLYGON],                 # ~$1.06
    # [Chain.BSC, Chain.CORE],                    # ~$0.67
    # [Chain.BSC, Chain.CELO],                    # ~$0.6
    [Chain.BSC, Chain.COMBO_TESTNET],           # ~$0.4
    [Chain.BSC, Chain.OP_BNB],                  # ~$0.29
    #############################################========================= 
    # [Chain.POLYGON, Chain.BSC],                 # ~$1.39    
    # [Chain.POLYGON, Chain.CORE],                # ~$0.50
    # [Chain.POLYGON, Chain.CELO],                # ~$0.47
    [Chain.POLYGON, Chain.COMBO_TESTNET],       # ~$0.35
    [Chain.POLYGON, Chain.OP_BNB],              # ~$0.41
    # [Chain.POLYGON, Chain.MANTLE],              # ~$0.83
    #############################################========================= 
    # [Chain.CORE, Chain.BSC],                    # ~$2.34
    # [Chain.CORE, Chain.POLYGON],                # ~$0.89
    # [Chain.CORE, Chain.POLYGON, Chain.CELO],    # ~$0.89 + $0.42 ~ $1.31
    # [Chain.CORE, Chain.COMBO_TESTNET],          # ~$0.43
    [Chain.CORE, Chain.OP_BNB],                 # ~$0.43
    #############################################========================= 
    # [Chain.CELO, Chain.BSC],                    # ~$2.35
    # [Chain.CELO, Chain.POLYGON],                # ~$0.85
    # [Chain.CELO, Chain.POLYGON, Chain.CORE],    # ~$0.89 + $0.5 ~ $1.39   
    # [Chain.CELO, Chain.COMBO_TESTNET],          # ~$0.51
    # [Chain.CELO, Chain.OP_BNB],                 # ~$0.51           
    #############################################========================= =$0
    [Chain.BSC_TESTNET, Chain.OP_BNB],          
    [Chain.BSC_TESTNET, Chain.COMBO_TESTNET],
]

mint_pandra_config = [
    Chain.CORE, Chain.CELO, Chain.POLYGON, Chain.BSC, Chain.BSC_TESTNET 
]