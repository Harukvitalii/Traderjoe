from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
import os
import urllib.request
import logging

# EXTENSION_PATH = 'metamask-chrome-10.11.2.zip'
EXTENSION_PATH = os.getcwd() + '/MetaMask.crx'


EXTENSION_ID = 'nkbihfbeogaeaoehlefnkodbefgpgknn'

logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s')



def downloadMetamaskExtension():
    print('Setting up metamask extension please wait...')

    # url = 'https://xord-testing.s3.amazonaws.com/selenium/10.0.2_0.crx'
    # urllib.request.urlretrieve(url, os.getcwd() + '/metamaskExtension.crx')


def launchSeleniumWebdriver(driverPath):
    chrome_options = Options()
    chrome_options.add_extension(EXTENSION_PATH)
    global driver
    
    driver = webdriver.Chrome(options=chrome_options, executable_path=driverPath)
    global wait 
    wait = WebDriverWait(driver, 10)
    time.sleep(5)
    print("Extension has been loaded")
    return driver, wait 


def metamaskSetup(recoveryPhrase, password):
    driver.switch_to.window(driver.window_handles[1])

    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Import an existing wallet']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="No thanks"]'))).click()
    

    pyperclip.copy(recoveryPhrase)
    
    input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="import-srp__srp-word-0"]')))
    input.send_keys(Keys.CONTROL,'v')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Confirm Secret Recovery Phrase"]'))).click()
    input1 = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@data-testid="create-password-new"]')))
    input1.send_keys(password)
    input2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@data-testid="create-password-confirm"]')))
    input2.send_keys(password)
    
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@data-testid="create-password-terms"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,'//button[text()="Import my wallet"]'))).click()


    wait.until(EC.element_to_be_clickable((By.XPATH,'//button[text()="Got it!"]'))).click()

    # closing the message popup after all done metamask screen
    wait.until(EC.element_to_be_clickable((By.XPATH,'//button[text()="Next"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,'//button[text()="Done"]'))).click()
    print("Wallet has been imported successfully")


def addNetwork(network_name, rpc_url, chain_id, currency_symbol):
    """Add new network

    :param network_name: Network name
    :type network_name: String
    :param rpc_url: RPC URL
    :type rpc_url: String
    :param chain_id: Chain ID
    :type chain_id: String
    :param currency_symbol: Currency symbol
    :type currency_symbol: String
    """
    try: 
        wait.until(EC.element_to_be_clickable((By.XPATH, '//i[@class="fa fa-times"]'))).click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.app-header__network-component-wrapper > div'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,'//button[text()="Add network"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,'//h6[text()="Add a network manually"]'))).click()
        
        inputs = driver.find_elements(By.XPATH, '//input')

        inputs[1].send_keys(network_name)
        inputs[2].send_keys(rpc_url)
        inputs[3].send_keys(chain_id)
        inputs[4].send_keys(currency_symbol)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Save"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Got it"]'))).click()
        
    except: 
        print('Failed to add network')
        return False
    print(f"Added Network {network_name}")
    return True


def changeMetamaskNetwork(networkName):
    # opening network
    print("Changing network")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
    print("closing popup")
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="popover-content"]/div/div/section/header/div/button').click()

    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span').click()
    time.sleep(2)
    print("opening network dropdown")
    elem = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div')
    time.sleep(2)
    all_li = elem.find_elements_by_tag_name("li")
    time.sleep(2)
    for li in all_li:
        text = li.text
        if (text == networkName):
            li.click()
            print(text, "is selected")
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(3)
            return
    time.sleep(2)
    print("Please provide a valid network name")

    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)


def connectToWebsite():

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    # driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Next"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Connect"]'))).click()
    
    # driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[4]/div[2]/button[2]').click()
    # time.sleep(1)
    # driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
    # time.sleep(3)
    print('Site connected to metamask')
    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(0.1)


def confirmApprovalFromMetamask():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(10)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(10)
    # confirm approval from metamask
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[4]/footer/button[2]').click()
    time.sleep(12)
    print("Approval transaction confirmed")

    # switch to dafi
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)


def rejectApprovalFromMetamask():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(10)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(10)
    # confirm approval from metamask
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[4]/footer/button[1]').click()
    time.sleep(8)
    print("Approval transaction rejected")

    # switch to dafi
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
    print("Reject approval from metamask")


def confirmTransactionFromMetamask():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(10)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(10)

    # # confirm transaction from metamask
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[3]/div[3]/footer/button[2]').click()
    time.sleep(13)
    print("Transaction confirmed")

    # switch to dafi
    driver.switch_to.window(driver.window_handles[0])

    time.sleep(3)


def rejectTransactionFromMetamask():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(5)
    # confirm approval from metamask
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[3]/div[3]/footer/button[1]').click()
    time.sleep(2)
    print("Transaction rejected")

    # switch to web window
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

def addToken(tokenAddress):
    # opening network
    print("Adding Token")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
    print("closing popup")
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="popover-content"]/div/div/section/header/div/button').click()

    # driver.find_element_by_xpath('//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span').click()
    # time.sleep(2)

    print("clicking add token button")
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div/div/div[3]/div/div[3]/button').click()
    time.sleep(2)
    # adding address
    driver.find_element_by_id("custom-address").send_keys(tokenAddress)
    time.sleep(10)
    # clicking add
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div[2]/div[2]/footer/button[2]').click()
    time.sleep(2)
    # add tokens
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div[3]/footer/button[2]').click()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

def signConfirm():
    print("sign")
    time.sleep(3)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[3]/button[2]').click()
    time.sleep(1)
    # driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
    # time.sleep(3)
    print('Sign confirmed')
    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)


def signReject():
    print("sign")
    time.sleep(3)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[3]/button[1]').click()
    time.sleep(1)
    # driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
    # time.sleep(3)
    print('Sign rejected')
    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
    
    
    
    
    
