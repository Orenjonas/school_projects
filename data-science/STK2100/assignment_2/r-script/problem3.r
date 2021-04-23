

# FUNCTION DEFINITIONS 

divide.data <- function(dataset, fraction) {
    # Divide dataset into two groups, selecting randomly from dataset.
    # Size of goup 1 is: fraction*(size of dataset).
    #
    # Args:
    #  dataset(data.frame): Data to be splitted
    #  fraction(int): Portion of dataset to be split into group 1
    #
    # Returns:
    # list of dataframes. The first is the biggest

    n <- nrow(dataset)
    fraction <- round(n * fraction)
    permutation <- sample(1:n, n)
    idx1 <- sort(permutation[1:fraction])

    set1 <- dataset[idx1, ]
    set2 <- dataset[-idx1, ]
    return(list(set1, set2))
}
split.k.ways <- function(dataset, k) {
    # Split data randomly into n different parts of equal size.
    # If the set does not split evenly some observations are dropped
    #
    # Args:
    #   dataset(data.frame): Data to be splitted
    #   n(int):	             Number of sets desired
    #
    # Returns:
    #  list containing n datasets

    n <- nrow(dataset)
    permutation <- sample(1:n, n)
    sets <- list()
    interval <- floor(nrow(dataset)/k)
    for (i in 1:k) {
	idx <- sort(permutation[((i-1)*interval+1):(i*interval)])
	sets[[i]] <- dataset[idx, ]
    }
    return(sets)
}



# MAIN

library(kknn)
library(dplyr)

dataset <- read.table("https://www.uio.no/studier/emner/matnat/math/STK2100/v19/mandatoryassignments-exam/data.dat", header=TRUE)

splitted <- divide.data(dataset, 0.5)
train <- splitted[[1]]
test <-splitted[[2]]

sets <- split.k.ways(train, k=5)


# FIND OPTIMAL k USING 5-FOLD CROSS VALIDATION
K <- 1:20
RSS <- numeric(length(K))
RSS.i <- numeric(5)
for (k in 1:length(K)) {
    for (i in 1:length(sets)) {
	set <- sets[[i]]
	cv.test <- set
	cv.train <- setdiff(train, cv.test)
	# x <- cv.train$x
	# y <- cv.train$y
	fit <- kknn(y ~ x, train = cv.train, test = cv.test, k = k)
	RSS.i[i] <- mean((fit$fitted.values - cv.test$y)^2)
    }
    RSS[k] <- mean(RSS.i)
}
k <- which(RSS == min(RSS))
print(k)


# PLOT k VS ERROR
plot(K, RSS, type = "b", xlab = "k", pch = 16,
     ylab = "Error", cex = 2, lwd = 3)



# FIT THE KNN MODEL
x <- train$x
y <- train$y
# Fit the model to the train data
fit.knn <- kknn(y ~ x, train=train, test=train, k=k)

# PLOT KNN VS TRAINING DATA
plot(x, y, xlab = "x", ylab = "y", pch = 16, cex = 1.5)
lines(sort(x), fit.knn$fitted.values[order(x)], col = 2, lwd = 2, lty = 1)

# SPLINES
library(splines)


# FIND OPTIMAL LAMBDA USING 5-FOLD CROSS VALIDATION
lambdas <- seq(0, 4e-04, length.out=1000)
RSS <- numeric(length(lambdas))
RSS.i <- numeric(5)
for (j in 1:length(lambdas)) {
    for (i in 1:length(sets)) {
	cv.test <- sets[[i]]
	cv.train <- setdiff(train, cv.test)
	x <- cv.train$x
	y <- cv.train$y
	m <- smooth.spline(x, y, lambda = lambdas[j], nknots = 5)
	fit <- predict(m, x=cv.test$x)
	RSS.i[i] <- mean((fit$y - cv.test$y)^2)
    }
    RSS[j] <- mean(RSS.i)
}
lambda <- lambdas[which(RSS == min(RSS))]
print(lambda)

# PLOT LAMBDA VS ERROR
plot(lambdas, RSS, type = "b", xlab = "lamda", pch = 16,
     ylab = "Error", cex = 2, lwd = 3)


# FIT QUBIC SPLINE
x <- train$x
y <- train$y
x.knots <- seq(min(x), max(x), length = 7)
x0 <- seq(min(x), max(x), length = 200)
m.qspline <- lm(y ~ bs(x, knots = x.knots[2:6], degree = 3))
fit.qspline <- predict(m.qspline,  data.frame(x = x0))

# FIT SMOOTHING SPLINE
m.sspline <- smooth.spline(x, y, lambda = lambda, nknots = 5)
fit.sspline <- predict(m.sspline, x=x0)


# PLOT FITTED MODELS OVER TRAINING DATA
cols <- c(2,3,4)
ltys <- c(1,2,3)

# jpeg('plots3/fitted_models.jpg')
plot(x, y, xlab = "x", ylab = "y", pch = 16, cex = 1.5)
lines(sort(x), fit.knn$fitted.values[order(x)], col = cols[1], lwd = 2, lty = ltys[1])
lines(x0, fit.qspline, col = cols[2], lwd = 2, lty=ltys[2])
lines(fit.sspline, col = cols[3], lty = ltys[3], lwd = 3)
legend('topleft' , legend = c("kNN",
			  "qubic spline", 
			  "smoothing spline"),
       col = cols, lty = ltys, cex = 1.5)
# dev.off()


# ERRORS
x <- test$x
y <- test$y

error <- list()

# Fit the model to the test data
fit.knn <- kknn(y ~ x, train=train, test=test, k=k)
error['kNN model'] <- mean((fit.knn$fitted.values - test$y)^2)

fit.qspline <- predict(m.qspline,  data.frame(x = x))
error['Non penalized cubic spline'] <- mean((fit.qspline - test$y)^2)

fit.sspline <- predict(m.sspline,  data.frame(x = x))
error['Smoothing spline'] <- mean((fit.sspline$y - test$y)^2)
error



