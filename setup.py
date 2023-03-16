
from decimal import Decimal


print(46511627906976744 * 21.5)
deltaIds = (-27,-26,-25,-24,-23,-22,-21,-20,-19,-18,-17,-16,-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12)

def calculate_range_pricing_for_pool(delta): 
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




    # print(distributionX)   
    # print(distributionY) 
    # return distributionX, distributionY



# calculate_range_pricing_for_pool(deltaIds)
# number = qunatity_not_zero
# truncate_position = 16  # specify the position up to which you want to keep the digits

# # convert number to a string
# number_str = str(number)

# # find the position of the decimal point
# decimal_pos = number_str.find('.')

# if decimal_pos == -1:
#     # if there is no decimal point, just return the original number as integer
#     result = int(number)
# else:
#     # take only the required number of digits before and including the truncate_position
#     result_str = number_str[:decimal_pos + truncate_position + 1]

#     # remove any extra zeroes in the end of the string
#     while result_str[-1] == '0':
#         result_str = result_str[:-1]
    
#     # if the final character is decimal point, remove it too
#     if result_str[-1] == '.':
#         result_str = result_str[:-1]

#     # convert the string back to float or int depending on need
#     if result_str.find('.') == -1:
#         result = int(result_str)
#     else:
#         result = float(result_str)

# print(result)