from datetime import datetime, timezone

# Usage:
# from stock_bar_example import bars, snapshots, ...

class Bars:
    def __init__(self, data):
        self.data = data

bars = Bars(
    data={
        'AMZN': [{
            'symbol': 'AMZN',
            'open': 216.345,
            'high': 216.54,
            'low': 215.4,
            'close': 215.5,
            'volume': 895778.0,
            'trade_count': 15774.0,
            'vwap': 215.925205,
            'timestamp': datetime(2025, 6, 17, 16, 45, tzinfo=timezone.utc)
        }],
        'CVX': [{
            'symbol': 'CVX',
            'open': 149.21,
            'high': 149.3,
            'low': 148.96,
            'close': 149.055,
            'volume': 221263.0,
            'trade_count': 4665.0,
            'vwap': 149.176898,
            'timestamp': datetime(2025, 6, 17, 16, 45, tzinfo=timezone.utc)
        }],
        'MSFT': [{
            'symbol': 'MSFT',
            'open': 477.93,
            'high': 478.21,
            'low': 477.0,
            'close': 477.245,
            'volume': 275423.0,
            'trade_count': 8473.0,
            'vwap': 477.5658,
            'timestamp': datetime(2025, 6, 17, 16, 45, tzinfo=timezone.utc)
        }]
    }
)

snapshots = {
    'AMZN': {
        'symbol': 'AMZN',
        'daily_bar': {
            'symbol': 'AMZN',
            'open': 215.165,
            'high': 217.39,
            'low': 214.58,
            'close': 214.82,
            'volume': 924027.0,
            'trade_count': 12907.0,
            'vwap': 216.061027,
            'timestamp': datetime(2025, 6, 17, 4, 0, tzinfo=timezone.utc)
        },
        'latest_quote': {
            'symbol': 'AMZN',
            'ask_exchange': ' ',
            'ask_price': 0.0,
            'ask_size': 0.0,
            'bid_exchange': 'V',
            'bid_price': 214.79,
            'bid_size': 1.0,
            'conditions': ['R'],
            'tape': 'C',
            'timestamp': datetime(2025, 6, 17, 20, 0, 0, 785, tzinfo=timezone.utc)
        },
        'latest_trade': {
            'symbol': 'AMZN',
            'conditions': ['@'],
            'exchange': 'V',
            'id': 12901,
            'price': 214.82,
            'size': 100.0,
            'tape': 'C',
            'timestamp': datetime(2025, 6, 17, 19, 59, 59, 544580, tzinfo=timezone.utc)
        },
        'minute_bar': {
            'symbol': 'AMZN',
            'open': 214.94,
            'high': 215.0,
            'low': 214.81,
            'close': 214.82,
            'volume': 21403.0,
            'trade_count': 338.0,
            'vwap': 214.884431,
            'timestamp': datetime(2025, 6, 17, 19, 59, tzinfo=timezone.utc)
        },
        'previous_daily_bar': {
            'symbol': 'AMZN',
            'open': 212.35,
            'high': 217.05,
            'low': 211.63,
            'close': 216.16,
            'volume': 993188.0,
            'trade_count': 12556.0,
            'vwap': 215.242246,
            'timestamp': datetime(2025, 6, 16, 4, 0, tzinfo=timezone.utc)
        }
    },
    'CVX': {
        'symbol': 'CVX',
        'daily_bar': {
            'symbol': 'CVX',
            'open': 147.415,
            'high': 149.96,
            'low': 146.51,
            'close': 148.88,
            'volume': 208132.0,
            'trade_count': 4143.0,
            'vwap': 148.953115,
            'timestamp': datetime(2025, 6, 17, 4, 0, tzinfo=timezone.utc)
        },
        'latest_quote': {
            'symbol': 'CVX',
            'ask_exchange': 'V',
            'ask_price': 151.0,
            'ask_size': 5.0,
            'bid_exchange': 'V',
            'bid_price': 148.86,
            'bid_size': 1.0,
            'conditions': ['R'],
            'tape': 'A',
            'timestamp': datetime(2025, 6, 17, 19, 59, 59, 846146, tzinfo=timezone.utc)
        },
        'latest_trade': {
            'symbol': 'CVX',
            'conditions': [' '],
            'exchange': 'V',
            'id': 52983828346687,
            'price': 148.88,
            'size': 100.0,
            'tape': 'A',
            'timestamp': datetime(2025, 6, 17, 19, 59, 47, 778096, tzinfo=timezone.utc)
        },
        'minute_bar': {
            'symbol': 'CVX',
            'open': 148.93,
            'high': 148.965,
            'low': 148.825,
            'close': 148.88,
            'volume': 5422.0,
            'trade_count': 149.0,
            'vwap': 148.9014,
            'timestamp': datetime(2025, 6, 17, 19, 59, tzinfo=timezone.utc)
        },
        'previous_daily_bar': {
            'symbol': 'CVX',
            'open': 145.65,
            'high': 146.82,
            'low': 143.76,
            'close': 146.1,
            'volume': 291208.0,
            'trade_count': 4662.0,
            'vwap': 145.167405,
            'timestamp': datetime(2025, 6, 16, 4, 0, tzinfo=timezone.utc)
        }
    },
    'MSFT': {
        'symbol': 'MSFT',
        'daily_bar': {
            'symbol': 'MSFT',
            'open': 475.33,
            'high': 478.7,
            'low': 474.08,
            'close': 477.95,
            'volume': 329069.0,
            'trade_count': 8190.0,
            'vwap': 476.706816,
            'timestamp': datetime(2025, 6, 17, 4, 0, tzinfo=timezone.utc)
        },
        'latest_quote': {
            'symbol': 'MSFT',
            'ask_exchange': 'V',
            'ask_price': 480.0,
            'ask_size': 6.0,
            'bid_exchange': 'V',
            'bid_price': 474.0,
            'bid_size': 1.0,
            'conditions': ['R'],
            'tape': 'C',
            'timestamp': datetime(2025, 6, 17, 19, 59, 53, 895584, tzinfo=timezone.utc)
        },
        'latest_trade': {
            'symbol': 'MSFT',
            'conditions': ['@'],
            'exchange': 'V',
            'id': 8187,
            'price': 477.95,
            'size': 100.0,
            'tape': 'C',
            'timestamp': datetime(2025, 6, 17, 19, 59, 57, 152966, tzinfo=timezone.utc)
        },
        'minute_bar': {
            'symbol': 'MSFT',
            'open': 477.87,
            'high': 478.1,
            'low': 477.8,
            'close': 477.95,
            'volume': 5758.0,
            'trade_count': 179.0,
            'vwap': 477.968402,
            'timestamp': datetime(2025, 6, 17, 19, 59, tzinfo=timezone.utc)
        },
        'previous_daily_bar': {
            'symbol': 'MSFT',
            'open': 475.355,
            'high': 480.595,
            'low': 475.06,
            'close': 479.06,
            'volume': 409355.0,
            'trade_count': 8101.0,
            'vwap': 479.165701,
            'timestamp': datetime(2025, 6, 16, 4, 0, tzinfo=timezone.utc)
        }
    }
}