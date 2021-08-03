from .detect_strategy import Detect_Strategy
from myutils import *
from modules.test import t_test_statistic


__all__ =["Std_Correlation_Strategy"]

class Std_Correlation_Strategy(Detect_Strategy):
    def __init__(self, volume_std_min_interval = 4, price_std_max_interval = 4.0, price_date_max_correlation = 3, days_interval = 120 ): 
        super(Std_Correlation_Strategy, self).__init__()
        self.volume_std_min_interval = volume_std_min_interval
        self.price_std_max_interval = price_std_max_interval
        self.price_date_max_correlation = price_date_max_correlation
        self.days_interval = days_interval


    def eval(self,response):
        is_detected = False
        volume = get_volume(response, is_normalize = False)
        avg_price = get_avg_price(response, is_normalize = False)
        date = get_date(response)
        latest_date = date[0]
        earliest_date = date[-1]

        t_stats_volume = t_test_statistic(sample = volume[1:], example = volume[0])
        t_stats_avg_price = t_test_statistic(sample = avg_price[1:], example = avg_price[0])
        corr = "N/A"
        
        if t_stats_volume >  self.volume_std_min_interval and t_stats_avg_price< self.price_std_max_interval and t_stats_avg_price>- self.price_std_max_interval:
            corr = correlation_test(avg_price)
        
            if corr <  self.price_date_max_correlation:
                print("\n  +++++++++++++++")
                print("  Abnormal volume is detected at "+str(latest_date[0])[:10]+" since "+str(earliest_date[0])[:10])
                print("  t_stats_volume: "+str(t_stats_volume[0]))
                print("  t_stats_avg_price: "+str(t_stats_avg_price[0]))
                print("  price date correlation: " + str(corr) )
                print("  +++++++++++++++\n")
                is_detected = True
            corr = str(round(corr,3))  
        return {
                "filter_name": "double_std_correlation_strategy",
                "detected":is_detected, 
                "begin_date":str(earliest_date[0])[:10],
                "end_date":str(latest_date[0])[:10], 
                "details":{
                    "t_stats_volume":str(round(t_stats_volume[0],3)), 
                    "t_stats_avg_price":str(round(t_stats_avg_price[0],3)), 
                    "price_date_correlation":corr
                    },
                "configs":{
                    "volume_std_min_interval":str( self.volume_std_min_interval),
                    "price_std_max_interval":str( self.price_std_max_interval),
                    "price_date_max_correlation":str(self.price_date_max_correlation),
                    "days_interval": str(self.days_interval)
                    },
                }
