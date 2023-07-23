import requests

from enum import Enum
from web3 import Web3
from util.chain import Chain


class Session:
    @staticmethod
    def get_web3_session_via_proxy(proxy: str):
        session = requests.Session()
        session.proxies = {"socks5": proxy, "http": proxy, "https": proxy}
        session.proxies.update(requests.utils.getproxies())
        session.auth = requests.auth.HTTPProxyAuth("", "")

        return session