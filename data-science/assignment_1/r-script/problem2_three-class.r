library(tree)

vertebralcolumn  <- read.table("https://www.uio.no/studier/emner/matnat/math/STK2100/v19/mandatoryassignments-exam/vertebralcolumn.dat", header=TRUE)

vertebralcolumn[ ,'class'] <- as.factor(vertebralcolumn[ ,'class'])

divide.data <- function(dataset, size.train)
# Divide dataset into training and testset
{
    n <- nrow(dataset)
    n.train <- round(n * size.train)
    n.test <- n - n.train
    permutation <- sample(1:n, n)
    train.index <- sort(permutation[1:n.train])

    train <- dataset[train.index, ]
    test <- dataset[-train.index, ]

    n.grow <- round(n.train * 0.75)
    grow.index <- sort(sample(train.index, n.grow))
    prune.index <- setdiff(train.index, grow.index)
    grow <- dataset[grow.index, ]
    prune <- dataset[prune.index, ]
    return(list("train"=train, "test"=test, "grow"=grow, "prune"=prune))
}


# Divide into healthy and unhealthy
healthy <- vertebralcolumn[vertebralcolumn[ ,'class'] == 'NO', ]
unhealthy <- vertebralcolumn[vertebralcolumn[ ,'class'] != 'NO', ]

# Divide into grow, prune and test set
data.healthy <- divide.data(healthy, 2/3)
data.unhealthy <- divide.data(unhealthy, 2/3)

# Combine unhealthy and healthy sets
data.grow <- rbind(data.healthy$grow, data.unhealthy$grow)
data.prune <- rbind(data.healthy$prune, data.unhealthy$prune)
data.test <- rbind(data.healthy$test, data.unhealthy$test)

f1 <- as.formula(paste("class ~ ", paste(head(names(data.grow), n=-1), collapse = "+"),
                        collapse = NULL))
t1<- tree(f1, data = data.grow, control = tree.control(nobs = nrow(data.grow),
                                                            minsize = 0, mindev = 0))
plot(t1)

# Use cross validation to find deviance vs complexity
t2 <- cv.tree(t1)
# save fig
plot(t2)

# Select tree size that minimises deviance
J <- t2$size[t2$dev == min(t2$dev)]
J <- min(J)

# Prune tree
t3 <- prune.tree(t1, newdata=data.prune, method='misclass', best = J)
plot(t3)
text(t3)

##
## COMPUTE PREDICTIONS AND ERROR
##
p.original <- predict(t1, newdata = data.test, type = "class")
p.pruned <- predict(t3, newdata = data.test, type = "class")
# table 5.11
# confusion.matrix(p3, juice2[ , "choice"])

a1 <-  table(p.original, data.test$class)
err.original <- 1 - sum(diag(a1)) / sum(a1)

a2 <-  table(p.pruned, data.test$class)
err.pruned <- 1 - sum(diag(a2)) / sum(a2)

##
## QDA AND PDA
##
library(MASS)
d1 <- lda(f1, data = data.grow)
q1 <- qda(f1, data = data.grow)

p.lda <- predict(d1, newdata = data.test, type = "class")
p.qda <- predict(q1, newdata = data.test, type = "class")

a3 <-  table(p.lda$class, data.test$class)
err.lda <- 1 - sum(diag(a3)) / sum(a3)

a4 <-  table(p.qda$class, data.test$class)
err.qda <- 1 - sum(diag(a4)) / sum(a4)

err.original
err.pruned
err.lda
err.qda
