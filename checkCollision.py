# import numpy as np
# import pandas as pd
# import ast
#
# # Load the data
# file_path = 'input/output_collision.csv'
# data = pd.read_csv(file_path)
#
# # Convert the routes from string representation to list of tuples
# data['routes'] = data['routes'].apply(ast.literal_eval)
#
# # Extract all unique robot IDs
# robots = data['robot'].unique()
#
# # Create a dictionary to store the time slices for each robot
# time_slices = {robot: [] for robot in robots}
#
#
# # Calculate the Euclidean distance between two points
# def calculate_distance(point1, point2):
#     return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
#
#
# # Fill the time slices with the positions at each time step
# for robot in robots:
#     robot_data = data[data['robot'] == robot]
#     time = 0
#     for idx, row in robot_data.iterrows():
#         route = row['routes']
#         # Start at (0,0)
#         if time == 0 or time_slices[robot][-1][1] != (0, 0):
#             time_slices[robot].append((time, (0, 0)))
#         for i in range(len(route)):
#             if i > 0:
#                 time += calculate_distance(route[i - 1], route[i])
#             time_slices[robot].append((time, route[i]))
#         # Return to (0, 0) after completing the route
#         time += calculate_distance(route[-1], (0, 0))
#         time_slices[robot].append((time, (0, 0)))
#
#     # Ensure the final position is (0, 0)
#     if time_slices[robot][-1][1] != (0, 0):
#         time += calculate_distance(time_slices[robot][-1][1], (0, 0))
#         time_slices[robot].append((time, (0, 0)))
#
# # Create a list of all unique time steps
# all_time_steps = sorted(set([time_step for slices in time_slices.values() for time_step, _ in slices]))
#
# # Create a DataFrame to store the positions at each time step for each robot
# time_df = pd.DataFrame(index=robots, columns=all_time_steps)
#
# # Fill the DataFrame with positions
# for robot, slices in time_slices.items():
#     for time_step, position in slices:
#         time_df.loc[robot, time_step] = str(position)
#
#
# # Unify the coordinate format to use tuples
# def unify_coordinates_format(position):
#     if pd.notna(position):
#         position = position.replace('[', '(').replace(']', ')')
#     return position
#
#
# # Apply the coordinate format unification
# time_df = time_df.applymap(unify_coordinates_format)
#
# # Transpose the DataFrame to switch rows and columns
# time_df_transposed = time_df.transpose()
#
# # Filter out columns with NaN values only
# time_df_transposed = time_df_transposed.dropna(how='all', axis=1)
#
# # Ensure the final row for each robot is (0, 0)
# for robot in robots:
#     last_position = time_df_transposed[robot].dropna().iloc[-1]
#     if last_position != '(0, 0)':
#         time_df_transposed.loc[max(time_df_transposed.index) + 1, robot] = '(0, 0)'
#
# # Save the final DataFrame to a new CSV file
# output_file_path = 'output/robot_time_slices_final_corrected.csv'
# time_df_transposed.to_csv(output_file_path)
#
# print(f'Output saved to: {output_file_path}')
#
# import numpy as np
# import pandas as pd
# import ast
#
# # Load the initial data
# input_file_path = 'input/input_OSACO.csv'
# data = pd.read_csv(input_file_path)
#
# # Convert the routes from string representation to list of tuples
# data['routes'] = data['routes'].apply(ast.literal_eval)
#
# # Extract all unique robot IDs
# robots = data['robot'].unique()
#
# # Create a dictionary to store the time slices for each robot
# time_slices = {robot: [] for robot in robots}
#
# # Calculate the Euclidean distance between two points
# def calculate_distance(point1, point2):
#     return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
#
# # Create a DataFrame to store the positions at each time step for each robot
# time_df = pd.DataFrame()
#
# # Fill the time slices with the positions at each time step
# for robot in robots:
#     robot_data = data[data['robot'] == robot]
#     time = 0
#     for idx, row in robot_data.iterrows():
#         route = row['routes']
#         # Start at (0,0)
#         if time == 0 or time_slices[robot][-1][1] != (0, 0):
#             time_slices[robot].append((time, (0, 0)))
#             time_df.loc[time, robot] = str((0, 0))
#         for i in range(len(route)):
#             if i > 0:
#                 time += calculate_distance(route[i - 1], route[i])
#             while time in time_df.index and any(time_df.loc[time] == str(route[i])):
#                 time += 0.1  # Increment time slightly if the position is occupied
#             time_slices[robot].append((time, route[i]))
#             time_df.loc[time, robot] = str(route[i])
#         # Return to (0, 0) after completing the route
#         time += calculate_distance(route[-1], (0, 0))
#         while time in time_df.index and any(time_df.loc[time] == str((0, 0))):
#             time += 0.1  # Increment time slightly if the position is occupied
#         time_slices[robot].append((time, (0, 0)))
#         time_df.loc[time, robot] = str((0, 0))
#
# # Remove redundant (0, 0) positions
# for robot in robots:
#     positions = time_df[robot].dropna()
#     for idx in range(len(positions) - 1, 0, -1):
#         if positions.iloc[idx] == '(0, 0)' and positions.iloc[idx - 1] == '(0, 0)':
#             time_df.loc[positions.index[idx], robot] = None
#
# # Sort the DataFrame by time index
# time_df = time_df.sort_index()
#
# # Save the final DataFrame to a new CSV file
# output_file_path = 'output/robot_time_slices_final_corrected_ACO.csv'
# time_df.to_csv(output_file_path)
#
# print(f"Output saved to: {output_file_path}")
#
# import numpy as np
# import pandas as pd
# import ast
#
# # Load the initial data
# input_file_path = 'input/input_OSACO.csv'
# data = pd.read_csv(input_file_path)
#
# # Convert the routes from string representation to list of tuples
# data['routes'] = data['routes'].apply(ast.literal_eval)
#
# # Extract all unique robot IDs
# robots = data['robot'].unique()
#
# # Create a DataFrame to store the positions at each time step for each robot
# time_df = pd.DataFrame()
#
#
# # Calculate the Euclidean distance between two points
# def calculate_distance(point1, point2):
#     return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
#
#
# # Fill the time slices with the positions at each time step
# for robot in robots:
#     robot_data = data[data['robot'] == robot]
#     time = 0  # Start time for each robot
#     for idx, row in robot_data.iterrows():
#         route = row['routes']
#
#         # Start at (0, 0) for each new segment
#         time_df.loc[time, robot] = str((0, 0))
#
#         # Traverse each point in the route, calculating travel time based on distance
#         previous_position = (0, 0)  # Starting point
#         for position in route:
#             travel_time = calculate_distance(previous_position, position)  # Calculate travel time based on distance
#             time += travel_time  # Increment time by travel time
#             time_df.loc[time, robot] = str(position)
#             previous_position = position  # Update the previous position
#
#         # Return to (0, 0) after completing the route
#         travel_time = calculate_distance(previous_position, (0, 0))
#         time += travel_time  # Increment time to return to start
#         time_df.loc[time, robot] = str((0, 0))
#
# # Sort the DataFrame by time index to ensure correct ordering
# time_df = time_df.sort_index()
#
# # Save the final DataFrame to a new CSV file
# output_file_path = 'output/robot_time_slices_with_travel_time.csv'
# time_df.to_csv(output_file_path)
#
# print(f"Output saved to: {output_file_path}")
import numpy as np
import pandas as pd
import ast

