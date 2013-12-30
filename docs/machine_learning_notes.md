Machine Learning Notes
======================

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
- The error is `J = sum((h(x) - j) ^ 2) / (2 * m)`.
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

### Support Vector Machines

### Clustering

### Dimensionality Reduction

### Anomaly Detection

### Recommender Systems

### Large Scale Machine Learning

### Photo OCR

