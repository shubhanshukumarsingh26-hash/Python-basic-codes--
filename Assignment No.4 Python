# Method 1: Using Python List
print(" Addition using Python List ")
r = 2
c = 2
A = [[1, 2],
     [3, 4]]
B = [[5, 6],
     [7, 8]]

#Addition
C = [[0]*c for _ in range(r)]
for i in range(r):
    for j in range(c):
        C[i][j] = A[i][j] + B[i][j]

print("Matrix A:", A)
print("Matrix B:", B)
print("Result C = A+B:", C)

# Method 2: Using NumPy
print("\n Addition using NumPy ")
import numpy as np

A_np = np.array([[1, 2],
                 [3, 4]])
B_np = np.array([[5, 6],
                 [7, 8]])

C_np = A_np + B_np
print("Matrix A:\n", A_np)
print("Matrix B:\n", B_np)
print("Result C = A+B:\n", C_np)


OUTPUT:
 Addition using Python List 
Matrix A: [[1, 2], [3, 4]]
Matrix B: [[5, 6], [7, 8]]
Result C = A+B: [[6, 8], [10, 12]]

 Addition using NumPy 
Matrix A:
 [[1 2]
 [3 4]]
Matrix B:
 [[5 6]
 [7 8]]
Result C = A+B:
 [[ 6 8]
 [10 12]]