# Load the initial data
input_file_path = 'input/input_OSACO.csv'
data = pd.read_csv(input_file_path)

# Convert the routes from string representation to list of tuples
data['routes'] = data['routes'].apply(ast.literal_eval)

# Extract all unique robot IDs
robots = data['robot'].unique()

# Create a DataFrame to store the positions at each time step for each robot
time_df = pd.DataFrame()

# Calculate the Euclidean distance between two points
def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Counter for duplicate coordinates
duplicate_count = 0

# Fill the time slices with the positions at each time step
for robot in robots:
    robot_data = data[data['robot'] == robot]
    time = 0  # Start time for each robot
    for idx, row in robot_data.iterrows():
        route = row['routes']

        # Start at (0, 0) for each new segment
        time_df.loc[time, robot] = str((0, 0))

        # Traverse each point in the route, calculating travel time based on distance
        previous_position = (0, 0)  # Starting point
        for position in route:
            travel_time = calculate_distance(previous_position, position)  # Calculate travel time based on distance
            time += travel_time  # Increment time by travel time
            if time in time_df.index and any(time_df.loc[time] == str(position)):
                duplicate_count += 1  # Increment duplicate counter
            time_df.loc[time, robot] = str(position)
            previous_position = position  # Update the previous position

        # Return to (0, 0) after completing the route
        travel_time = calculate_distance(previous_position, (0, 0))
        time += travel_time  # Increment time to return to start
        if time in time_df.index and any(time_df.loc[time] == str((0, 0))):
            duplicate_count += 1  # Increment duplicate counter
        time_df.loc[time, robot] = str((0, 0))

# Sort the DataFrame by time index to ensure correct ordering
time_df = time_df.sort_index()

# Save the final DataFrame to a new CSV file
output_file_path = 'output/robot_time_slices.csv'
time_df.to_csv(output_file_path)

print(f"Output saved to: {output_file_path}")
print(f"Total number of duplicate coordinates handled: {duplicate_count}")