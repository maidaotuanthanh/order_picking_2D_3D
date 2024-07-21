class OrderLinesMapper:
    def __init__(self, df_orderlines, orders_number):
        self.df_orderlines = df_orderlines
        self.orders_number = orders_number

    def map_orders(self):
        '''Mapping orders with wave number'''
        self.df_orderlines.sort_values(by='DATE', ascending=True, inplace=True)
        # Unique order numbers list
        list_orders = self.df_orderlines.OrderNumber.unique()
        dict_map = dict(zip(list_orders, [i for i in range(1, len(list_orders) + 1)]))
        # Order ID mapping
        self.df_orderlines['OrderID'] = self.df_orderlines['OrderNumber'].map(dict_map)
        # Grouping Orders by Wave of orders_number
        self.df_orderlines['WaveID'] = (self.df_orderlines.OrderID % self.orders_number == 0).shift(1).fillna(
            0).cumsum()
        # Counting number of Waves
        waves_number = self.df_orderlines.WaveID.max() + 1
        return self.df_orderlines, waves_number
