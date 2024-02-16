# Simple Linear Regression

# Importing the Dataset
dataset = read.csv("Eucalypt Hardwoods.csv")

# Splitting the Dataset into Training and Testing set
#install.packages("caTools")
library(caTools)
set.seed(123)

#install.packages("ggplot2")
library(ggplot2)

# Fitting the Simple Linear Regression Model using Training Set
regressor = lm(formula = hardness ~ density ,data = dataset)
print(regressor)

# Predicting the y value
y_pred = predict(regressor, newdata = dataset)
print(y_pred)

# Actual y value
y_act = dataset$hardness
y_act

#Fitting a regression line
ggplot() + 
  geom_point(aes(x= dataset$density, 
                 y = dataset$hardness),
             colour = "red") +
  geom_line(aes(x= dataset$density, 
                y = predict(regressor, newdata = dataset)),
            colour = "blue") +
  ggtitle("Density Vs Hardness (Regression line)") +
  xlab("Density") +
  ylab("Hardness")


# Finding residuals
residual = y_pred - y_act
residual


#Plotting residual plot
ggplot() + 
  geom_point(aes(x= y_pred, 
                 y = residual),
             colour = "red") +
  geom_hline(yintercept = 0,
             linetype = "solid",
             colour = "blue") +
ggtitle("y_pred vs Residual (Residual plot)") +
  xlab("y_pred") +
  ylab("Residual")



