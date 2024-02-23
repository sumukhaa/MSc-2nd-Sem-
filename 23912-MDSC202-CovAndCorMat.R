# Generate a 15x2 matrix with random integers
matrix <- matrix(sample(1:25, size = 15 * 2, replace = TRUE), nrow = 15, ncol = 2)
print(matrix)

x <- matrix[, 1]
y <- matrix[, 2]

# Mean
mean_x <- mean(x)
mean_y <- mean(y)
# printing Mean
print(mean_x)
print(mean_y)      

# Variance
var_x <- sum((x - mean_x)^2) / (length(x) - 1)
var_y <- sum((y - mean_y)^2) / (length(y) - 1)
# printing Variance
print(var_x)
print(var_y)      

# Covariance
covariance <- sum((x - mean_x) * (y - mean_y)) / (length(x) - 1)
print(covariance)   # printing  covariance

# Correlation
correlation <- covariance / (sqrt(var_x) * sqrt(var_y))
print(correlation)     # printing correlation

# Covariance matrix
covariance_matrix <- matrix(c(var_x, covariance, covariance, var_y), nrow = 2, byrow = TRUE)

# Correlation matrix
correlation_matrix <- matrix(c(1, correlation, correlation, 1), nrow = 2, byrow = TRUE)
# printing covariance_matrix
print("Covariance Matrix:")
print(covariance_matrix)          
# printing correlation_matrix
print("Correlation Matrix:")
print(correlation_matrix)   