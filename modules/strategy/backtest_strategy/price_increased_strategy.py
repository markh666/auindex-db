from .backtest_strategy import Backtest_Strategy
from myutils import *
from modules.test import t_test_statistic


class Price_Increased_Strategy(Backtest_Strategy):
    def __init__(self, detect_strategy, db=None, symbol_list=None, days_interval=120, hold_priod=200, date_from="2019-02-05", date_to="2021-02-10", increased_threshold=2.0):
        self.db = db
        if symbol_list == None:
            symbol_list = self.db.get_watchlist()
        super(Price_Increased_Strategy, self).__init__(
            detect_strategy=detect_strategy, symbol_list=symbol_list)
        self.days_interval = days_interval
        self.hold_priod = hold_priod
        self.date_from = date_from
        self.date_to = date_to
        self.increased_threshold = increased_threshold

    def _get_idx_of_date(self, dates, curr_date):
        for i in range(len(dates)):
            date = date_str_to_datetime(dates[i][0], include="ymd")
            if date <= curr_date:
                return i
        return len(dates)-1

    def price_explosed(self, buy_in_price, prices):
        for price in prices:
            if price[0]/buy_in_price >= self.increased_threshold:
                print("buy in price "+str(buy_in_price))
                print("explosed price "+str(price[0]))
                return True
        return False

    def eval(self):
        repeats = 0
        success = 0
        for symbol in self.symbol_list:
            print("====> back testing "+symbol[0])
            response = self.db.get_end_of_day_data(
                symbol=symbol[0], date_from=self.date_from, date_to=self.date_to)
            if (response.empty):
                print("no price")
                continue
            date = get_date(response=response)
            avg_price = get_avg_price(response, is_normalize=False)

            print("====> back testing from "+date[-1][0]+" to "+date[0][0])
            for i in range(0, len(response)):
                end_date = date_str_to_datetime(date[i][0], include="ymd")
                start_date = add_days(end_date, -self.days_interval)

                ### the date list is in the reverse order
                # print(response)

                start_idx = self._get_idx_of_date(date, end_date)
                end_idx = self._get_idx_of_date(date, start_date)

                if(end_idx-start_idx <= 15):
                    continue
                record = self.detect_strategy.eval(
                    response=response[start_idx:end_idx])
                if record["detected"]:
                    repeats += 1
                    end_idx = self._get_idx_of_date(date, end_date)
                    start_date = add_days(end_date, self.hold_priod)
                    start_idx = self._get_idx_of_date(date, start_date)
                    if(end_idx-start_idx <= 30):
                        continue
                    curr_price = avg_price[start_idx: end_idx]

                    if self.price_explosed(curr_price[0], curr_price):
                        success += 1

        return success/repeats

        #self.db.add_filter_record(symbol_id=symbol[0], record=record)


# detect_strategy = Sample_BS(detect_strategy=detect_strategy,**bstconfigs )
