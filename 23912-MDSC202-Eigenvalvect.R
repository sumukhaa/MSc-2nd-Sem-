A <- matrix(data=c(3,2,1,1,2,3,1,2,4),nrow=3,ncol=3)
print(A)

# Calculate eigenvalues and eigenvectors and normalised eigenvectors
eigen_result <- eigen(A)

# Eigenvalues
eigenvalues <- eigen_result$values
print("Eigenvalues:")
print(eigenvalues)

# Eigenvectors
eigenvectors <- eigen_result$vectors
print("Eigenvectors:")
print(eigenvectors)

# Normalize eigenvectors
sqrt(rowSums(eigenvectors^2))
normalized_eigenvectors <- eigenvectors / sqrt(rowSums(eigenvectors^2))
print("Normalized Eigenvectors:")
print(normalized_eigenvectors)