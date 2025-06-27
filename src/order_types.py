from enum import Enum

order_type_translate = {
    '0': 'do_nothing',
    '1': 'market_buy',
    '2': 'market_sell',
    '3': 'limit_buy',
    '4': 'limit_sell',
    '5': 'modify_limit_buy',
    '6': 'modify_limit_sell'
}

class OrderTypes(Enum):
    do_nothing = '0'
    market_buy = '1'
    market_sell = '2'
    limit_buy = '3'
    limit_sell = '4'
    modify_limit_buy = '5'
    modify_limit_sell = '6'