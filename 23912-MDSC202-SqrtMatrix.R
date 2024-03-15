# Given a positive definite square matrix,
# find its squareroot matrix

n = 3

# setting matrix input
matrixInput = c(5, 0, 0, 0, 5, 0, 0, 0, 6)

Mat = matrix(matrixInput, nrow=n, ncol=n)
print("Matrix", Mat)
eigen_values = eigen(Mat)

sqrt_eigvals = sqrt(eigen_values$values)

lambda = diag(sqrt_eigvals)

# calculating squareroot matrix
sqrt_Matrix = eigen_values$vectors %*% lambda %*% solve(eigen_values$vectors)

print("Square root of Matrix:")
print(sqrt_Matrix)
