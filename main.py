import pandas as pd
from ast import literal_eval
import itertools
from simulation_wave import Simulation


def simulate_batch(n1, n2, y_low, y_high, origin_loc, df_orderlines):
    ''' Loop with several scenarios of n orders per wave'''
    # Lists for results
    list_wid, list_dst, list_route, list_ord = [], [], [], []
    # Test several values of orders per wave
    for orders_number in range(1, 10):
        # orders_number = 1
        simulation = Simulation(y_low, y_high, origin_loc, orders_number, df_orderlines)
        list_wid, list_dst, list_route, list_ord, distance_route = simulation.simulation_wave(list_wid, list_dst,
                                                                                              list_route, list_ord)
        print("Total distance covered for {} orders/wave: {:,} m".format(orders_number, distance_route))

    # By Wave
    df_waves = pd.DataFrame({'wave': list_wid,
                             'distance': list_dst,
                             'routes': list_route,
                             'order_per_wave': list_ord})

    return df_waves


def main():
    # Example setup, replace with actual data and parameters
    y_low, y_high = 0, 25
    origin_loc = (0, 0)
    orders_number = 9
    n1, n2 = 1, 5  # Range of orders per wave to test
    # Example DataFrame, replace with actual data
    df_orderlines = pd.read_csv('input/df_lines.csv')

    df_waves = simulate_batch(n1, n2, y_low, y_high, origin_loc, df_orderlines)
    # print(df_waves)
    df_waves.to_csv('output.csv', index=False)


if __name__ == "__main__":
    main()
