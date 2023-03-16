import datetime
import time
from pprint import pprint
def list_of_lists_to_one_list(list_of_lists: list): 
    l = [ ]
    for lst in list_of_lists:
        for j in lst: 
            l.append(j)
    return l



def print_floor(results: list):
    floor = []
    for i, result in enumerate(results): 
        i+=1
        if not result['sales']: 
            print('Non shoes')
        else:
            shoe = result['sales'][0]
            print(f'{shoe["primaryProperties"]["Rarity"]:9}{shoe["primaryProperties"]["Type"]:8}mint {shoe["primaryProperties"]["Mint"]:4} LVL {shoe["level"]:4} Price {shoe["priceEth"]:3} BNB')
        if i % 7 == 0:
            print('\n')
            markble = []
            
            for j in range(i-7,i): 
                try:
                    config = results[j]['sales'][0]["priceEth"]
                except IndexError: 
                    config = 0
                markble.append(config)
            floor.append(markble)
    
    return floor









def success_buy_count():
    text = []
    with open('txt/shoe_success.txt','r') as f:
        text = f.readlines()
        print(text)
    with open('txt/shoe_success.txt','w') as f:
        len_text = len(text)
        for i in range(len_text-2): 
            f.write(text[i])
        success_times = text[-2].split(' ')
        f.write(success_times[0]+' '+success_times[1]+' '+str(int(success_times[2].strip('\n'))+1)+'\n')
        f.write(text[-1])


def fail_buy_count():
    text = []
    with open('txt/shoe_success.txt','r') as f:
        text = f.readlines()
        # print(text)
    fail_times =  text[-1].split(' ')
    print(fail_times)
    if fail_times[0] != datetime.datetime.now().strftime('%Y-%m-%d'):
        print('dsjlkfjsdljfklsdklfsdkjflsdfjsdlf')
        with open('txt/shoe_success.txt','w') as f:
            len_text = len(text)
            for i in range(len_text): 
                f.write(text[i])
            f.write(f"\n{datetime.datetime.now().strftime('%Y-%m-%d')} SUCCESS 0\n{datetime.datetime.now().strftime('%Y-%m-%d')} FAIL 0")
            f.close
        with open('txt/shoe_success.txt','r') as f:
            text = f.readlines()
    with open('txt/shoe_success.txt','w') as f:
        len_text = len(text)
        for i in range(len_text-1): 
            f.write(text[i])
        fail_times =  text[-1].split(' ')

        f.write(fail_times[0]+' '+fail_times[1]+' '+str(int(fail_times[2].strip('\n'))+1))
