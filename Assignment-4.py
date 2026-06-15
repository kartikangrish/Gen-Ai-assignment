# ==============================================================================
# NUMPY ASSIGNMENT
# ==============================================================================

import numpy as np

# 1. Create an array of 10 zeros
zeros_arr = np.zeros(10)
print("10 Zeros:\n", zeros_arr)

# 2. Create an array of 10 ones
ones_arr = np.ones(10)
print("\n10 Ones:\n", ones_arr)

# 3. Create an array of 10 fives
fives_arr = np.ones(10) * 5
print("\n10 Fives:\n", fives_arr)

# 4. Create an array of the integers from 10 to 50
range_10_50 = np.arange(10, 51)
print("\nIntegers from 10 to 50:\n", range_10_50)

# 5. Create an array of all the even integers from 10 to 50
evens_10_50 = np.arange(10, 51, 2)
print("\nEvens from 10 to 50:\n", evens_10_50)

# 6. Create a 3x3 matrix with values ranging from 0 to 8
matrix_3x3 = np.arange(0, 9).reshape(3, 3)
print("\n3x3 Matrix (0-8):\n", matrix_3x3)

# 7. Create a 3x3 identity matrix
identity_matrix = np.eye(3)
print("\n3x3 Identity Matrix:\n", identity_matrix)

# 8. Use NumPy to generate a random number between 0 and 1
rand_num = np.random.rand(1)
print("\nRandom number (0 to 1):\n", rand_num)

# 9. Use NumPy to generate an array of 25 random numbers sampled from a standard normal distribution
rand_normal = np.random.randn(25)
print("\n25 Random standard normal numbers:\n", rand_normal)

# 10. Create the specific decimal grid matrix (0.01 to 1.0)
decimal_matrix = np.arange(1, 101).reshape(10, 10) / 100
print("\nDecimal Matrix:\n", decimal_matrix)

# 11. Create an array of 20 linearly spaced points between 0 and 1
linspace_arr = np.linspace(0, 1, 20)
print("\n20 Linearly spaced points:\n", linspace_arr)


# --- NUMPY INDEXING AND SELECTION ---

# Given Base Matrix setup:
mat = np.arange(1, 26).reshape(5, 5)
print("\nBase Matrix 'mat':\n", mat)

# 12. Replicate output: [[12, 13, 14, 15], [17, 18, 19, 20], [22, 23, 24, 25]]
slice_1 = mat[2:, 1:]
print("\nSlice 1 (Rows 2+, Cols 1+):\n", slice_1)

# 13. Replicate output: 20
val_20 = mat[3, 4]
print("\nValue 20:\n", val_20)

# 14. Replicate output: [[2], [7], [12]]
slice_2 = mat[:3, 1:2]
print("\nSlice 2 (Column 1 as column matrix):\n", slice_2)

# 15. Replicate output: [21, 22, 23, 24, 25]
slice_3 = mat[4, :]
print("\nSlice 3 (Last row):\n", slice_3)

# 16. Replicate output: [[16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]
slice_4 = mat[3:, :]
print("\nSlice 4 (Last two rows):\n", slice_4)


# --- NUMPY MATH AND AGGREGATIONS ---

# 17. Get the sum of all the values in mat
total_sum = mat.sum()
print("\nSum of all values:\n", total_sum)

# 18. Get the standard deviation of the values in mat
std_dev = mat.std()
print("\nStandard deviation:\n", std_dev)

# 19. Get the sum of all the columns in mat
col_sum = mat.sum(axis=0)
print("\nSum of columns:\n", col_sum)
