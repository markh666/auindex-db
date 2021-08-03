from datetime import datetime
from pytz import timezone
import pandas as pd

from mydatabase.filter_center import Filter_center
from myutils import *
import modules.strategy.detect_strategy as detect_strategy


class StockFilter:
    def __init__(self, detectstrategy, access_auindex):
        self.detectstrategy = detect_strategy.__dict__[detectstrategy]()
        self.access_auindex = access_auindex

        self.filter_center = Filter_center()


    def _detect_abnormal_volume(self, response):
        return self.detectstrategy.eval(response=response)


    def detect_abnormal_volume(self, days_interval=120):
        print("Starting detect_abnormal_volume()")
        watchlist = pd.DataFrame(
            self.access_auindex.request_new_watchlist()).T.symbol.to_list()
        current_syd_time = datetime.now(tz=timezone('Australia/Sydney'))
        detect_start_date = np.datetime64(current_syd_time-pd.Timedelta(days=days_interval))
        input_start_from = str(detect_start_date)[:10]

        for symbol in watchlist:
            response = self.access_auindex.request_prices(symbol=symbol.lower(), date_from=input_start_from)
            if response is None:
                print(f"######################## Please check {symbol} ########################")
                continue

            price = pd.DataFrame(response).T
            price.time = price.time.astype(dtype='datetime64[ms]')
            price = price[price.volume != 0]

            # skip symbol with empty data or SUSPENDED stocks which has less than detect_days/10 days ohlc
            if (price.shape[0] <= 15) or ((price.time[0]-price.time[1]).days > 100):
                print(f"######################## Please check {symbol} ########################")
                continue
            
            str_latest_time = str(current_syd_time)[:10]
            if (price.time[0].year != current_syd_time.year) or (price.time[0].month != current_syd_time.month) or (price.time[0].day != current_syd_time.day):
                str_latest_time = str(price.time[0])[:10]

            print("====>Detecting "+symbol+" from "+input_start_from+" to "+str_latest_time)
            record = self._detect_abnormal_volume(response=price)
            self.filter_center.add_new_filter_record(symbol=symbol, record=record)


    def _detect_candlestick_pattern(self, response):
        return self.detectstrategy.eval(response=response)


    def detect_candlestick_pattern(self, days_interval=120):
        print("Starting detect_candlestick_pattern()")
        watchlist = pd.DataFrame(
            self.access_auindex.request_new_watchlist()).T.symbol.to_list()
        current_syd_time = datetime.now(tz=timezone('Australia/Sydney'))
        detect_start_date = np.datetime64(current_syd_time-pd.Timedelta(days=days_interval))
        input_start_from = str(detect_start_date)[:10]

        for symbol in watchlist:
            response = self.access_auindex.request_prices(
                symbol=symbol.lower(), date_from=input_start_from)
            if response is None:
                print(f"######################## Please check {symbol} ########################")
                continue

            price = pd.DataFrame(response).T
            price.time = price.time.astype(dtype='datetime64[ms]')
            price = price[price.volume != 0]

            # skip symbol with empty data or SUSPENDED stocks which has less than detect_days/10 days ohlc
            if (price.shape[0] <= 15) or ((price.time[0]-price.time[1]).days > 100):
                print(f"######################## Please check {symbol} ########################")
                continue
            
            str_latest_time = str(current_syd_time)[:10]
            if (price.time[0].year != current_syd_time.year) or (price.time[0].month != current_syd_time.month) or (price.time[0].day != current_syd_time.day):
                str_latest_time = str(price.time[0])[:10]

            print("====>Detecting "+symbol+" from "+input_start_from+" to "+str_latest_time)
            record = self._detect_candlestick_pattern(response=price)
            if record != None:
                self.filter_center.add_new_filter_record(symbol=symbol, record=record)

if __name__ == "__main__":
    from access_auindex import Access_auindex
    from mydatabase.database import Database
    access_auindex = Access_auindex()
    db = Database()
    db.init_tables()

    stockfilter = StockFilter(
        detectstrategy="Candlestick_Pattern_Strategy", access_auindex=access_auindex)
    stockfilter.detect_candlestick_pattern()
