---
title: Machine Learning Notes
layout: default
---

Andrew Ng's Coursera Course
---------------------------

### Welcome

- Machine learning comes from artifical intelligence.
- Machine learning involves mining data for information.
- Machine learning can solve problems that can't be solved by hand.
- Machine learning can solve customization problems.
- Machine learning can be used to understand human learning.
- Machine learning is defined as "Field of study that gives computers the ability to **learn without being explicitly programmed**." -- Arthur Samuel (1959).
- "A computer program is said to learn from _experience E_ with respect to some _task T_ and some _performance measure P_, if its performance on T, as measured by P, improves with experience E." -- Tom Mitchell (1998)
- **Supervised learning** takes both predictive features (domain) and a predicted value (range).
- **Regression**, a type of supervised learning, predicts a continous output (a single number).
- **Classification**, a type of supervised learning, predicts a discrete value (0 or 1).
- **Unsupervised learning** finds patterns within the data without seeking a specific result. Often synonomous with _clustering_.

### Linear Regression

- Use vectors and matrixes to keep track of features, values, and multipliers.
- `x` means feature (domain).
- `y` means value (range).
- `m` is the number of training examples.
- `n` represents the number of features.
- `h` means hypothesis.
- `theta` is a multiplier in the regression, also known as the parameters.
- In linear regression, the prediction function is `h(x) = theta[0] + theta[1] * x[1] + theta[2] * x[2] + ...`.
- The cost, or amount of error, is written as `J`.
- In linear regression, `J = sum((h(x) - y) ^ 2) / (2 * m)`.
- Our goal is to minimize the cost, `J`, to find the most accurate predictor function.
- We use **gradient descent** to minimize `J`. We start with a guess for `theta`, we continually change `theta` to reduce `J` until we reach a minimum.
- The descent calculation updates both `J` and `theta` on each iteration. It uses a _partial derivative_ of `theta`.
- The **learning rate** says how much to change in each descent. It's notated by `alpha`.
- If `alpha` is too large, gradient descent will fail to converge, or it will find a _local optima_. If it is too small, gradient descent will be too slow.
- A _local optima_ is a minimum that is not the global minimum of the function.
- In linear regression, the descent is `theta = theta - alpha * sum(h(x) - y) * x / m`.
- In **batch gradient descent**, each step uses all of the training examples.

### More on Linear Regression

- Use **feature scaling** to make sure each feature is on a similar scale. Typical is to use `-1` to `1`.
- The formula for feature scaling is `x[i] = x[i] - mu[i] / (max - min)`.
- `mu` represent the mean, or average.
- Alternatively, you can divide by the standard deviation, or `sigma`.
- **Converge** or accept the minimum if the change in `J` is less than `10 ^ -3` in one iteration.
- If `J` does not decrease consistently on each iteration, use a smaller `alpha`.
- Start with a small `alpha`, such as `0.001`, and multiply by three until you get to a fast enough learning rate.
- You can create a new feature by _multiplying two features together_. You can also make a new feature by _multiplying a feature by itself_. This will produce a **polynomial linear regression**.
- In small problems it is also possible to find the optimal version of `theta` simply by linear algebra: `theta = inverse(transpose(X) * X) * transpose(X) * y`. This method is too slow if `n` is very large.

### Classification

- A `0` is a negative class, and a `1` is a positive class.
- A **threshold** determines if we predict `1` or `0`. A default choice for  the threshold is `0.5`.
- For _classification_ problems, we often want to use **logistic regression** because the output will always be between `0` and `1`.
- In logistic regression, the hypothesis function is `h(x) = 1 / (1 + e ^ (-transpose(theta) * x))`. This is called the _logistic function_ or alternatively _sigmoid function_.
- The hypothesis tells us how likely a result is. In formula, `P(y = 1 | x; theta)`.
- The **decision boundary** determines which examples will be predicted as `1` or `0`.
- Decision boundaries can be non-linear if we use polynomial features.
- The cost function of logistic regression is the same as linear regression. Remember, however, that the hypothesis function is different.
- The cost function for logistic regression can be simplified to `J = -(sum(y * log(h(x))) + (1 - y) * log(1 - h(x))) / m`.
- The calculation for `theta` in logistic regression's gradient descent remains the same as linear regression.
- There are other ways to get the minimum cost. These include _conjugate gradient_, _BFGS_, and _L-BGFS_.
- For multiple classes, train a classifier for each class. Then, in prediction, use the class the receives the maximum value for the hypothesis.

### Regularization

- **Overfitting** is a major problem with machine learning. While fitting the training set very well, new examples are poorly predicted.
- The two main ways to deal with overfitting is to 1) reduce the number of features or 2) regularize the values of `theta`.
- In calculating `J`, add (or subtract) `lambda * sum(theta ^ 2) / m`. `lambda` is the regularization term.
- If `lambda` is too large, the algorithm will fail to converge or produce underfitting.

### Representing Neural Networks

