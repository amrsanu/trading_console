from enum import Enum


class OrderType(Enum):
    """_summary_

    Args:
        Enum (_type_): _description_
    """
    LIMIT_ORDER = 1
    MARKET_ORDER = 2
    STOP_ORDER = 3
    STOPLIMIT_ORDER = 4


class OrderStatus(Enum):
    """_summary_

    Args:
        Enum (_type_): _description_
    """
    CANCELLED = 1
    TRADED_FILLED = 2
    FUTURE_USE = 3
    TRANSIT = 4
    REJECTED = 5
    PENDING = 6


class OrderSlides(Enum):
    """_summary_

    Args:
        Enum (_type_): _description_
    """
    SELL = -1
    BUY = 1
