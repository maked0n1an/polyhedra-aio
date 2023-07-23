from enum import Enum
import requests
from web3 import Web3


class Rpc(Enum):
    BSC = (1,)
    ARBITRUM = (2,)
    POLYGON = (3,)
    AVAX = (4,)
    GNOSIS = (5,)
    OPTIMISM = (6,)
    CELO = (7,)
    KLAYTN = 8
    DFK = 9

    @staticmethod
    def get_web3_session(proxy: str):
        session = requests.Session()
        session.proxies = {"socks5": proxy, "http": proxy, "https": proxy}
        session.proxies.update(requests.utils.getproxies())
        session.auth = requests.auth.HTTPProxyAuth("", "")

        return session