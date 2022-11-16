from enum import Enum


class Currency(Enum):
    USD = "oficial"
    USD_BLUE = "blue"
    EURO = "oficial_euro"
    EURO_BLUE = "blue_euro"
    ARS = "ars"


class OperationType(Enum):
    BUY = "value_buy"
    SELL = "value_sell"


CURRENCY_NAMES = [data.name for data in Currency]
