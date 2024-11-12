class OrderLinesMapper:
    def __init__(self, orderlines, orders_number):
        self.orderlines = orderlines
        self.orders_number = orders_number

    def map_orders(self):
        self.orderlines.sort_values(by='DATE', ascending=True, inplace=True)
        # Unique order numbers list
        list_orders = self.orderlines.OrderNumber.unique()
        dict_map = dict(zip(list_orders, [i for i in range(1, len(list_orders) + 1)]))
        # Order ID mapping
        self.orderlines['OrderID'] = self.orderlines['OrderNumber'].map(dict_map)
        # Grouping Orders by Wave of orders_number
        self.orderlines['WaveID'] = (self.orderlines.OrderID % self.orders_number == 0).shift(1).fillna(
            0).cumsum()
        # Counting number of Waves
        waves_number = self.orderlines.WaveID.max() + 1
        # print(self.orderlines)
        return self.orderlines, waves_number
