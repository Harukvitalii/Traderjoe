
import json
import requests
import asyncio
import time

from storage   import ADMIN, BOT_API
from traderjoe import web_driver_avax

from pprint   import pp
from dotenv   import load_dotenv

from arequestsHelper import AREQUEST_MANAGER 



load_dotenv()

usdt_left = 2200
avax_left = 0
avax_fee  = 1


class TraderJoe(AREQUEST_MANAGER): 
    time_sleep       = 120
    bin_range        = 23
    POOL             = 'AVAX-USDt'
    web3_avax        = web_driver_avax

    
    def __init__(self, BOT_API, ADMIN_ID):
        super().__init__(BOT_API, ADMIN_ID)

        self.bin_ids          = self.get_bin_ids()
        
        
    
    async def main(self,*args): 

        pool  = self.load_from_range()
        binId = self.get_last_bin_by_swap()
        price = self.get_current_price_by_bidId(binId)
        # ми маєм мати діапазаон ціни в якому у нас уже бул знаходиться 
    # якщо ми доходимо до однієї із сторін кінця пула,
        print(price, binId)
        if pool['price_low'] >= price: 
            # Пул опустился ниже ренджа
            # 1) забераєм весь пул.
            balance_before = self.web3_avax.balance
            self.web3_avax.remove_liquidity_pool_AVAX(self.POOL, side= "low")
            
            if self.web3_avax.balance <= balance_before:
                self.bot_notify_normal(f'remove liqv avax failed stopping')
                time.sleep(10000000)
            removed_liqv = round(float(self.web3_avax.balance),4) - avax_left - avax_fee 
            # #сделано чтоби добавить ликвидность в айдишку на которой стоим две пари по полам
            #                                                       coef для свечи на которой добавляем, если 0.5 = 1, 0.75 = 1.25
            to_left_avax = removed_liqv/(self.bin_range//2 + 0.5) * 0.75
            # #
            removed_liqv = removed_liqv - to_left_avax
            
            # 2) свапаєм, щоб було дві монети
            # якщо ми забераємо ліквідність зверху, то це тільки AVAX
            sucs, amount_USDT = self.web3_avax.swap_trader_joe_avax_to_alt(amount_AVAX=removed_liqv)
            if not sucs:
                self.bot_notify_normal(f'Swap failed amount {removed_liqv}')
                time.sleep(10000000)
            # # 3) закидаємо знову в пул.
            midpoint = self.bin_range // 2
            if self.bin_range % 2 == 0:
                num_list = [num for num in range(-midpoint, 1)]
            else: 
                num_list = [num for num in range(-midpoint, 1)]
            sucs = self.web3_avax.add_liquidity_pool_AVAX(num_list, binId, to_left_avax, amount_USDT, side = 'low')
            #86956521739130430
            #86956521739130432
            #43478260869565216
            if not sucs:
                self.bot_notify_normal(f'add liquidity fail {amount_USDT} side low')
                time.sleep(10000000)
            # 4) ставимо новий діапазон
            for i, bin in enumerate(self.bin_ids):
                if bin['binId'] == binId: 
                    price_low   = self.bin_ids[i + num_list[0]]['priceXY']
            self.update_json_pool('price_low',price_low)
            self.bot_notify_normal(f'Seccussfully reentered {self.POOL}')
            exit()

        
        elif price>= pool['price_high']:
            # Пул поднялся више ренджа
            # 1) забераєм весь пул.
            balance_before = self.web3_avax.usdt_balance
            self.web3_avax.remove_liquidity_pool_AVAX(self.POOL, side= "high")
            
            if self.web3_avax.usdt_balance <= balance_before:
                self.bot_notify_normal(f'remove liqv avax failed stopping')
                time.sleep(10000000)
                
            removed_liqv = self.web3_avax.usdt_balance - usdt_left 
            to_left_usdt = removed_liqv/(self.bin_range//2 + 0.5) * 0.5
            #
            removed_liqv = removed_liqv - to_left_usdt
            # 2) свапаєм, щоб було дві монети
            # якщо ми забераємо ліквідність зверху, то це тільки AVAX
            sucs, amount_out = self.web3_avax.swap_trader_joe_alt_to_avax(removed_liqv)
            if not sucs:
                self.bot_notify_normal(f'Swap failed amount {removed_liqv}')
                time.sleep(10000000)
                
            # 3) закидаємо знову в пул.
            midpoint = self.bin_range // 2
            if self.bin_range % 2 == 0:
                num_list = [num for num in range(0, midpoint+1)]
            else: 
                num_list = [num for num in range(0, midpoint+1)]
                
            sucs = self.web3_avax.add_liquidity_pool_AVAX(num_list, binId, amount_AVAX = amount_out, amountUSDT=to_left_usdt, side = 'high')
            #
            if not sucs:
                self.bot_notify_normal(f'add liquidity fail {amount_out}AVAX, {to_left_usdt} USDT side high')
                time.sleep(10000000)
            # 4) ставимо новий діапазон
            for i, bin in enumerate(self.bin_ids):
                if bin['binId'] == binId: 
                    price_high   = self.bin_ids[i + num_list[0]]['priceXY']
            self.update_json_pool('price_high',price_high)
        else: 
            print('working in range')
        #TO DO 
        # 1) хедж на бинансе
        
        
    def calculate_amount (self):
        
        return 
    
    
    def update_json_pool(self,key, value, file_name ="./project/data_avaxusdt.json"):
        #save 2 variables to json file  
        with open(file_name, 'r') as f:
            data = json.load(f)

        data[key] = value

        with open(file_name, 'w') as f:
            json.dump(data, f)
            
                    
    def load_from_range(self, file_name="./project/data_avaxusdt.json"): 
        with open(file_name, 'r') as f:
            return json.load(f)    
    
    
    def calculate_new_range(self, num_list, bin_id): 
        pass 
    
        for i, bin in enumerate(self.bin_ids):
            if bin['binId'] == bin_id: 
                price_low  = self.bin_ids[i + num_list[0]]
                price_high = self.bin_ids[i + num_list[-1]]
        return price_low, price_high


    def get_bin_ids(self, *args): 
        avax_usdt_pool = "0xdF3E481a05F58c387Af16867e9F5dB7f931113c9"
        link = f'https://barn.traderjoexyz.com/v1/bin/avalanche/{avax_usdt_pool}/8376193?filterBy=1d&radius=400'
        resp = requests.get(link)
        resp = resp.json()
        return resp
    
    def get_current_price(self,PAIR=None): 
        link = "https://api.thegraph.com/subgraphs/name/traderjoe-xyz/exchange"
        #TO DO change currencies curernct pair USDt - AVAX
        data = {"query":"\n    query pairDetailQuery(\n      $first: Int! = 1\n      $orderBy: String! = \"trackedReserveAVAX\"\n      $orderDirection: String! = \"desc\"\n      $dateAfter: Int! = "+ str(int(time.time()-1)) +"\n    ) {\n      pairs (first: $first, orderBy: $orderBy, orderDirection: $orderDirection, \n        where: {\n          token0_in: [\"0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7\",\"0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7\"],\n          token1_in: [\"0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7\",\"0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7\"]\n        }) {\n        id\n        name\n        token0Price\n        token1Price\n        token0 {\n          id\n          symbol\n          name\n          decimals\n          derivedAVAX\n        }\n        token1 {\n          id\n          symbol\n          name\n          decimals\n          derivedAVAX\n        }\n        reserve0\n        reserve1\n        reserveUSD\n        volumeUSD\n        hourData(first: 24, where: {date_gt: $dateAfter}, orderBy: date, orderDirection: \"desc\") {\n          volumeUSD\n          untrackedVolumeUSD\n          date\n          volumeToken0\n          volumeToken1\n        }  \n        timestamp\n      }\n    }\n  ",
                "variables":{"dateAfter":int(time.time()-1)},"operationName":"pairDetailQuery"}
        
        resp = requests.post(link, json=data)
        resp = resp.json()
        return float(resp["data"]["pairs"][0]["token0Price"])
    
    
    def get_last_bin_by_swap(self, lbPair=None): 
        data = {"query":"\n  query lbPairSwaps($first: Int! = 10, $lbPair: String!, $dateAfter: Int!) {\n    swaps(\n      first: $first\n      orderBy: timestamp\n      orderDirection: desc\n      where: { lbPair: $lbPair, timestamp_gte: $dateAfter }\n    ) {\n      activeId\n      amountUSD\n      amountXIn\n      amountXOut\n      amountYIn\n      amountYOut\n      timestamp\n    }\n  }\n",
                "variables":{"dateAfter":int(time.time())-2*60*60,"first":10,"lbPair":"0xdf3e481a05f58c387af16867e9f5db7f931113c9"},"operationName":"lbPairSwaps"}
        link = "https://api.thegraph.com/subgraphs/name/traderjoe-xyz/joe-v2"
        resp = requests.post(link, json=data)
        resp = resp.json()
        return int(resp["data"]["swaps"][0]["activeId"])
    
    
    def get_current_price_by_bidId(self,binId): 
        r  = self.get_bin_ids()
        for i in r: 
            if int(i['binId']) == binId: 
                return float(i['priceXY'])
        self.bot_notify_normal('Error in get_current_price_by_bidId OUT OF RANGE 13-30 за авакс FIX FIX FIX')
            
        
    async def run_main_forever(self, *args):
        while True:
            await self.main(*args)
            await asyncio.sleep(1)  # Wait for 60 seconds before running again
        
        
if __name__ == "__main__":
    Pool = TraderJoe(BOT_API, ADMIN)

    Pool.run_function_with_exception(Pool.run_main_forever, 'TraderJoe Pool', otladka=1)  





