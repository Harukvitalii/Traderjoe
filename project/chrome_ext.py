from metamsk import *
from dotenv import load_dotenv
import os 

load_dotenv()

my_key = os.getenv('MY_SECRET_TEST')
passw  = os.getenv('METAMASK_PASSW')

driver = launchSeleniumWebdriver('drivers/chromedriver')

metamaskSetup(my_key, passw)
# driver.get('https://traderjoexyz.com')
time.sleep(1000)