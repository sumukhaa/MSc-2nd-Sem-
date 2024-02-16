# Simple Linear Regression

# Importing the Dataset
dataset = read.csv("Salary_Data.csv")

# Splitting the Dataset into Training and Testing set
# install.packages("caTools")

library(caTools)
set.seed(123)
split = sample.split(dataset$Salary, SplitRatio = 2/3)
print(split)

training_set = subset(dataset, split== TRUE)
test_set = subset(dataset, split == FALSE)

# Fitting the Simple Linear Regression Model using Training Set

regressor = lm(formula = Salary ~ YearsExperience ,data = training_set)
print(regressor)

# Predicting the Test Set Results
y_pred = predict(regressor, newdata = test_set)

print(y_pred)

# Visualizing the Training Set Results

#install.packages("ggplot2")
library(ggplot2)

ggplot() + 
geom_point(aes(x= training_set$YearsExperience, 
                y = training_set$Salary),
                colour = "red") +
  geom_line(aes(x= training_set$YearsExperience, 
                y = predict(regressor, newdata = training_set)),
                colour = "blue") +
  ggtitle("Salary Vs YearsExperience (Training Set Results)") +
  xlab("Years of Experience") +
  ylab("Salary")

### Visualizing the Testing Set Results
ggplot() + 
  geom_point(aes(x= test_set$YearsExperience, 
                 y = test_set$Salary),
             colour = "red") +
  geom_line(aes(x= test_set$YearsExperience, 
                y = y_pred),
            colour = "blue") +
  ggtitle("Salary Vs YearsExperience (Testing Set Results)") +
  xlab("Years of Experience") +
  ylab("Salary")




