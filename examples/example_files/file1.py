# This Python script processes a dataset and outputs basic statistics.

import numpy as np

# Dataset
data = [12, 15, 17, 19, 24, 29, 33, 35, 39]

# Calculate mean and standard deviation
mean = np.mean(data)
std_dev = np.std(data)

# Output results
print(f"Mean: {mean}")
print(f"Standard Deviation: {std_dev}")
