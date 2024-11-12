# import pandas as pd
# from ast import literal_eval
# import itertools
# from simulation_wave import Simulation
# import matplotlib.pyplot as plt
#
# def assign_robot(wave_id):
#     # Calculate robot number based on wave id
#     robot_number = wave_id % 10 + 1
#     return 'R' + str(robot_number)
#
#
#
# def simulate_batch(y_low, y_high, origin_loc, orderlines):
#     # Lists for results
#     list_wid, list_dst, list_route, list_ord = [], [], [], []
#     # Lists for plotting
#     orders_numbers = []
#     distances = []
#     # Test several values of orders per wave
#     for orders_number in range(1, 10):
#         simulation = Simulation(y_low, y_high, origin_loc, orders_number, orderlines)
#         list_wid, list_dst, list_route, list_ord, distance_route = simulation.simulation_wave(list_wid, list_dst,
#                                                                                           list_route, list_ord)
#         print("Total distance for {} orders/wave: {:,} m".format(orders_number, distance_route))
#         # Append to lists for plotting
#         orders_numbers.append(orders_number)
#         distances.append(distance_route)
#
#     # By Wave
#     df_waves = pd.DataFrame({'wave': list_wid,
#                              'distance': list_dst,
#                              'routes': list_route,
#                              'order_per_wave': list_ord})
#
#     # Add 'robot' column
#     df_waves['robot'] = df_waves['wave'].apply(assign_robot)
#
#     # Plotting
#     plt.bar(orders_numbers, distances)
#     plt.xlabel('Number of Orders per Wave')
#     plt.ylabel('Total Distance')
#     plt.title('Total Distance for Different Numbers of Orders per Wave')
#     plt.tight_layout()  # Adjust the layout to make sure everything fits
#     plt.show()
#
#     return df_waves
#
#
# def main():
#     # Example setup, replace with actual data and parameters
#     y_low, y_high = 0, 25
#     origin_loc = (0, 0)
#     orders_number = 9
#     # Example DataFrame, replace with actual data
#     orderlines = pd.read_csv('input/df_lines.csv')
#
#     df_waves = simulate_batch(y_low, y_high, origin_loc, orderlines)
#     # print(df_waves)
#     df_waves.to_csv('output/output_OSACO.csv', index=False)
#
#
# if __name__ == "__main__":
#     main()
import pandas as pd
from simulation_wave import Simulation
import matplotlib.pyplot as plt

def assign_robot(wave_id):
    # Calculate robot number based on wave id
    robot_number = wave_id % 10 + 1
    return 'R' + str(robot_number)

def simulate_batch(y_low, y_high, origin_loc, orderlines):
    # Lists for results
    list_wid, list_dst, list_route, list_ord = [], [], [], []
    # Lists for plotting
    orders_numbers = []
    distances = []
    # Test several values of orders per wave
    for orders_number in range(1, 10):
        simulation = Simulation(y_low, y_high, origin_loc, orders_number, orderlines)
        list_wid, list_dst, list_route, list_ord, distance_route = simulation.simulation_wave(list_wid, list_dst,
                                                                                              list_route, list_ord)
        print("Total distance for {} orders/wave: {:,} m".format(orders_number, distance_route))
        # Append to lists for plotting
        orders_numbers.append(orders_number)
        distances.append(distance_route)

    # By Wave
    df_waves = pd.DataFrame({'wave': list_wid,
                             'distance': list_dst,
                             'routes': list_route,
                             'order_per_wave': list_ord})

    # Add 'robot' column
    df_waves['robot'] = df_waves['wave'].apply(assign_robot)

    # Plotting
    plt.bar(orders_numbers, distances)
    plt.xlabel('Number of Orders per Wave')
    plt.ylabel('Total Distance')
    plt.title('Total Distance for Different Numbers of Orders per Wave')
    plt.tight_layout()  # Adjust the layout to make sure everything fits
    plt.show()

    return df_waves

def main():
    # Example setup, replace with actual data and parameters
    y_low, y_high = 0, 25
    origin_loc = (0, 0)  # Ensure this is correctly formatted as a tuple
    orders_number = 9
    # Example DataFrame, replace with actual data
    orderlines = pd.read_csv('input/df_lines.csv')

    df_waves = simulate_batch(y_low, y_high, origin_loc, orderlines)
    # print(df_waves)
    df_waves.to_csv('output/output_OSACO.csv', index=False)

if __name__ == "__main__":
    main()
