#Q1) 





# a) Finding correlation coefficient between X and Y

dataset = read.csv("Q1.csv")

#Let r be correlation coefficient
r <- cor(dataset$Months, dataset$Songs)
r







# b) Getting Regression Coefficients from Excel

# Data coefficients got from excel
B0 <- -12.88728849
B1 <- 21.12638093






# c) Fitting the obtained line equation on the Scatter plot

# Plotting scatter plot
plot(dataset$Months, dataset$Songs, main = "ScatterPlot for Q1) c)",
     xlab = "Months", ylab = "Songs")

# Function to generate the fitted line
get_equation <- function(B1, B0){
  paste0("y=", format(B1,digits=4), "*x+", format(B0, digits=4))
  }

# Get equation string
equation <- get_equation(B1, B0)

# Add the fitted line
abline(a=B0, b=B1, lty=2, col="blue", label=equation)  

# display the equation
legend("topleft", legend = equation, bty ="n")


