#Importing the dataset
dataset = read.csv("Student_Performance.csv")

# Encoding the Categorical "Extracurricular_Activities" Column
dataset$State = factor(dataset$Extracurricular_Activities,
                       levels = c("Yes", "No"),
                       labels = c(1,0))

#Importing a library
library(caTools)

#Setting the seed for randomness
set.seed(123)

#Setting the split ratio of training set and test set and also the target variable
split = sample.split(dataset$Performance_Index, SplitRatio = 0.8)
print(split)

# Splitting the data set into Training and Testing set
training_set = subset(dataset, split== TRUE)
test_set = subset(dataset, split == FALSE)

# Fitting the Multiple Linear Regression Model using Training Set 
regressor = lm(formula = Performance_Index ~ ., data = training_set)
print(regressor)

# Predicting the Test Set Results
y_pred = predict(regressor, newdata = test_set)
print(y_pred)

y_actual = test_set$Performance_Index
print(y_actual)
