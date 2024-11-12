import matplotlib.pyplot as plt

# Data for the two series
data_series_1 = [
    440560, 280711, 215695, 180289, 158181,
    142127, 129707, 119835, 112075
]
data_series_2 = [
    440560, 281636, 218797, 183649, 162400,
    146226, 133962, 123684, 116211
]

# X-axis labels
x_labels = ['1', '2', '3', 'Order 4', '5',
            '6', '7', '8', '9']

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(x_labels, data_series_1, marker='o', label='Nearest Neighbor & 2-opt')
plt.plot(x_labels, data_series_2, marker='o', label='Nearest Neighbor')

# Adding labels and title
plt.xlabel('Orders/Wave')
plt.ylabel('Total Distance')
plt.title('Meters per Order/Wave')
plt.legend()

# Display the plot
plt.grid(True)
plt.show()
