# Multiple Linear Regression
 dataset = read.csv("50_Startups.csv")

 # Encoding the Categorical "State" Column
 dataset$State = factor(dataset$State,
                        levels = c("New York", "California", "Florida"),
                        labels = c(1,2,3))
 
 # Splitting the Dataset into Training and Testing set
 # install.packages("caTools")
 
 library(caTools)
 set.seed(123)
 split = sample.split(dataset$Profit, SplitRatio = 0.8)
 print(split)
 
 training_set = subset(dataset, split== TRUE)
 test_set = subset(dataset, split == FALSE)
 
 # Fitting the Multiple Linear Regression Model using Training Set
 
 regressor = lm(formula = Profit ~ ., data = training_set)
 print(regressor)
 
 # Predicting the Test Set Results
 y_pred = predict(regressor, newdata = test_set)
 
 print(y_pred)
print(test_set$Profit)
 