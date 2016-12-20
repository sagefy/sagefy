
Expectations for Guess and Slip Updates
---------------------------------------

### Bayes

The best formulation is likely a Bayesian update, given that the other parameters also update using Bayes.

    post = prior * likelihood / normal

`likelihood / normal` is the Bayes factor, determines how much the probability changes per update.

If `likelihood / normal` is 1, then there is no change in probability. If `l / n` is greater than 1, then the probability increases. If `l / n` is less than 1, then the probability decreases.

Either the likely or the normal will include addition or subtraction, because without it the numbers would just cancel out through division.

If `l / n` is negative or zero, probability drops to zero or less than zero.

If `n / l < p`, then the probability goes above one.

### Error Rate

Error rates can be measured as

    error = sqrt(
        sum((result - expectation)^2 for each instance)
        / num_instances
    )

The guess and slip update formulas should vastly beat a static guess of the guess slip and mean guess. Given a range of 0.01 -> 0.5, the error of the control is approximately 0.145.

The error should decrease with fewer cards being evaluated and more learner data available.

Preferably, the error rate would be in the range of a few hundredths, meaning 0.05 or less.

### Parameters

Parameters available for update include score and priors: guess, slip, learned, and transit.

A few notable formulas:

    p(answer is a slip | score == 0) = learned
    p(answer is a slip | score == 1) = 0
    p(answer is a slip | score) = learned * (1 - score)

    p(answer is a guess | score == 1) = 1 - learned
    p(answer is a guess | score == 0) = 0
    p(answer is a guess | score) = (1 - learned) * score

    p(correct | learned == 1) = 1 - slip
    p(correct | learned == 0) = guess
    p(correct | learned) = learned * (1 - slip) + (1 - learned) * guess

    p(incorrect | learned == 1) = slip
    p(incorrect | learned == 0) = 1 - guess
    p(incorrect | learned) = learned * slip + (1 - learned) * (1 - guess)

    p(correct | guess, learned) = learned + (1 - learned) * guess
    p(incorrect | guess, learned) = (1 - learned) * (1 - guess)
    p(correct | slip, learned) = learned * (1 - slip)
    p(incorrect | slip, learned) = learned * slip + (1 - learned)

If a learned answers correctly, guess should go up or stay the same (`l / n >= 1`), and slip should go down or stay the same (`l / n <= 1`).

If the learner answers incorrectly, guess should go down or stay the same (`l / n <= 1`), and slip should go up or stay the same (`l / n >= 1`).

A learner with a low `learned` tells us more about guess than a learner with a high `learned` when the answer is correct.

A learner with a high `learned` tells us more about slip than a learner with a low `learned` when the answer is incorrect.

Question: Negative cases... How does `learned` impact guess when answer is incorrect? How does `learned` impact slip when answer is correct? One of three possibilities: no impact, forward (low l, 0 == high impact on guess), inverse (high l, 0 == high impact on guess).

 learned | score | guess | slip
---------+-------+-------+------
 low     | 0     | ?     | +
 mid     | 0     | ?     | ++
 high    | 0     | ?     | +++
 low     | 1     | +++   | ?
 mid     | 1     | ++    | ?
 high    | 1     | +     | ?

### References

http://stats.stackexchange.com/questions/13275/bayesian-probability-1-is-it-possible

http://en.wikipedia.org/wiki/Bayesian_inference#Probability_of_a_hypothesis