- For some problems, it would take too many polynomial features to create a good predictor that is reasonably performant. An example is using pixels of an image as features.
- **Neural networks** can represent problem spaces with large number of interactive features effectively.
- It is designed to mimic the brain. Each neuron has input, dendrites, and output, axons. The center is the nucleus.
- Neural networks use the sigmoid function to ensure that outputs are always between `0` and `1`.
- A **bias unit** is added to regularize layers.
- There is an **input layer**, which is the features, an output hypothesis, and between there are **hidden layers**.
- `a` represents the activation of units.
- `Theta`, a matrix, represents the weights of the edges between the nodes, from layer `j` to layer `j + 1`.
- The hypothesis function essentially looks like a linear regression of linear regressions. The values of `Theta` first produce `a`s for each layer, then produces the hypothesis with `Theta` with the `a`s.
- Neural networks may contain many hidden layers.
- In a multiclass classification problem, the hypothesis can be a vector instead of a single number.

### Learning Neural Networks

- `L` is the number of layers in the network.
- `s[l]` is the number of units in layer `l`.
- The cost function of a neural network is, get ready for it... `J = -(sum(sum(y * log(h(x)) + (1 - y) * log(1 - h(x))))) / m + lambda * sum...(theta ^ 2) / (2 * m)`.
- To compute the descent of `Theta`, you need to use **backpropagation**.
- The full backpropagation algorithm is a little complicated, but involves `Delta[l][i, j] = Delta[l][i, j] + a[l][j] * delta[l + 1][j]` and `delta[L] = a[L] - y[i]`.
- You can check that your gradient descent is working by estimating how much `J` should change at each step. The formula is `approx = (J[theta + Epsilon] - J[theta - Epsilon]) / (2 * Epsilon)`. The change should be similar to, but not exactly, this result.
- Do not run this checking while actually training, or it will slow down the algorithm.
- When training a neural network, initialize using random values for `Theta`.

### General Advice

- Use **diagnostics** on your algorithm before jumping to huge conclusions.
- Evaluate your hypothesis by breaking your examples into 60%, 20% and 20% randomly. The first set is your **training set**, the second **cross validation set** and the third **test set**.
- The error is `J = sum((h(x) - y) ^ 2) / (2 * m)`.
- One way to select polynomial models is to start with just 1, then move up one at a time until the cross validation error does not improve.
- A similar technique can be used to train the regularization parameter, increasing until cross validation does not improve.
- Underfit is also called **bias** and overfit is also called **variance**.
- When the bias is high, the training error will be high, and the cross validation error and training error will be similar.
- When the variance is high, the training error will be low, and the cross validation error will be much higher than the training error.
- **Learning curves** plot the training and cross validation errors, given the domain is the training set size and the domain is the amount of error.
- In a high bias problem, getting more examples will not help. Try getting more features, adding polynomial features, or decreasing `lambda`.
- In a high variance problem, getting more examples will help. Also try reducing the number of features or increasing `lambda`.
- Neural networks are more prone to overfitting. Use regularization.

### Designing a System

- Where to invest time:
    - Collect data.
    - Develop feaetures.
    - Account for edge cases in features, such as misspellings.
- Start with a simple algorithm; get an implementation up quick and dirty.
- Plot a learning curve before moving forward.
- Examine the examples your algorithm predicts incorrectly.
- Find a single number for determining the quality of the system, usually the error rate.
- In the case of a **skewed class**, where positive example far outnumber negative examples, error rates are not informative. Instead use precision and recall.
- **Precision** measures of the predicted positive, what percentage is actually positive. The formula is `true positive / (true position + false positive)`.
- **Recall** measures how many postive examples were correctly predicted. The formula is `true positive / (true positive + false negative)`.
- The **F score** combines precision and recall into a single number for comparision. It's formula is `2 * P * R / (P + R)`.
- A useful test of whether an algorithm will success is if a _human expert_ could also make an accurate prediction.
- The **large data rationale** states you should use a learning algorithm with many features on a very large training set that is unlikely to overfit.

### Support Vector Machines

- Support vector machines are related to logistic regression.
- We want a large margin of confidence when making predictions. If `transpose(theta) * x` is greater than 1, or less than -1, we can be very confident in our prediction.
- Support vector machines try to find the largest margin between classes possible.
- The **gaussian kernel** can predict non-linear boundaries by identifying examples as _landmarks_. The predictions are then based on _similarity_ of examples.
- The similarity is measured by `exp(-length(x - l[i]) ^ 2 / (2 * sigma ^ 2))`.
- If `sigma` is large, then the features will vary more smoothly. This means high bias and low variance.
- If `sigma` is small, then there will be high variance and low bias.
- Use an SVM package for optimizations. You'll need to specify the **kernel** or similarity function, as well as a parameter `C`.
- Do feature scaling before using SVM.
- SVM packages often already have multiclass classification built-in.
- If `n >> m`, use logisitic regression.
- If `n < m`, use SVM with Gaussian kernel.
- If `n << m`, use logistic regression or SVM with linear kernel. Try adding more features.
- Neural networks work well for most combinations, but are prone to be slower.

