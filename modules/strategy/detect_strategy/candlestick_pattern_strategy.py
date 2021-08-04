from .detect_strategy import Detect_Strategy
from .utils import *
from myutils import *


__all__ = ["Candlestick_Pattern_Strategy"]


class Candlestick_Pattern_Strategy(Detect_Strategy):
    def __init__(self, days_interval=120):
        super().__init__()
        self.days_interval = days_interval

    def eval(self, response):
        is_detected = False
        response.index = response.time
        date = get_date(response)
        latest_date = date[0]
        earliest_date = date[-1]

        pattern, y = find_pattern(response, 'sym')
        if pattern == None:
            return
        else:
            is_detected = True

        (x1, y1), (x2, y2) = pattern['line1']
        (x3, y3), (x4, y4) = pattern['line2']
        x1 = str(x1)[:10]
        x2 = str(x2)[:10]
        x3 = str(x3)[:10]
        x4 = str(x4)[:10]

        print("\n  +++++++++++++++")
        print("  Candlestick Pattern is detected at " +
              str(latest_date[0])[:10]+" since "+str(earliest_date[0])[:10])
        print("  (x1,y1),(x2,y2): "+str((x1, y1))+str((x2, y2)))
        print("  (x3,y3),(x4,y4): "+str((x3, y3))+str((x4, y4)))
        print("  +++++++++++++++\n")

        return {
            "filter_name": "candlestick_pattern_strategy",
            "detected": is_detected,
            "begin_date": str(earliest_date[0])[:10],
            "end_date": str(latest_date[0])[:10],
            "details": {
                "(x1,y1),(x2,y2)": str((x1, y1))+str((x2, y2)),
                "(x3,y3),(x4,y4)": str((x3, y3))+str((x4, y4)),
            },
            "configs": {
                "days_interval": str(self.days_interval)
            },
        }
