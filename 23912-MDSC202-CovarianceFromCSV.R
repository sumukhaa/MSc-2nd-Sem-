options(max.print = 99999)

# Load the data
data <- read.csv("MW-All-Indices-01-Mar-2024.csv", header = FALSE)
print(data)

# CLEANING THE DATA

# Extract the first 74 rows and 15 columns
subset_data <- data[2:74, 2:15]
print(subset_data)

# Remove commas and convert the columns to numeric
subset_data <- apply(subset_data, 2, function(x) as.numeric(gsub(",", "", x)))
print(subset_data)

# Remove rows with missing values
subset_data <- na.omit(subset_data)
print(subset_data)

# COVARIANCE
# Number of observations for finding Variance-Covariance matrix
n <- nrow(subset_data)
print(n)

# Mean of each variable
means <- colMeans(subset_data)
print(means)

#1s column vector
one_matrix <- matrix(1, ncol = 1, nrow = nrow(subset_data))
print(one_matrix)


xminusxbar <- subset_data - one_matrix %*% means
xminusxbar

final <- t(xminusxbar) %*% xminusxbar
final <- 1/(n-1) * final
final

sd <- sqrt(diag(final))
cor <- final / (sd %*% t(sd))
print(cor)


# Save cov_matrix to a CSV file
write.csv(cor, file = "covariance_matrix.csv")
