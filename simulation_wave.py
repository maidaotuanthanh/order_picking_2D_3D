# from orderlines_mapping import OrderLinesMapper
# from locations_listing import LocationLister
# from create_picking_route_OSACO import RouteCalculator
#
#
# class Simulation:
#     def __init__(self, y_low, y_high, origin_loc, orders_number, orderlines):
#         self.y_low = y_low
#         self.y_high = y_high
#         self.origin_loc = origin_loc
#         self.orders_number = orders_number
#         self.orderlines = orderlines
#         self.mapper = OrderLinesMapper(orderlines, orders_number)
#         self.route_calculator = RouteCalculator(y_low, y_high)
#
#     def simulation_wave(self, list_wid, list_dst, list_route, list_ord):
#         """ Simulate total picking distance with n orders per wave"""
#         distance_route = 0
#         self.orderlines, waves_number = self.mapper.map_orders()
#
#         for wave_id in range(waves_number):
#             lister = LocationLister(self.orderlines)
#             list_locs, n_locs = lister.get_locations_for_wave(wave_id)
#
#             wave_distance, list_chemin = self.route_calculator.create_picking_route(self.origin_loc, list_locs)
#             distance_route += wave_distance
#             list_wid.append(wave_id)
#             list_dst.append(wave_distance)
#             list_route.append(list_chemin)
#             list_ord.append(self.orders_number)
#
#         return list_wid, list_dst, list_route, list_ord, distance_route
from orderlines_mapping import OrderLinesMapper
from locations_listing import LocationLister
from create_picking_route_OSACO import RouteCalculator


class Simulation:
    def __init__(self, y_low, y_high, origin_loc, orders_number, orderlines):
        self.y_low = y_low
        self.y_high = y_high
        self.origin_loc = origin_loc
        self.orders_number = orders_number
        self.orderlines = orderlines
        self.mapper = OrderLinesMapper(orderlines, orders_number)
        self.route_calculator = RouteCalculator(y_low, y_high)

    def simulation_wave(self, list_wid, list_dst, list_route, list_ord):
        """ Simulate total picking distance with n orders per wave"""
        distance_route = 0
        self.orderlines, waves_number = self.mapper.map_orders()

        for wave_id in range(waves_number):
            lister = LocationLister(self.orderlines)
            list_locs, n_locs = lister.get_locations_for_wave(wave_id)

            # Ensure that list_locs is a list of tuples/lists (coordinates)
            wave_distance, list_chemin = self.route_calculator.create_picking_route(self.origin_loc, list_locs)
            distance_route += wave_distance
            list_wid.append(wave_id)
            list_dst.append(wave_distance)
            list_route.append(list_chemin)
            list_ord.append(self.orders_number)

        return list_wid, list_dst, list_route, list_ord, distance_route
