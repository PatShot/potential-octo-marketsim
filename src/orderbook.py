# An orderbook for Market Orders
# import numpy as np
# from prettytable import PrettyTable
from dataclasses import dataclass
from typing import List, Dict
from order import OrderData, OrderTypes
from trade import Trade, TradeDirection
import sys
import logging

@dataclass
class BookData:
    price: int
    quantity: int
    order_id: int
    trader_id: int


class OrderBook():
    '''
    Main Order 
    '''
    def __init__(self) -> None:
        self.bids: List[BookData] = [] 
        self.asks: List[BookData] = []

        self.trades: Dict[int, List[Trade]] = {}
        self.time = 0

        self.price_sequence = [] # sequence of executed prices.
        self.volumes_sequence = [] # sequence of the volumes of the executed prices.

        self.last_best_bid_price: int  = -1
        self.last_best_ask_price: int  = -1
        self.last_best_bid_volume: int  = -1
        self.last_best_ask_volume: int = -1

    @staticmethod
    def convert_order_to_book(order: OrderData, order_id: int) -> BookData:
        return BookData(price=order.price, quantity=order.quantity, trader_id=order.trader_id, order_id=order_id)

    def add_to_bids(self, book_data: BookData) -> None:
        self.bids.append(book_data)

    def add_to_asks(self, book_data: BookData) -> None:
        self.asks.append(book_data)

    def execute_market_order(self, quantity: int, order_type: OrderTypes, order_id: int, trader_id: int):
        '''
        Execute order at the first available bid or ask
        depending on whether selling or buying
        '''
        
        match(order_type):
            case OrderTypes.market_buy:
                try:
                    best_available_ask: BookData = self.asks.pop(0)
                    print(best_available_ask)
                except Exception as e:
                    logging.log(2, e)
                    best_available_ask = BookData(sys.maxsize, 0, -1, -1)

                if quantity >= best_available_ask.quantity:
                    self.trades[self.time].append(
                        Trade(
                            price=best_available_ask.price,
                            volume=best_available_ask.quantity,
                            direction=TradeDirection.BUY,
                            trade_id_coming_in_book=best_available_ask.trader_id,
                            trader_id_already_in_book=trader_id,
                            order_id_already_in_book=best_available_ask.order_id,
                            order_id_coming_in_book=order_id
                        )
                    )

                    # Recursion to continue till the quantity in the order runs out.
                    self.execute_market_order(quantity=quantity-best_available_ask.quantity, order_type=OrderTypes.market_buy, order_id=order_id, trader_id=trader_id)
                else:
                    if quantity != 0:
                        self.trades[self.time].append(
                            Trade(
                                price=best_available_ask.price,
                                volume=quantity,
                                direction=TradeDirection.BUY,
                                trader_id_already_in_book=best_available_ask.trader_id,
                                trade_id_coming_in_book=trader_id,
                                order_id_already_in_book=best_available_ask.order_id,
                                order_id_coming_in_book=order_id
                            )
                        )
                    # Since best ask has been popped, we need to put it back in with updated volume (if total volume of ask isn't bought).
                    self.add_to_asks(BookData(best_available_ask.price,best_available_ask.quantity-quantity, best_available_ask.order_id, best_available_ask.trader_id))
                    self.asks = sorted(self.asks, key= lambda x: (x[0], x[2]))
            case OrderTypes.market_sell:
                try:
                    best_available_bid: BookData = self.bids.pop(0)
                    print(best_available_bid)
                except Exception as e:
                    logging.log(2, e)
                    best_available_bid = BookData(sys.maxsize, -1, -1, -1)

                if quantity >= best_available_bid.quantity:
                    self.trades[self.time].append(
                        Trade(
                            price=best_available_bid.price,
                            volume=best_available_bid.quantity,
                            direction=TradeDirection.SELL,
                            trade_id_coming_in_book=best_available_bid.trader_id,
                            trader_id_already_in_book=trader_id,
                            order_id_already_in_book=best_available_bid.order_id,
                            order_id_coming_in_book=order_id
                        )
                    )

                    # Recursion to continue till the quantity in the order runs out.
                    self.execute_market_order(quantity=quantity-best_available_bid.quantity, order_type=OrderTypes.market_buy, order_id=order_id, trader_id=trader_id)
                else:
                    if quantity != 0:
                        self.trades[self.time].append(
                            Trade(
                                price=best_available_bid.price,
                                volume=quantity,
                                direction=TradeDirection.BUY,
                                trader_id_already_in_book=best_available_bid.trader_id,
                                trade_id_coming_in_book=trader_id,
                                order_id_already_in_book=best_available_bid.order_id,
                                order_id_coming_in_book=order_id
                            )
                        )
                    # Since best ask has been popped, we need to put it back in with updated volume (if total volume of ask isn't bought).
                    self.add_to_bids(BookData(best_available_bid.price,best_available_bid.quantity-quantity, best_available_bid.order_id, best_available_bid.trader_id))
                    self.bids = sorted(self.asks, key= lambda x: (x[0], x[2]))
            case OrderTypes.limit_buy:
                pass
            case OrderTypes.limit_sell:
                pass
            case OrderTypes.modify_limit_buy:
                pass
            case OrderTypes.modify_limit_sell:
                pass
            case _:
                raise ValueError("Order Type is not part of defined Order Types.")