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
    def getWeb3(proxy: str, rpc):
        session = requests.Session()
        session.proxies = {"socks5": proxy, "http": proxy, "https": proxy}
        session.proxies.update(requests.utils.getproxies())
        session.auth = requests.auth.HTTPProxyAuth("", "")

        if rpc == Rpc.BSC:
            return Web3(
                provider=Web3.HTTPProvider("https://rpc.ankr.com/bsc", session=session)
            )

        if rpc == Rpc.AVAX:
            return Web3(
                provider=Web3.HTTPProvider("https://avax.meowrpc.com", session=session)
            )

        if rpc == Rpc.ARBITRUM:
            return Web3(
                provider=Web3.HTTPProvider(
                    "https://arbitrum-one.publicnode.com", session=session
                )
            )

        if rpc == Rpc.GNOSIS:
            return Web3(
                provider=Web3.HTTPProvider(
                    "https://gnosis.api.onfinality.io/public", session=session
                )
            )

        if rpc == Rpc.OPTIMISM:
            return Web3(
                provider=Web3.HTTPProvider(
                    "https://optimism.meowrpc.com", session=session
                )
            )

        if rpc == Rpc.POLYGON:
            return Web3(
                provider=Web3.HTTPProvider(
                    "https://polygon.llamarpc.com",
                    session=session,
                )
            )

        if rpc == Rpc.CELO:
            return Web3(
                provider=Web3.HTTPProvider("https://1rpc.io/celo", session=session)
            )

        if rpc == Rpc.DFK:
            return Web3(
                provider=Web3.HTTPProvider(
                    "https://subnets.avax.network/defi-kingdoms/dfk-chain/rpc",
                    # session=session,
                )
            )

        if rpc == Rpc.KLAYTN:
            return Web3(
                provider=Web3.HTTPProvider(
                    "https://rpc.ankr.com/klaytn",
                    session=session,
                )
            )

        return Web3(
            provider=Web3.HTTPProvider("https://rpc.ankr.com/bsc", session=session)
        )