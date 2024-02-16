#Importing the dataset
dataset = read.csv("Walmart.csv")

"
Dropping the date feature assuming it doesn't affect weekly sales 
(as it is a string)
"
df = subset(dataset, select = -c(Date))

#Importing a library
library(caTools)

#Setting the seed for randomness
set.seed(123)

#Setting the split ratio of training set and test set and also the target variable
split = sample.split(dataset$Weekly_Sales, SplitRatio = 0.8)
print(split)

# Splitting the dataset df into Training and Testing set
training_set = subset(df, split== TRUE)
test_set = subset(df, split == FALSE)

# Fitting the Multiple Linear Regression Model using Training Set 
regressor = lm(formula = Weekly_Sales ~ ., data = training_set)
print(regressor)

# Predicting the Test Set Results
y_pred = predict(regressor, newdata = test_set)
print(y_pred)

y_actual = test_set$Weekly_Sales
print(y_actual)
