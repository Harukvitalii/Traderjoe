from web3 import Web3
from storage import my_address, contract_marketplace, ABI_marketplace
from storage  import USDT_ADRESS, ABI_USDT_PROXY
from dotenv import load_dotenv
import requests 
import os 
import time 
from eth_account import Account
from decimal import Decimal

import logging

# Enable Mnemonic features
logging.basicConfig( level=logging.DEBUG)
Account.enable_unaudited_hdwallet_features()
load_dotenv()


class WEB3_DRIVER_AVAX: 
    def __init__(self,privider_link, address, contract, ABI, private=None,secret=None): 
        web3 = Web3(Web3.HTTPProvider(privider_link))
        self.web3      = web3
        self.address   = web3.toChecksumAddress(address)   
        if secret: 
            self.private = Account.from_mnemonic(secret).privateKey.hex()
        else: 
            self.private = private
        self.contract_complate = self.web3.eth.contract(address=contract, abi=ABI)
        self.balance = self.web3.fromWei(self.web3.eth.get_balance(self.web3.toChecksumAddress(self.address)), 'ether')
        
        print(web3.isConnected(), '\nbalance: ', round(self.balance,3), 'AVAX')
        
    
    def add_liquidity_pool_AVAX(self, bin_range, amount_AVAX=None , amountUSDT=None): 
        dict_transaction = {
            'chainId': self.web3.eth.chain_id,
            'from': self.address,
            'gasPrice': int(self.web3.eth.gasPrice*1.1),
            'nonce': self.web3.eth.getTransactionCount(self.address),
            'value': int(self.web3.toWei(amount_AVAX, 'ether'))
            }
        # создаём транзакцию

        amountX, amountY = self.get_min_out_amount(amount_AVAX, amountUSDT)
        num_list = []

        # calculate the midpoint
        midpoint = bin_range // 2

        # loop through the range -midpoint to midpoint + 1
        for num in range(-midpoint, midpoint + 1):
            # append each integer to the list
            num_list.append(num)
        deltaIds = num_list,
        distributionX, distributionY = self.calculate_range_pricing_for_pool()
        
        transaction = self.contract_complate.functions.addLiquidityAVAX(
            tokenX_address = "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7",
            tokenY_address = "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E",
            binStep	= 20,
            amountX	= amountX,
            amountY	= amountY,
            amountXMin = int(amountX*0.999),
            amountYMin = int(amountY*0.999),
            activeIdDesired	= 8376132 ,#const
            idSlippage = 2, #const
            deltaIds = deltaIds,
            distributionX = distributionX,
            distributionY = distributionY,
            to_address = self.address,
            deadline = int(time.time()) + 60 * 2
        ).buildTransaction(dict_transaction)
        print(transaction)
        # exit()
        signed_txn = self.web3.eth.account.signTransaction(transaction, self.private)
    # Отправляем, смотрим тут https://testnet.bscscan.com/
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        timeout  = 60  # maximum time to wait for transaction receipt
        hash = self.wait_transaction(txn_hash, timeout)
        return hash
    
    
    def calculate_range_pricing_for_pool(self, delta): 

        zero_index = delta.index(0)
        array1 = delta[:zero_index+1]
        array2 = delta[zero_index:]
        # print(array1)
        qunatity_not_zero = 1*10**18/(len(array2)-0.5)
        qunatity_not_zero = Decimal(qunatity_not_zero).to_integral_value()
        
        qunatity_zero = qunatity_not_zero/2
        qunatity_zero = Decimal(qunatity_zero).to_integral_value()
        
        distributionX = [0]*(len(array1)-1) + [qunatity_zero] + [qunatity_not_zero]*(len(array2)-1)

        qunatity_not_zero = 1*10**18/(len(array1)-0.5)
        qunatity_not_zero = Decimal(qunatity_not_zero).to_integral_value()
        
        qunatity_zero     = qunatity_not_zero/2
        qunatity_zero = Decimal(qunatity_zero).to_integral_value()
        distributionY = [qunatity_not_zero]*(len(array1)-1) +  [qunatity_zero] + [0]*(len(array2)-1)
        
        return distributionX, distributionY 
    
    
    def remove_liquidity_pool(self,): 
        pass 
    
    def collectFees(self,): 
        dict_transaction = {
            'chainId': self.web3.eth.chain_id,
            'from': self.address,
            'gasPrice': int(self.web3.eth.gasPrice*1),
            'nonce': self.web3.eth.getTransactionCount(self.address),
            # 'value': int(self.web3.toWei(amount_AVAX, 'ether'))
            }
        # создаём транзакцию
        #TO DO  FIND A WAY TO GET IDS WITH MY LIQUIDITY OR WRITE IT ON THE ADDLIQUIDITY FUNCION IN FILE OR WHATEVER
        all_bins_with_my_liquidity = [i for i in range(8376134,8376181+1)] 
        transaction = self.contract_complate.functions.collectFees(
            self.address,  #my adress
            all_bins_with_my_liquidity
            
        ).buildTransaction(dict_transaction)
        print(transaction)
        # exit()
        signed_txn = self.web3.eth.account.signTransaction(transaction, self.private)
    # Отправляем, смотрим тут https://testnet.bscscan.com/
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        timeout  = 60  # maximum time to wait for transaction receipt
        hash = self.wait_transaction(txn_hash, timeout)
        return hash

    
    def swap_trader_joe_avax_to_alt(self, amount_AVAX): 
        dict_transaction = {
            'chainId': self.web3.eth.chain_id,
            'from': self.address,
            'gasPrice': int(self.web3.eth.gasPrice*1.1),
            'nonce': self.web3.eth.getTransactionCount(self.address),
            'value': int(self.web3.toWei(amount_AVAX, 'ether'))
            }
        # создаём транзакцию

        _amountOutMin = self.get_min_out_amount(amount_AVAX)
        transaction = self.contract_complate.functions.swapExactAVAXForTokens(
            _amountOutMin,
            [20],
            ["0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7", # WrappedAVAX
             "0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7"],# Teather
            "0xb13D2e1b6a388e07Ac1AFebf3b7c1d7c924667E4",
            int(time.time()) + 60 * 1
        ).buildTransaction(dict_transaction)
        print(transaction)
        # exit()
        signed_txn = self.web3.eth.account.signTransaction(transaction, self.private)
    # Отправляем, смотрим тут https://testnet.bscscan.com/
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        timeout  = 60  # maximum time to wait for transaction receipt
        hash = self.wait_transaction(txn_hash, timeout)
        return hash
    
    
    
    
    def get_min_out_amount(self, AVAX, USD): 
        """amount in 299.1 format """
        link = "https://api.thegraph.com/subgraphs/name/traderjoe-xyz/joe-v2"
        data = {"query":"\n    query tokenPairLbPairsQuery(\n      $first: Int! = 1\n      $orderBy: String! = \"totalValueLockedUSD\"\n      $orderDirection: String! = \"desc\"\n      $dateAfter: Int! = 1622419200\n    ) {\n      lbpairs(\n        first: $first,\n        orderBy: totalValueLockedUSD\n        orderDirection: desc\n        where: {\n          tokenX_in: [\"0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7\",\"0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7\"],\n          tokenY_in: [\"0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7\",\"0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7\"]\n        }\n      ) {\n        ...lbPairFields\n        ...lbPairHourDataField\n      }\n    }\n    \n  fragment lbPairFields on LBPair {\n    id\n    name\n    binStep\n    baseFeePct\n    tokenXPrice\n    tokenYPrice\n    tokenX {\n      id\n      symbol\n      decimals\n    }\n    tokenY {\n      id\n      symbol\n      decimals\n    }\n    reserveX\n    reserveY\n    totalValueLockedUSD\n    volumeUSD\n    timestamp\n  }\n\n    \n  fragment lbPairHourDataField on LBPair {\n    hourData(\n      first: 24\n      orderBy: date\n      orderDirection: desc\n      where: { date_gt: $dateAfter } # one day away from start of current hour\n    ) {\n      date\n      volumeUSD\n      untrackedVolumeUSD\n      volumeTokenX\n      volumeTokenY\n      feesUSD\n    }\n  }\n\n  ","variables":{"tokens":["0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7","0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7"]},"operationName":"tokenPairLbPairsQuery"}

        response = requests.post(link, json=data)
        json_response = response.json()
        
        fee = float(json_response['data']['lbpairs'][0]["baseFeePct"])*1.2/100
        if AVAX: 
            convert_rate = json_response['data']['lbpairs'][0]["tokenYPrice"]
            USD = float(convert_rate)*(1-fee)*AVAX
            USD = int(USD * 10**6)
        else: 
            convert_rate = json_response['data']['lbpairs'][0]["tokenXPrice"]
            AVAX = float(convert_rate)*(1-fee)*USD 
            AVAX = int(AVAX * 10**18)

        print(fee, convert_rate)
        return AVAX, USD
    
    def testing(self,): 
        
        result = self.contract_complate.functions.wavax().call()
        print(result)
    
    
    
    
    
    def approve_usdt(self, amount: int): 
        contract_usdt = self.web3.eth.contract(address=self.web3.toChecksumAddress(USDT_ADRESS), abi=ABI_USDT_PROXY)
        dict_transaction = {
            'chainId'  : self.web3.eth.chain_id,
            'from'     : self.address,
            # 'to'       : self.web3.toChecksumAddress(USDT_ADRESS),
            'gasPrice' : int(self.web3.eth.gasPrice*1.01),
            'nonce'    : self.web3.eth.getTransactionCount(self.address),
            # 'value': int(self.web3.toWei(priceUSD, 'ether'))
            }
        # создаём транзакцию
        
        transaction = contract_usdt.functions.approve(
            contract_marketplace, int(amount)
        ).buildTransaction(dict_transaction)
        print(transaction)
        # exit()
        signed_txn = self.web3.eth.account.signTransaction(transaction, self.private)

    # Отправляем, смотрим тут https://snowtrace.io
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        timeout  = 60  # maximum time to wait for transaction receipt
        hash = self.wait_transaction(txn_hash, timeout)
        return hash
        
    
    
    def wait_transaction(self, txn_hash, timeout=60): 
        start_time = time.time()

        while True:
            try:
                transaction = self.web3.eth.getTransactionReceipt(txn_hash)
                if transaction is not None:
                    status = int(transaction['status'])
                    print(txn_hash.hex())
                    return txn_hash.hex()
            except Exception as e:
                print(e)

            time.sleep(1)
            elapsed_time = time.time() - start_time
            if elapsed_time >= timeout:
                print(f"Transaction timed out after {timeout} seconds.")
                return txn_hash.hex()
        

    async def smart_contract_function_execution(self,): 
        pass
    
    
    
if __name__ == "__main__":
    httprouter = ' https://api.avax.network/ext/bc/C/rpc'  
    web = WEB3_DRIVER_AVAX(httprouter,my_address,contract_marketplace, ABI_marketplace, secret= os.getenv('MY_SECRET'))
    
    # web.approve_usdt(1)