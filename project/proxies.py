import aiohttp


def prepare_proxy(proxies): 
    proxies = proxies[:]
    proxies = [proxy.split(':') for proxy in proxies]
    return [[f'http://{proxy[0]}:{proxy[1]}',aiohttp.BasicAuth(proxy[2],proxy[3])] for proxy in proxies]



proxy_amazy = [


"45.89.19.46:13152:8eMPfu:bCP0WuoDu4",             # истекает 2023-03-30 19:54:31
"45.89.19.113:7766:8eMPfu:bCP0WuoDu4",             # истекает 2023-03-30 19:54:31
"45.89.18.233:9072:8eMPfu:bCP0WuoDu4",             # истекает 2023-03-30 19:54:31
"45.89.19.65:6896:8eMPfu:bCP0WuoDu4",             # истекает 2023-03-30 19:54:31





]

proxies    = prepare_proxy(proxy_amazy)