### Clustering

- **K-means** is the most popular clustering, or unsupervised, algorithm.
- You must specify `K`, or the number of clusters.
- `K` must be less than `m`.
- Start with a random selection of cluster centroids. Then, find the closest centroids to each example. Then, move the centroid to the mean of the points assigned to that centroid. Continue until convergence.
- `J` is measured as `sum(len(x - mu) ^ 2) / m`.
- In general, you'll want to run K-means several times with different values of `K` and pick the one with the lowest cost. Local optima are possible as well.

### Dimensionality Reduction

- Sometimes we need to reduce the number of features.
- We can reduce several similar features down to a smaller number of features.
- **Principal Component Analysis** or PCA can be used to reduce down the number of features.
- Before running PCA, use feature scaling on the features you want to reduce.
- First, compute the _covariance matrix_ by `Sigma = sum(x[i] * transpose(x[i])) / m`.
- Use the _singular value decomposition_ on `Sigma` and take the first matrix `U`.
- The `U` matrix tells us how to reduce the features optimally. We can also use `U` to decompress the features back to their original state.
- You should eliminate down to the number of features, `k`, where `sum(length(x - x[approx]) ^ 2) / m / (sum(length(x) ^ 2) / m)` is less than 0.01. Alternatively, where `sum(S over k) / sum(S over m)` > 0.99.
- Only run PCA on the training set.
- PCA works well for performance and reducing space requirements, as well as visualizing data. It doesn't work as well to solve overfitting problems.
- Do PCA only if running the algorithm without PCA first doesn't work.

### Anomaly Detection

- Sometimes, we want to use machine learning to find problematic or abnormal examples. This includes fraud detection, manufactoring, and monitoring online systems.
- The **gaussian distribution** also known as the normal distribution will tell us if an example falls outside of the normal variance, also known as `sigma ^ 2`.
- We fit the parameters to `mu = sum(x) / m` and `sigma ^ 2 = sum((x - mu) ^ 2) / m`. When we have a new example, we compute `Pi(exp(-(x - mu) ^ 2 / (2 * sigma ^ 2)) / (sqrt(2 * pi) * sigma))`.
- Its easier to tell if we have a good algoritm if we have labeled examples. Use the _F score_ to detemine if the algorithm is good.
- You can also use cross validation to choose the threshold.
- Its common in anomaly detection to want to make features that include dividing an existing feature by another.
- Multivariate gaussian distribution is also possible.

### Recommender Systems

- Sometimes we want to make predictions both for examples and users. In this case, we have `nu` for the number of users, and `nm` for the examples. The matrix `r` determines if a user has engaged with an example. The matrix `y` evaluates this engagement. `y` may have empty values.
- We want to find `theta` such that `theta = min(sum((transpose(theta) * x - y) ^ 2) / 2 + sum(theta ^ 2) * lambda / 2 / 2)`.
- The **collaborative filtering** algorithm can find `theta` given `x`, and can find `x` given `theta`. Therefore, we just make a guess for `theta`, then produce `x`, then produce `theta`, and so forth, until we converge.
- The gradient descent step is:
    - `x = x - alpha * (sum(transpose(theta) * x - y) * theta + lambda * x)`
    - `theta = theta - alpha * (sum(transpose(theta) * x - y) * x + lambda * theta)`
- The prediction is `transpose(theta) * x`.
- We can use **low rank matrix factorization** to recommend new examples to the user.
- We can use **mean normalization** to initialize users with few to no examples.

### Large Scale Machine Learning

- Having more data means you can have more features without overfitting.
- Having more data makes batch gradient descent computationally expensive.
- Two alternatives to batch gradient descent are **stochastic gradient descent** and **mini-batch gradient descent**.
- A stochastic gradient descent updates theta for each example, one at a time, rather than each example on every iteration. Often, one to ten run throughs of the examples will converge.
- With mini-batch gradient descent, we randomly select a small number of examples on each iteration of batch gradient descent. Often, this is the fastest route to an accurate model.
- Another way to speed up batch gradient descent is to use **map-reduce**. Have each machine handle part of the summation, and combine the summations in the reduce step.
- With any example, if you have difficulty converging, use a smaller `alpha`.
- In a system where new examples are constantly coming in, use **online learning**.
- In online learning, we update `theta` for each new example, using `theta = theta - alpha * (h(x) - y) * x`.
- Online learning systems can adapt to changes in user preferences.

### Photo OCR

- To create new examples from existing data, you can distort existing examples. Add noise, rotate, blur, stretch, skew...
- Crowd sourcing can help produce more examples as well.
- Often machine learning systems involve multiple machine learning components. Measure the error rate of the pipeline. Any component that varies greatly from the overall system error rate will be a candidate for improvement.
