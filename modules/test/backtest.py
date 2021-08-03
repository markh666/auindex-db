
# class Backtest:
#     ### TODO create backtest_strategy, detect_strategy classes which contain configs
#     def __init__(self, backtest_strategy, detect_strategy, bstconfigs, stconfigs, db):

#         self.backtest_strategy = Sample_FS(**stconfigs)
#         self.detect_strategy = Sample_BS(detect_strategy=detect_strategy,**bstconfigs )
#         self.db = db 

#     def run(self):
#         results = self.backtest_strategy.eval(self.detect_strategy)
#         self._save_results(results)

#     def _save_results(self,results):
#         pass