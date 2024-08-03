# region imports
from AlgorithmImports import *
# endregion

class Demo(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2019, 1, 1)
        self.set_end_date(2021, 1, 1)
        self.set_cash(5000)
        self.universe_settings.resolution = Resolution.DAILY
        self.add_universe(self.selection_filter)
        self.universe_settings.leverage = 2
        self.set_security_initializer(lambda x: x.set_fee_model(ConstantFeeModel(0)))

    def selection_filter(self, coarse):
        sorted_vol = sorted(coarse, key = lambda x : x.dollar_volume, reverse = True)
        filtered = [x.symbol for x in sorted_vol if x.price > 50]
        return filtered[:10]
    
    def on_securities_changed(self, changes):
        self.changes = changes
        self.log(f"on_securities_changed({self.time}):{changes}")

        for security in changes.removed_securities:
            if security.invested:
                self.liquidate(security.symbol)

        
        for security in changes.added_securities:
            if not security.invested:
                self.set_holdings(security.symbol, 0.15)
