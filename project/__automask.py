import os
import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from auto_metamask import *

chromedriver_path = 'drivers/chromedriver'
my_key = os.getenv('MY_SECRET_TEST')
passw  = os.getenv('METAMASK_PASSW')

# Set the chromedriver path as an environment variable
os.environ['webdriver.chrome.driver'] = chromedriver_path

if __name__ == '__main__':

    # metamask_path = downloadMetamask(
    #     'https://github.com/MetaMask/metamask-extension/releases/download/v10.11.2/metamask-chrome-10.11.2.zip')
    # print(metamask_path)
    driver = setupWebdriver("/home/kaixenix/Programming/CrProjects/TraderJoe/metamask-chrome-10.11.2.zip")
    print('driver started')
    # Test account, please do not use for production environment
    setupMetamask(
        my_key, passw)
    addNetwork('BSC', 'https://bsc-dataseed1.binance.org', '56', 'BNB')
    changeNetwork('BSC')
    # Test account, please do not use for production environment
    # driver.get('https://traderjoexyz.com')
    # importPK("bb334564f93fc3a40a3b6a89e0560101bb86e5b75c773381f1e6d2f37fc5c5ba")

    driver.switch_to.new_window()
    driver.get('https://metamask.github.io/test-dapp/')

    wait = WebDriverWait(driver, 20, 1)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[text()="Connect"]'))).click()
    connectWallet()

    time.sleep(6)
    driver.quit()