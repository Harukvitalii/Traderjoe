from metamsk import *
from dotenv import load_dotenv
from storage import chromedriver_path
import os 
import traceback

load_dotenv()

my_key = os.getenv('MY_SECRET_TEST')
passw  = os.getenv('METAMASK_PASSW')


network_name = "Avalanche Network"
rpc_url  = "https://api.avax.network/ext/bc/C/rpc"
chain_id = 43114
currency_symbol = "AVAX"



# try: 
def get_min_amount_tokenX_tokenY(token1adr, token2adr, binStep):
    """Using selenium and extension. can fail"""
    
    pool_link = f"https://traderjoexyz.com/avalanche/pool/v2/{token1adr}/{token2adr}/{binStep}"
    driver, wait  = launchSeleniumWebdriver(chromedriver_path)
    time.sleep(2)
    try: 
        metamaskSetup(my_key, passw)
        if not addNetwork(network_name, rpc_url, chain_id, currency_symbol): 
            time.sleep(1000)
    except Exception as err:
        tb = traceback.format_exc()
        print(tb)
        time.sleep(10000)
        
    driver.switch_to.new_window()

    try: 
        driver.get('https://traderjoexyz.com')
        driver.find_element(By.XPATH, '//*[@class="chakra-icon css-bbkz97"]').click()
        try: 
            driver.find_element(By.XPATH, '//div[text()="MetaMask"]').click()
        except:
            print('Invisible matamask')
            # wait.until(EC.invisibility_of_element((By.XPATH, '//div[text()="MetaMask"]')))
            driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text()="MetaMask"]'))))
    # driver.find_element(By.XPATH, '//button[text()="Connect"]').click()
        connectToWebsite()
        driver.get(pool_link)
        try: 
            element = driver.find_element(By.XPATH, '//button[text()="Remove Liquidity"]')
        except:
            print('Invisible matamask')
            # wait.until(EC.invisibility_of_element((By.XPATH, '//div[text()="MetaMask"]')))
            driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Remove Liquidity"]'))))
        try: 
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//h2[contains(text(), "You will receive:")]/following-sibling::div/div[3]/p[contains(@class, "css-1xi6ire")]')))
            first_coin_amount = element.text

            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//h2[contains(text(), "You will receive:")]/following-sibling::div/div[2]/p[contains(@class, "css-d544uc")]')))
            second_coin_amount = element.text
        except:
            print('Not found min amount')
            return 0,0
        return first_coin_amount, second_coin_amount
    except Exception as err:
        tb = traceback.format_exc()
        print(tb)
        time.sleep(10000)
        return 0, 0

# except: 
get_min_amount_tokenX_tokenY()