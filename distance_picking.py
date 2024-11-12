# class DistanceCalculator:
#     def __init__(self, y_low, y_high):
#         self.y_low = y_low
#         self.y_high = y_high
#
#     def distance_picking(self, Loc1, Loc2):
#         # Start Point
#         z1 = Loc1[2] if len(Loc1) > 2 else 0
#         z2 = Loc2[2] if len(Loc2) > 2 else 0
#
#         x1, y1 = Loc1[0], Loc1[1]
#         # End Point
#         x2, y2 = Loc2[0], Loc2[1]
#         # Distance x-axis
#         distance_x = abs(x2 - x1)
#         # Distance z-axis
#         distance_z = abs(z2 - z1)
#         # Distance y-axis
#         if x1 == x2:
#             distance_y1 = abs(y2 - y1)
#             distance_y2 = distance_y1
#         else:
#             distance_y1 = (self.y_high - y1) + (self.y_high - y2)
#             distance_y2 = (y1 - self.y_low) + (y2 - self.y_low)
#         # Minimum distance on y-axis
#         distance_y = min(distance_y1, distance_y2)
#         # Total distance
#         distance = distance_x + distance_y + distance_z
#         return int(distance)

class DistanceCalculator:
    def __init__(self, y_low, y_high):
        self.y_low = y_low
        self.y_high = y_high

    def distance_picking(self, Loc1, Loc2):
        # Ensure both Loc1 and Loc2 are lists or tuples
        if not isinstance(Loc1, (list, tuple)) or not isinstance(Loc2, (list, tuple)):
            raise ValueError("Loc1 and Loc2 must be lists or tuples with at least two elements")

        # Start Point
        z1 = Loc1[2] if len(Loc1) > 2 else 0
        z2 = Loc2[2] if len(Loc2) > 2 else 0

        x1, y1 = Loc1[0], Loc1[1]
        # End Point
        x2, y2 = Loc2[0], Loc2[1]
        # Distance x-axis
        distance_x = abs(x2 - x1)
        # Distance z-axis
        distance_z = abs(z2 - z1)
        # Distance y-axis
        if x1 == x2:
            distance_y1 = abs(y2 - y1)
            distance_y2 = distance_y1
        else:
            distance_y1 = (self.y_high - y1) + (self.y_high - y2)
            distance_y2 = (y1 - self.y_low) + (y2 - self.y_low)
        # Minimum distance on y-axis
        distance_y = min(distance_y1, distance_y2)
        # Total distance
        distance = distance_x + distance_y + distance_z
        return int(distance)
