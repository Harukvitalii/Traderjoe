from web3 import Web3
from storage import my_address, contract_marketplace, ABI_marketplace
from storage  import USDT_ADRESS, ABI_USDT_PROXY, COIN_ADRESSES
from dotenv import load_dotenv
from pprint import pp
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


GAS_FEE_RATE = 1

# якщо будет використовувати, можуть буди помилски, але це збереже від проскальзивания при ремуве из пула 
USING_MIN_AMOUNT = False


class WEB3_DRIVER_AVAX: 
    timeout = 60 #sec
    
    def __init__(self,privider_link, address, contract, ABI, private=None,secret=None): 
        web3 = Web3(Web3.HTTPProvider(privider_link))
        
        self.web3      = web3
        self.address   = web3.to_checksum_address(address)   
        if secret: 
            self.private = Account.from_mnemonic(secret)._private_key.hex()
        else: 
            self.private       = private
        self.contract_complate = self.web3.eth.contract(address=contract, abi=ABI)
        
        self.usdt_contract     = self.web3.eth.contract(address=self.web3.to_checksum_address(USDT_ADRESS), abi=ABI_USDT_PROXY)
        
        self                    .update_balances()

        print(web3.is_connected(), '\nbalance:   ', round(self.balance,3), 'AVAX')
        print('balance USDT: ', round(self.usdt_balance/10**6,3), 'USDT')
        
    
    
    def add_liquidity_pool_AVAX(self, num_list ,central_binId: int, amount_AVAX=None , amountUSDT=None, side = None): 
        # создаём транзакцию
        # amountX, amountY = self.get_min_out_amount(amount_AVAX, amountUSDT)
        distributionX, distributionY = self.calculate_range_pricing_for_pool(num_list, side)
        
        args = (
            self.web3.to_checksum_address("0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7"),
            self.web3.to_checksum_address("0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7"),
            20,
            int(amount_AVAX*10**18),
            int(amountUSDT),
            int(amount_AVAX*10**18*0.999),
            int(amountUSDT*0.999),
            int(central_binId),#TO DO
            2, #const
            num_list,
            distributionX,
            distributionY,
            self.address,
            int(time.time()) + 60 * 2)
        pp(args)
        transaction = self.contract_complate.functions.addLiquidityAVAX(
            args
        ).build_transaction(self.dict_transact(amount_AVAX))
        print(transaction)
        # exit()
        signed_txn = self.web3.eth.account.sign_transaction(transaction, self.private)
    # Отправляем, смотрим тут https://testnet.bscscan.com/
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        hash     = self.wait_transaction(txn_hash)
        self.update_balances()
        return hash
    
    
    def calculate_range_pricing_for_pool(self, delta, side = 'low'): 

        zero_index = delta.index(0)
        array1 = delta[:zero_index+1]
        array2 = delta[zero_index:]
        # print(array1)
        qunatity_not_zero = 1*10**18/(len(array2)-0.5)
        qunatity_not_zero = int(Decimal(qunatity_not_zero).to_integral_value())
        
        qunatity_zero = qunatity_not_zero/2
        qunatity_zero = int(Decimal(qunatity_zero).to_integral_value())
        
        distributionX = [0]*(len(array1)-1) + [qunatity_zero] + [qunatity_not_zero]*(len(array2)-1)
        

        qunatity_not_zero = 1*10**18/(len(array1)-0.5)
        qunatity_not_zero = int(Decimal(qunatity_not_zero).to_integral_value())
        
        qunatity_zero     = qunatity_not_zero/2
        qunatity_zero = int(Decimal(qunatity_zero).to_integral_value())
        distributionY = [qunatity_not_zero]*(len(array1)-1) +  [qunatity_zero] + [0]*(len(array2)-1)
        if side == 'low': 
            distributionX = distributionX
            return distributionX, distributionY 
        
        elif side == 'high':
            distributionY = distributionY
            return distributionX, distributionY 
    
    
    
    def remove_liquidity_pool_AVAX(self, pair, side): 

        liq_data = self.get_liquidity_data(pair)
        liq_pos = liq_data['userBinLiquidities'] # list
        ids, amounts = [], []
        
        if side   == 'low' : liq_pos = liq_pos[len(liq_pos)//2:]
        elif side == 'high': liq_pos = liq_pos[:len(liq_pos)//2]
        else               : pass
        
        for lb in liq_pos: 
            ids    .append(int(lb['binId']))
            amounts.append(int(lb['liquidity']))
        
        
        # создаём транзакцию
        #TO DO  FIND A WAY TO GET IDS WITH MY LIQUIDITY OR WRITE IT ON THE ADDLIQUIDITY FUNCION IN FILE OR WHATEVER 
        # address _tokenX,address _tokenY,uint16 _binStep,uint256 _amountXMin,uint256 _amountYMin,uint256[] _ids,uint256[] _amounts,address _to,uint256 _deadline
        pair1, pair2 = pair.split('-')[0],pair.split('-')[1] 
        _tokenX	     = str(self.web3.to_checksum_address(COIN_ADRESSES[pair1]['address']))
        _tokenY	     = str(self.web3.to_checksum_address(COIN_ADRESSES[pair2]['address']))
        _binStep     = int(liq_data['lbPair']['binStep'])
        _ids         = ids
        _amounts     = amounts
        _to_address  = str(self.address)
        _deadline    = int(time.time()) + 60 * 2
        if USING_MIN_AMOUNT: 
            _amountXMin, _amountYMin  = 0, 0 #get_min_amount_tokenX_tokenY(pair1, pair2, _binStep)
        else:_amountXMin, _amountYMin = 0, 0
        transaction  = self.contract_complate.functions.removeLiquidityAVAX(
            _tokenY,
            _binStep,
            _amountXMin,
            _amountYMin,
            _ids,
            _amounts,
            _to_address,
            _deadline,
        ).build_transaction(self.dict_transact())
        print(transaction)
        # exit()
        signed_txn = self.web3.eth.account.sign_transaction(transaction, self.private)
    # Отправляем, смотрим тут https://testnet.bscscan.com/
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        hash = self.wait_transaction(txn_hash)
        self.update_balances()
        return hash
    
        
    
    def collectFees(self, pair): 
        liq_data = self.get_liquidity_data(pair)
        liq_possitions = liq_data['userBinLiquidities'] # list
        
        all_bins_with_my_liquidity  = [int(lb['binId']) for lb in liq_possitions]
        

        # создаём транзакцию
        #TO DO  FIND A WAY TO GET IDS WITH MY LIQUIDITY OR WRITE IT ON THE ADDLIQUIDITY FUNCION IN FILE OR WHATEVER 
        transaction = self.contract_complate.functions.collectFees(
            self.address,  #my adress
            all_bins_with_my_liquidity

        ).build_transaction(self.dict_transact())
        print(transaction)
        # exit()
        signed_txn = self.web3.eth.account.sign_transaction(transaction, self.private)
        # Отправляем, смотрим тут https://testnet.snowtrace.com/
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        hash     = self.wait_transaction(txn_hash)
        self.update_balances()
        return hash

    
    def swap_trader_joe_avax_to_alt(self, amount_AVAX): 
        # создаём транзакцию
        # Пари нужно вводить акуратно
        amount_in, _amountOutMin = self.get_min_out_amount('AVAX-USDt', amount_AVAX)
        print(amount_in, _amountOutMin)
        transaction = self.contract_complate.functions.swapExactAVAXForTokens(
            _amountOutMin,
            [20],
            [
                "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7", #wAVAX
                # "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E", #usdc
                "0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7" #usdt
            ],
            self.address,
            int(time.time()) + 60 * 1
        ).build_transaction(self.dict_transact(amount_AVAX))
        print(transaction)
        # exit()
        signed_txn = self.web3.eth.account.sign_transaction(transaction, self.private)
    # Отправляем, смотрим тут https://testnet.bscscan.com/
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        hash     = self.wait_transaction(txn_hash)
        self.update_balances()
        return hash, _amountOutMin
    
    def swap_trader_joe_alt_to_avax(self, amount_alt): 

        # создаём транзакцию
        # Пари нужно вводить акуратно
        amount_in, _amountOutMin = self.get_min_out_amount('USDt-AVAX', amount_alt)
        print(amount_in, _amountOutMin)
        transaction = self.contract_complate.functions.swapExactTokensForAVAX(
            amount_in,
            _amountOutMin,
            [0],
            [
                "0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7", #USDT
                "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7", # WrappedAVAX
             ],# Teather
            "0xb13D2e1b6a388e07Ac1AFebf3b7c1d7c924667E4",
            int(time.time()) + 60*2
        ).build_transaction(self.dict_transact())
        print(transaction)
        # exit()
        signed_txn = self.web3.eth.account.sign_transaction(transaction, self.private)
    # Отправляем, смотрим тут https://testnet.bscscan.com/
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        hash     = self.wait_transaction(txn_hash)
        self.update_balances()
        return hash, _amountOutMin
    
    
    
    
    
    def get_min_out_amount(self, pair, amount_in): 
        """amount in 100.1 format """
        pair2  = pair.split('-')[1]
        
        liq_data = self.get_liquidity_data(pair)['lbPair']
        
        tokenX_zeroes = liq_data["tokenX"]["decimals"]
        tokenY_zeroes = liq_data["tokenY"]["decimals"]
        
        fee = float(liq_data["baseFeePct"])*2/100
        
        if liq_data["tokenY"]['symbol'] == pair2: 
            print("not reverse")
            convert_rate = liq_data["tokenYPrice"]
            token_out = float(convert_rate)*(1-fee)*amount_in
            token_out = int(token_out * 10**int(tokenY_zeroes))
        else: 
            convert_rate = liq_data["tokenXPrice"]
            token_out = float(convert_rate)*(1-fee)*amount_in
            token_out = int(token_out * 10**int(tokenX_zeroes))
            
            
        print(fee, convert_rate)
        return amount_in, token_out
    
    
    
    def get_liquidity_data(self,pair): 
        pair1  = pair.split('-')[0]
        pair2  = pair.split('-')[1]
        address_in  = COIN_ADRESSES[pair1]['address']
        address_out = COIN_ADRESSES[pair2]['address']
        print(address_in, address_out)
        # [self.web3_avax.web3.to_checksum_address(addr1), self.web3_avax.web3.to_checksum_address(addr2)]
        link = "https://api.thegraph.com/subgraphs/name/traderjoe-xyz/joe-v2"
        
        data = {"query":"\n  query liquidityPositions(\n    $first: Int! = 1000\n    $user: Bytes!\n    $lbPairAddr: String!\n  ) {\n    liquidityPositions(\n      first: $first\n      where: { lbPair: $lbPairAddr, user: $user, binsCount_gt: 0 }\n    ) {\n      id\n      binsCount\n      userBinLiquidities(first: 1000, where: { liquidity_gt: 0 }) {\n        liquidity\n        binId\n      }\n      user {\n        id\n      }\n      lbPair {\n        ...lbPairFields\n      }\n    }\n  }\n  \n  fragment lbPairFields on LBPair {\n    id\n    name\n    binStep\n    baseFeePct\n    tokenXPrice\n    tokenYPrice\n    tokenX {\n      id\n      symbol\n      decimals\n    }\n    tokenY {\n      id\n      symbol\n      decimals\n    }\n    reserveX\n    reserveY\n    totalValueLockedUSD\n    volumeUSD\n    timestamp\n  }\n\n",
                "variables":{"lbPairAddr":"0xdf3e481a05f58c387af16867e9f5db7f931113c9","user":"0xb13d2e1b6a388e07ac1afebf3b7c1d7c924667e4"},
                "operationName":"liquidityPositions"}
        
        response = requests.post(link, json=data)
        json_response = response.json()
        
        return json_response['data']['liquidityPositions'][0]
    
    
    def testing(self,): 
        
        result = self.contract_complate.functions.wavax().call()
        print(result)
    
    
    
    
    
    def approve_usdt(self, amount: int): 
        contract_usdt = self.usdt_contract
        # создаём транзакцию
        
        transaction = contract_usdt.functions.approve(
            contract_marketplace, int(amount)
        ).build_transaction(self.dict_transact())
        print(transaction)
        # exit()
        signed_txn = self.web3.eth.account.sign_transaction(transaction, self.private)

    # Отправляем, смотрим тут https://snowtrace.io
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        hash = self.wait_transaction(txn_hash)
        return hash
        
        
    def dict_transact(self,amount_AVAX=None): 
        
        dict_transaction = {
            'chainId': self.web3.eth.chain_id,
            'from': self.address,
            'gasPrice': int(self.web3.eth.gas_price*GAS_FEE_RATE),
            'nonce': self.web3.eth.get_transaction_count(self.address),
            }
        if amount_AVAX: 
            dict_transaction['value'] = int(self.web3.to_wei(amount_AVAX, 'ether'))
        
        return dict_transaction
    
    def wait_transaction(self, txn_hash): 
        time.sleep(5)

        # Wait for the transaction receipt
        start_time = time.time()
        while time.time() < start_time + self.timeout:
            try:
                receipt = self.web3.eth.wait_for_transaction_receipt(txn_hash, timeout=self.timeout)
            except:
                continue
            if receipt.status == 1:
                # Transaction was successful
                return True
            else:
                # Transaction failed
                return False
        # Transaction was not mined within 2 minutes
        return False
        
    def update_balances(self,): 
        self.balance           = self.web3.from_wei(self.web3.eth.get_balance(self.web3.to_checksum_address(self.address)), 'ether')
        self.usdt_balance      = self.usdt_contract.functions.balanceOf(self.address).call()
    
    
if __name__ == "__main__":
    httprouter = ' https://api.avax.network/ext/bc/C/rpc'  
    web = WEB3_DRIVER_AVAX(httprouter,my_address,contract_marketplace, ABI_marketplace, secret= os.getenv('MY_SECRET'))
    
    # web.swap_trader_joe_avax_to_alt(1)