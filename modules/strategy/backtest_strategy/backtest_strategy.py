from modules.strategy.strategy import Strategy

__all__ =["Backtest_Strategy"]


class Backtest_Strategy(Strategy):
    def __init__(self, detect_strategy, symbol_list): 
        super(Backtest_Strategy, self).__init__()
        self.detect_strategy = detect_strategy
        self.symbol_list = symbol_list


