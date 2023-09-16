import requests

class Session:
    @staticmethod
    def get_web3_session_via_proxy(proxy: str):
        session = requests.Session()
        session.proxies = {"socks5": proxy, "http": proxy, "https": proxy}
        session.proxies.update(requests.utils.getproxies())
        session.auth = requests.auth.HTTPProxyAuth("", "")

        return session