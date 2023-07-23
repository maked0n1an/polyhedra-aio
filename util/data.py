from util.chain import Chain

# меняем рпс на свои
DATA = {    
    Chain.ARBITRUM                  : {'rpc': 'https://rpc.ankr.com/arbitrum', 'scan': 'https://arbiscan.io/tx/', 'token': 'ETH', 'chain_id': 42161},    

    Chain.ARBITRUM_NOVA             : {'rpc': 'https://nova.arbitrum.io/rpc', 'scan': 'https://nova.arbiscan.io/tx/', 'token': 'ETH', 'chain_id': 42170},
    
    Chain.AVALANCHE                 : {'rpc': 'https://rpc.ankr.com/avalanche', 'scan': 'https://snowtrace.io/tx/', 'token': 'AVAX', 'chain_id': 43114},    

    Chain.BSC                       : {'rpc': 'https://rpc.ankr.com/bsc', 'scan': 'https://bscscan.com/tx/', 'token': 'BNB', 'chain_id': 56},

    Chain.CELO                      : {'rpc': 'https://1rpc.io/celo', 'scan': 'https://celoscan.io/tx/', 'token': 'CELO', 'chain_id': 42220},

    Chain.CORE                      : {'rpc': 'https://rpc.coredao.org', 'scan': 'https://scan.coredao.org/tx/', 'token': 'CORE', 'chain_id': 1116},

    Chain.DFK                       : {'rpc': 'https://subnets.avax.network/defi-kingdoms/dfk-chain/rpc	', 'scan': 'https://explorer.dfkchain.com/tx/', 'token': 'JEWEL', 'chain_id': 53935},

    Chain.ETH                       : {'rpc': 'https://rpc.ankr.com/eth', 'scan': 'https://etherscan.io/tx/', 'token': 'ETH', 'chain_id': 1},

    Chain.FANTOM                    : {'rpc': 'https://rpc.ankr.com/fantom', 'scan': 'https://ftmscan.com/tx/', 'token': 'FTM', 'chain_id': 250},

    Chain.GNOSIS                    : {'rpc': 'https://rpc.ankr.com/gnosis', 'scan': 'https://gnosisscan.io/tx/', 'token': 'xDAI', 'chain_id': 100},

    Chain.HARMONY                   : {'rpc': 'https://api.harmony.one', 'scan': 'https://explorer.harmony.one/tx/', 'token': 'ONE', 'chain_id': 1666600000},
    
    Chain.KLAYTN                    : {'rpc': 'https://1rpc.io/klay', 'scan': 'https://scope.klaytn.com/tx/', 'token': 'KLAY', 'chain_id': 8217}, 

    Chain.MOONBEAM                  : {'rpc': 'https://rpc.ankr.com/moonbeam', 'scan': 'https://moonscan.io/tx/', 'token': 'GLMR', 'chain_id': 1284},

    Chain.MOONRIVER                 : {'rpc': 'https://moonriver.public.blastapi.io', 'scan': 'https://moonriver.moonscan.io/tx/', 'token': 'MOVR', 'chain_id': 1285},    

    Chain.OP_BNB                    : {'rpc': 'https://opbnbscan.com/', 'scan': 'https://opbnb-testnet.nodereal.io/v1/64a9df0874fb4a93b9d0a3849de012d3/tx/', 'token': 'tBNB', 'chain_id': 5611},  

    Chain.OPTIMISM                  : {'rpc': 'https://rpc.ankr.com/optimism', 'scan': 'https://optimistic.etherscan.io/tx/', 'token': 'ETH', 'chain_id': 10},  

    Chain.POLYGON                   : {'rpc': 'https://rpc.ankr.com/polygon', 'scan': 'https://polygonscan.com/tx/', 'token': 'MATIC', 'chain_id': 137},     

    Chain.POLYGON_ZKEVM             : {'rpc': 'https://zkevm-rpc.com', 'scan': 'https://zkevm.polygonscan.com/tx/', 'token': 'ETH', 'chain_id': 1101},

    Chain.ZK_SYNC                   : {'rpc': 'https://mainnet.era.zksync.io', 'scan': 'https://explorer.zksync.io/tx/', 'token': 'ETH', 'chain_id': 324},
}