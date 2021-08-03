import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import inspect
from pytz import timezone
from time import sleep

from mydatabase.watchlist_center import Wathlist_center
from mydatabase.price_center import Price_center


class Price_updater(Price_center):
    def __init__(self) -> None:
        super().__init__()
    

    def _check_any_tables_exist(self, check_list):
        engine = self.create_sqlalchemy_engine()

        for symbol in check_list:
            if not inspect(engine).has_table(symbol.lower()):
                return False
        return True
    

    def _fetch_latest_prices(self, single_part_watchlist, all_price_tables_exist, interval="1d", period="max"):
        codes = " ".join(single_part_watchlist)
        codes = codes.replace("_ASX", ".AX")

        # if all price tables are not existed, downloading data as long as possible
        if not all_price_tables_exist:
            prices = yf.download(tickers=codes, period=period, interval=interval)
        # if all price tables are existed, downloading less data only for daily update
        else:
            prices = yf.download(tickers=codes, period="7d", interval=interval)

        if prices.shape[0] == 0:
            return pd.DataFrame([])
            
        return prices


    def _clean_price(self, price, interval="1d"):
        price = price.dropna(axis=0, how='all')
        price = price.fillna(0)
        if price.shape[0] == 0:
            return pd.DataFrame([])

        price = price.apply(lambda x: round(x, 4))
        price = price[["Open", "High", "Low", "Close", "Adj Close", "Volume"]]
        price = price.rename(columns={"Open":"open","High":"high","Low": "low","Close": "close","Adj Close":"adj_close","Volume":"volume"})
        price.insert(0, "time", price.index) 
        price = price.reset_index(drop=True)

        # remove timezone +10/+11 of Australia stocks for hourly price
        if interval != "1d":
            price.time = price.time.dt.tz_localize(None)

        # need to remove last day price because they may include non-closed data
        # if updating price during market open hour
        current_syd_time = datetime.now(tz=timezone('Australia/Sydney'))
        if (current_syd_time.hour>=10) and (current_syd_time.hour<=16):
            # last_timestamp = price.time.iloc[-1]
            # last_day = datetime(last_timestamp.year, last_timestamp.month, last_timestamp.day)
            today_day = datetime(current_syd_time.year, current_syd_time.month, current_syd_time.day)
            price = price[price.time < today_day]
        
        # for daily price, only keep the date part
        if interval == "1d":
            price.time = price.time.dt.date
        return price


    def fetch_latest_prices(self):
        print("Starting fetch_latest_prices()")
        watchlist = Wathlist_center().select_watchlist()
        all_parts_watchlist = np.array_split(watchlist, 100)
        
        for single_part_watchlist in all_parts_watchlist:
            all_price_tables_exist = self._check_any_tables_exist(single_part_watchlist)
            prices = self._fetch_latest_prices(single_part_watchlist, all_price_tables_exist)

            for symbol in single_part_watchlist:
                print("fetch_latest_prices:", symbol)
                code = symbol.replace("_ASX", ".AX")
                price = prices.loc[:, (["Open", "High", "Low", "Close", "Adj Close", "Volume"], code)]

                # skip if the dataframe contains NaN only
                if pd.isna(price).eq(True).all().all():
                    continue

                cleaned_price = self._clean_price(price)
                cleaned_price.columns = cleaned_price.columns.droplevel(1)

                # skip if the dataframe does not have any row
                if cleaned_price.shape[0] == 0:
                    continue

                failed_insert = self.insert_price(symbol, cleaned_price, all_price_tables_exist)
                sleep(1)

                # if current symbol failed to insert due to mysql.connector.errors.IntegrityError
                # TRUNCATE first, then download max period and insert again
                if failed_insert:
                    query = f"TRUNCATE datacenter.{symbol.lower()};"
                    self.insert_query(query)

                    single_price = self._fetch_latest_prices([symbol], all_price_tables_exist=False)
                    cleaned_single_price = self._clean_price(single_price)
                    
                    self.insert_price(symbol, cleaned_single_price, all_price_tables_exist=False)
                    sleep(0.5)
