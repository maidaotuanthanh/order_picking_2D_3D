import numpy as np
import pandas as pd
import ast

# Load the data
file_path = 'input/output_collision.csv'
data = pd.read_csv(file_path)

# Convert the routes from string representation to list of tuples
data['routes'] = data['routes'].apply(ast.literal_eval)

# Extract all unique robot IDs
robots = data['robot'].unique()

# Create a dictionary to store the time slices for each robot
time_slices = {robot: [] for robot in robots}


# Calculate the Euclidean distance between two points
def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# Fill the time slices with the positions at each time step
for robot in robots:
    robot_data = data[data['robot'] == robot]
    time = 0
    for idx, row in robot_data.iterrows():
        route = row['routes']
        # Start at (0,0)
        if time == 0 or time_slices[robot][-1][1] != (0, 0):
            time_slices[robot].append((time, (0, 0)))
        for i in range(len(route)):
            if i > 0:
                time += calculate_distance(route[i - 1], route[i])
            time_slices[robot].append((time, route[i]))
        # Return to (0, 0) after completing the route
        time += calculate_distance(route[-1], (0, 0))
        time_slices[robot].append((time, (0, 0)))

    # Ensure the final position is (0, 0)
    if time_slices[robot][-1][1] != (0, 0):
        time += calculate_distance(time_slices[robot][-1][1], (0, 0))
        time_slices[robot].append((time, (0, 0)))

# Create a list of all unique time steps
all_time_steps = sorted(set([time_step for slices in time_slices.values() for time_step, _ in slices]))

# Create a DataFrame to store the positions at each time step for each robot
time_df = pd.DataFrame(index=robots, columns=all_time_steps)

# Fill the DataFrame with positions
for robot, slices in time_slices.items():
    for time_step, position in slices:
        time_df.loc[robot, time_step] = str(position)


# Unify the coordinate format to use tuples
def unify_coordinates_format(position):
    if pd.notna(position):
        position = position.replace('[', '(').replace(']', ')')
    return position


# Apply the coordinate format unification
time_df = time_df.applymap(unify_coordinates_format)

# Transpose the DataFrame to switch rows and columns
time_df_transposed = time_df.transpose()

# Filter out columns with NaN values only
time_df_transposed = time_df_transposed.dropna(how='all', axis=1)

# Ensure the final row for each robot is (0, 0)
for robot in robots:
    last_position = time_df_transposed[robot].dropna().iloc[-1]
    if last_position != '(0, 0)':
        time_df_transposed.loc[max(time_df_transposed.index) + 1, robot] = '(0, 0)'

# Save the final DataFrame to a new CSV file
output_file_path = 'output/robot_time_slices_final_corrected.csv'
time_df_transposed.to_csv(output_file_path)

print(f'Output saved to: {output_file_path}')
