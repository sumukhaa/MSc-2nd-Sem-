# Simple Linear Regression

# Importing the Dataset
dataset = read.csv("The Rocket propellant Data.csv")


#install.packages("caTools")
library(caTools)
set.seed(123)

#install.packages("ggplot2")
library(ggplot2)

# Fitting the Simple Linear Regression Model using Training Set
regressor = lm(formula = Shear_strength ~ Age_of_propellant ,data = dataset)
print(regressor)

# Predicting the y value
y_pred = predict(regressor, newdata = dataset)
print(y_pred)

# Actual y value
y_act = dataset$Shear_strength
y_act

#Fitting a regression line
ggplot() + 
  geom_point(aes(x= dataset$Age_of_propellant, 
                 y = dataset$Shear_strength),
             colour = "red") +
  geom_line(aes(x= dataset$Age_of_propellant, 
                y = predict(regressor, newdata = dataset)),
            colour = "blue") +
  ggtitle("Shear_strength Vs Age_of_propellant (Regression line)") +
  xlab("Age_of_propellant") +
  ylab("Shear_strength")


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



