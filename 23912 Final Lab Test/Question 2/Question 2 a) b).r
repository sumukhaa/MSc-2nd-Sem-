#Q2)
#a) Fitting MLR model on data set
data <- read.csv("Q2.csv")

model <- lm(GRE_Total ~ UGPA + GGPA, data = data)
summary(model)



#b) Printing p-values of the two independent variables
p_values <- summary(model)$coefficients[,4]
print(p_values)
