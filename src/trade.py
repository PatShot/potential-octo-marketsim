from dataclasses import dataclass
from enum import Enum


class TradeDirection(Enum):
    BUY = 'buy'
    SELL = 'sell'


@dataclass
class Trade:
    '''
    An Order becomes a Trade if it is executed.
    '''
    price: int                      # price the trade executed at
    volume: int                     # volume of the trade
    direction: TradeDirection       # direction of the trade (buy-side, sell-side)
    trader_id_already_in_book : int | None # id of the trader that has his order in the book (a limit order)
    trade_id_coming_in_book : int | None # id of trader that is entering the book (mkt or limit)
    order_id_already_in_book : int | None # id of the order already in book, for limit order
    order_id_coming_in_book : int | None # id of the order that has been issued and is being matched with order already in book
    