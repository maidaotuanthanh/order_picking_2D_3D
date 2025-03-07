import pandas as pd
from ast import literal_eval
import itertools


class LocationLister:
    def __init__(self, orderlines):
        self.orderlines = orderlines

    def get_locations_for_wave(self, wave_id):
        '''Getting storage locations to cover for a wave of orders'''
        df = self.orderlines[self.orderlines.WaveID == wave_id]
        # Create coordinates listing
        list_locs = list(df['Coord'].apply(lambda t: literal_eval(t)).values)
        list_locs.sort()
        # List of unique coordinates
        list_locs = list(k for k, _ in itertools.groupby(list_locs))
        n_locs = len(list_locs)
        return list_locs, n_locs
