from abc import ABC, abstractmethod
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass, AssetStatus
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockSnapshotRequest
import os
import json


############## Stock Data ##############

class StockData:

    def __init__(self, ticker):
        self.ticker = ticker
        self.cur_price = None
        self.cur_vol = None
        self.prev_high = None
        self.open_price = None

    def set_prev_high(self, prev_high):
        self.prev_high = prev_high
    
    def set_open_price(self, open_price):
        self.open_price = open_price



############## EP Filters ##############

class EPStockFilter(ABC):

    @abstractmethod
    def check(self, stock_data: StockData) -> bool:
        pass

class VolumnFilter(EPStockFilter):

    def __init__(self, min_vol):
        self.min_vol = min_vol

    def check(self, stock_data: StockData) -> bool:
        return stock_data.cur_vol > self.min_vol

class PricePrevHighFilter(EPStockFilter):

    def check(self, stock_data: StockData) -> bool:
        return stock_data.cur_price > stock_data.prev_high 

class PriceChangeFilter(EPStockFilter):

    def __init__(self, min_change_percent):
        self.min_change = min_change_percent

    def check(self, stock_data: StockData) -> bool:
        return (stock_data.cur_price - stock_data.open_price) / stock_data.open_price > self.min_change

class PennyStockFilter(EPStockFilter):

    def __init__(self, min_price):
        self.min_price = min_price

    def check(self, stock_data: StockData) -> bool:
        return stock_data.cur_price > self.min_price

class PricePrevHighFilter(EPStockFilter):

    def check(self, stock_data: StockData) -> bool:
        return stock_data.cur_price > stock_data.prev_high 

class EPStockFilterEngine:

    def __init__(self, filters):
        self.filters = filters

    def evaludate(self, stock_data: StockData) -> bool:
        return all(f.check(stock_data) for f in self.filters)



############## Alpaca Stock Query Client ##############

class StockQueryClient:

    def __init__(self):
        self.tokens_path = "tokens.json"
        self.tickers_path = "tickers.json"
        self.__api_key, self.__secret_key = None, None
        self.alpaca_client = self._alpha_client_init()

    def _get_keys(self):
        with open(self.tokens_path, 'r') as file:
            tokens = json.load(file)

        self.__api_key = tokens["alpaca"]["key"]
        self.__secret_key = tokens["alpaca"]["secret"]

    def _alpha_client_init(self):
        
        if not self.__api_key or not self.__secret_key:
            self._get_keys()

        return StockHistoricalDataClient(api_key=self.__api_key, secret_key=self.__secret_key)

    def get_tradable_tickers(self, update=False):

        if update or not os.path.exists(self.tickers_path):

            if not self.__api_key or not self.__secret_key:
                self._get_keys()

            client = TradingClient(api_key=self.__api_key, secret_key=self.__secret_key)
            nasdaq_assets = client.get_all_assets(GetAssetsRequest(
                                        status=AssetStatus.ACTIVE,
                                        asset_class=AssetClass.US_EQUITY,
                                        exchange="NASDAQ"))
            nyse_assets = client.get_all_assets(GetAssetsRequest(
                                        status=AssetStatus.ACTIVE,
                                        asset_class=AssetClass.US_EQUITY,
                                        exchange="NYSE"))

            assets = nasdaq_assets + nyse_assets

            symbols = [a.symbol for a in assets]
            tradable_tickers = list(set(symbols))
            
            with open(self.tickers_path, 'w') as file:
                json.dump(tradable_tickers, file)

        with open(self.tickers_path, 'r') as file:
            tradable_tickers = json.load(file)

        return tradable_tickers

    def send_bar_query(self, symbols, timeframe, start, end, limit=None):

        if symbols is None or timeframe is None or start is None or end is None:
            print("Error: One or more parameters are None.")
            return None
        
        request_params = StockBarsRequest(
            symbol_or_symbols=symbols,
            timeframe=timeframe,
            start=start,
            end=end,
            limit=limit
        )

        bars = self.alpaca_client.get_stock_bars(request_params)
        
        return bars

    def send_snapshot_query(self, symbols):

        if symbols is None:
            print("Error: Symbols parameter is None.")
            return None
        
        request_params = StockSnapshotRequest(symbol_or_symbols=symbols)

        snapshots = self.alpaca_client.get_stock_snapshot(request_params)
        
        return snapshots

    def request_test(self, start, end, timeframe):
        request_params = StockBarsRequest(
            symbol_or_symbols=["AMZN", "MSFT", "CVX"],
            timeframe=timeframe,
            start=start,
            end=end
        )

        bars = self.alpaca_client.get_stock_bars(request_params)
        print(bars)

        snapshots = self.alpaca_client.get_stock_snapshot(StockSnapshotRequest(symbol_or_symbols=["AMZN", "MSFT", "CVX"]))
        print(snapshots)


############## Stock Scanner ##############

class StockScanner:

    def __init__(self):
        self.tickers = self.get_all_tickers()
        self.filter_engine = self.filter_engine_init()
        self.stocks = {}
        self.ep_stocks = {}
        self.stock_init_all()

    def get_all_tickers(self, stock_query_client=None):

        if stock_query_client is None:
            stock_query_client = StockQueryClient()

        return stock_query_client.get_tradable_tickers()

    def filter_engine_init(self):
        filters = [
            VolumnFilter(min_vol=1000000),
            PricePrevHighFilter(),
            PriceChangeFilter(min_change_percent=0.05),
            PennyStockFilter(min_price=5)
        ]
        return EPStockFilterEngine(filters)

    def stock_init_all(self, stock_query_client=None):

        for ticker in self.tickers:
            self.stocks[ticker] = StockData(ticker)         

    def update_prev_high_and_open_price_all(self, stock_query_client):

        if stock_query_client is None:
            print("StockQueryClient is not provided.")
            return

        snapshots = stock_query_client.send_snapshot_query(self.tickers)

        skipped_tickers = []
        for ticker, snapshot in snapshots.items():

            if ticker not in self.stocks:
                print(f"Ticker {ticker} not found in stock data.")
                continue
            stock_data = self.stocks[ticker]

            try:
                stock_data.open_price = snapshot.daily_bar.open
                stock_data.prev_high = snapshot.previous_daily_bar.high
            except:
                stock_data.open_price = None
                stock_data.prev_high = None
                skipped_tickers.append(ticker)

        print(f"Skipped tickers due to missing data: {skipped_tickers}")

        self.ep_stocks = {}

    def filter_latest_stock(self, stock_query_client, start, end, timeframe):

        if stock_query_client is None:
            print("StockQueryClient is not provided.")
            return

        self.cur_ep_stocks = {}
        bars = stock_query_client.send_bar_query(self.tickers, timeframe, start, end)
        for ticker, bar in bars.data.items():

            if ticker not in self.stocks:
                print(f"Ticker {ticker} not found in stock data.")
                continue

            if ticker in self.ep_stocks:
                continue

            stock_data = self.stocks[ticker]

            try:
                stock_data.cur_price = bar[0].close
                stock_data.cur_vol = bar[0].volume
            except:
                print(f"Warning: No data found for {ticker}. Setting current price and volume to None.")
                stock_data.cur_price = None
                stock_data.cur_vol = None
            
            if stock_data.cur_price is not None and stock_data.cur_vol is not None \
                and stock_data.prev_high is not None and stock_data.open_price is not None:
                    
                    if self.filter_engine.evaludate(stock_data):
                        print(f"Ticker {ticker} passed all filters.")
                        self.ep_stocks[ticker] = stock_data
                        self.cur_ep_stocks[ticker] = stock_data
