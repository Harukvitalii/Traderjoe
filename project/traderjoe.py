
import aiohttp 
import os 
from web3_driver import WEB3_DRIVER_AVAX

from storage import contract_marketplace
from storage import ABI_marketplace
from storage import my_address, contract_marketplace, ABI_marketplace





httprouter = ' https://api.avax.network/ext/bc/C/rpc'  
web_driver_avax = WEB3_DRIVER_AVAX(httprouter,my_address,contract_marketplace, ABI_marketplace, secret= os.getenv('MY_SECRET'))
    
# https://raw.githubusercontent.com/traderjoe-xyz/joe-tokenlists/main/mc.tokenlist.json
# token list






# fnm = contract_marketplace.functions.buy(









