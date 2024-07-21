from distance_picking import DistanceCalculator
from next_location import LocationSelector


class RouteCalculator:
    def __init__(self, y_low, y_high):
        self.location_selector = LocationSelector(y_low, y_high)
        self.distance_calculator = DistanceCalculator(y_low, y_high)

    def calculate_total_distance(self, route):
        total_distance = 0
        for i in range(len(route) - 1):
            total_distance += self.distance_calculator.distance_picking(route[i], route[i + 1])
        return total_distance

    def two_opt(self, route):
        best_route = route.copy()
        improved = True
        while improved:
            improved = False
            for i in range(1, len(route) - 2):
                for j in range(i + 1, len(route)):
                    if j - i == 1:
                        continue
                    new_route = route[:]
                    new_route[i:j] = route[j - 1:i - 1:-1]  # this is the 2-optSwap
                    if self.calculate_total_distance(new_route) < self.calculate_total_distance(best_route):
                        best_route = new_route
                        improved = True
            route = best_route
        return best_route

    def nearest_neighbor(self, origin_loc, list_locs):
        route = [origin_loc]
        current_loc = origin_loc
        while list_locs:
            list_locs, current_loc, next_loc, _ = self.location_selector.next_location(current_loc, list_locs)
            route.append(next_loc)
        return route

    def create_picking_route(self, origin_loc, list_locs):
        initial_route = self.nearest_neighbor(origin_loc, list_locs)
        initial_route.append(origin_loc)
        optimized_route = self.two_opt(initial_route)
        total_distance = self.calculate_total_distance(optimized_route)

        return total_distance, optimized_route
