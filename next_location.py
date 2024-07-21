from distance_picking import DistanceCalculator


class LocationSelector:
    def __init__(self, y_low, y_high):
        self.distance_calculator = DistanceCalculator(y_low, y_high)

    def next_location(self, start_loc, list_locs):
        """Find closest next location"""
        list_dist = [self.distance_calculator.distance_picking(start_loc, loc) for loc in list_locs]
        distance_next = min(list_dist)
        index_min = list_dist.index(distance_next)
        next_loc = list_locs[index_min]
        list_locs.remove(next_loc)
        return list_locs, start_loc, next_loc, distance_next