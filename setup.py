
from decimal import Decimal

delta = list(range(-11, 1))
delta = list(range(0, 12))

print(delta)
def calculate_range_pricing_for_pool( delta, side = 'low'): 

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
    

x, y = calculate_range_pricing_for_pool(delta, 'low')
print(x)
print(len(x))
print(y)
print(len(y))

print(sum(x), sum(y), )
