from metamsk import *
from dotenv import load_dotenv
from storage import chromedriver_path
import os 
import traceback

load_dotenv()

my_key = os.getenv('MY_SECRET_TEST')
passw  = os.getenv('METAMASK_PASSW')

pool_link = "https://traderjoexyz.com/avalanche/pool/v2/0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7/0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e/1"

network_name = "Avalanche Network"
rpc_url  = "https://api.avax.network/ext/bc/C/rpc"
chain_id = 43114
currency_symbol = "AVAX"



# try: 
def get_min_amount_tokenX_tokenY():
    """Using selenium and extension. can fail"""
    
    driver = launchSeleniumWebdriver(chromedriver_path)
    time.sleep(2)
    try: 
        metamaskSetup(my_key, passw)
        addNetwork(network_name, rpc_url, chain_id, currency_symbol)
    except Exception as err:
        tb = traceback.format_exc()
        print(tb)
        
    driver.switch_to.new_window()

    try: 
        driver.get('https://traderjoexyz.com')
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@class="chakra-icon css-bbkz97"]').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//div[text()="MetaMask"]').click()


    # driver.find_element(By.XPATH, '//button[text()="Connect"]').click()
        connectToWebsite()
        driver.get(pool_link)
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//button[text()="Remove Liquidity"]').click()
        element = driver.find_element(By.XPATH, '//h2[contains(text(), "You will receive:")]/following-sibling::div/div[3]/p[contains(@class, "css-1xi6ire")]')

        first_coin_amount = element.text

        element = driver.find_element(By.XPATH, '//h2[contains(text(), "You will receive:")]/following-sibling::div/div[2]/p[contains(@class, "css-d544uc")]')

        second_coin_amount = element.text

        return first_coin_amount, second_coin_amount
    except Exception as err:
        tb = traceback.format_exc()
        print(tb)
        return 0, 0

# except: 
get_min_amount_tokenX_tokenY()