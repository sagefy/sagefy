---
title: Sequencer Background
layout: default
---

<script
src="//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>

Existing Systems
----------------

### Forgetting Curve

The Ebbinghaus model uses the following formula:

$$r=e^{-\frac{\tau}{s}}$$

where $$r$$ is retention, $$\tau$$ is time, and $$s$$ is strength.

### Learning Curve

A compliment to the Ebbinghaus Forgetting Curve:

$$a=1-e^{-\frac{\tau}{s}}$$

Other models suggest a sigmoid function. CDF of the logistic distribution:

$$a=\frac{1}{1+e^{-\frac{\tau-\mu}{s}}}$$

### Bayesian Knowledge Tracing

Bayesian Knowledge Tracing determines, given the pattern of learner responses, how likely a learner knows a skill.

Bayesian Knowledge Tracing is based on Bayes' Theorem.

$$p(A:B)=\frac{p(A)p(B:A)}{p(B)}$$

Here I am using `:` to mean 'given' because 'pipe' implies table to Markdown.

We call...

- $$p(A:B)$$ the posterior -- what we believe after seeing the data
- $$p(A)$$ the prior -- what we believe before the data
- $$p(B:A)$$ the likelihood -- how likely the data was given our prior belief
- $$p(B)$$ the normalizer -- how likely is the data given all hypotheses

As $$p(B)$$ can be difficult to formulate, often the following expression is useful.

$$p(B)=p(A)p(B:A)+p(\sim A)p(B:\sim A)$$

For BKT, we have the following factors:

- $$p(L)$$ - probability the skill is learned
- $$p(T)$$ - probability the skill will be learned on a particular item
- $$p(G)$$ - probability the learner will just guess the right answer
- $$p(S)$$ - probability the learner will mess up even knowing the skill

For any item, the probability of getting the answer correct is:

$$p(C)=p(L)p(\sim S)+p(\sim L)p(G)$$

Putting this all together, the probability the learner has learned the skill is, given a correct answer:

$$p(L_{-1}:Correct)=\frac{p(L_{-1})(1-p(S))}{p(L_{-1})(1-p(S))+(1-p(L_{-1}))p(G)}$$

Conversely...

$$p(L_{-1}:Incorrect)=\frac{p(L_{-1})p(S)}{p(L_{-1})p(S)+(1-p(L_{-1}))(1-p(G))}$$

All together...

$$p(L:Action)=p(L_{-1}:Action)+(1-p(L_{-1}:Action))p(T)$$

### Item Response Theory

[Item Response Theory](http://en.wikipedia.org/wiki/Item_response_theory) determines how likely a learner will correctly answer a particular question. It is described as a logistic function.

The parameters read:

- $$\theta$$ - learner ability
- $$b$$ - item difficulty
- $$a$$ - item discrimination; how likely the item determines ability
- $$c$$ - item guess

There are two common forms:

$$p(\theta)=\frac{e^{\theta-b}}{1+e^{\theta-b}}$$

$$p(\theta)=c+(1-c)\frac{e^{a(\theta-b)}}{1+e^{a(\theta-b)}}$$

The formulas change slightly depending on author.

Item Response Theory can be extended into Performance Factor Analysis, a competing model with Bayesian Knowledge Tracing.

### Knowledge Space Theory

[Knowledge Space Theory](http://en.wikipedia.org/wiki/Knowledge_space) represents what skills learner knows. KST is based on [antimatroids](http://en.wikipedia.org/wiki/Antimatroid).

We assume a learner has either learned a skill or not. Given skills `+`, `-`, `*`, and `/`, we would form prerequisites, such as:

- `+ -> -`
- `+ -> *`
- `* -> /`

The knowledge space represents all possible sets of knowledge a learner might have, such as:

- none
- `+`
- `+, -`
- `+, *`
- `+, *, /`
- `+, -, *, /`

An individual learner has a likelihood for each of these sets. KST makes the assumption that an individual question may inquire about multiple skills. We begin by asking questions that use multiple skills, and work backwards to assess learner knowledge.

Several automated systems exist to automatically determine prerequisites based on learner performance.

### Spaced Repetition

[Spaced Repetition](http://en.wikipedia.org/wiki/Spaced_repetition) suggests that learners will be more optimal by spreading out their practice, with reviews happening less frequently as ability improves.

The most popular algorithm is [SuperMemo 2](http://www.supermemo.com/english/ol/sm2.htm). The first review is after 1 day, the second review is after 6 days. After which, the next review is:

$$i_n=i_{n-1}e$$

...where $$e$$ is how difficult or easy the item is. $$e$$ is between 1.3 and 2.5, and it uses learner responses on a [Likert scale](http://en.wikipedia.org/wiki/Likert_scale) to determine the next time to review.

[Later versions of SuperMemo](http://www.supermemo.com/help/smalg.htm) include other considerations, such as:

- Similar cards
- Previous iteration duration
- Ebbinghaus forgetting curve

The latest is version [11/15](http://www.supermemo.com/english/algsm11.htm).

Distribution Types
------------------

For each distribution, I am most interested in $$\mu$$, or the mean of the distribution, and $$\sigma^2$$, or the variance, which can determine how confident we can be in our assertion.

### Beta Distribution

[Beta distributions](http://en.wikipedia.org/wiki/Beta_distribution) map probabilities from 0 to 1, where $$\alpha$$ is the count of positive examples and $$\beta$$ is the count of negative examples. Computation is fairly straightforward for most statistics.

$$f(x)=\frac{x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha,\beta)}$$

$$\mu=\frac{\alpha}{\alpha+\beta}$$

$$\sigma^2=\frac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}$$

...where $$\mu$$ is the mean and $$\sigma^2$$ is the variance.

### Exponential Distribution

The exponential distribution is often used to describe the frequency of time-bound events.

$$f(x)=\lambda e^{-\lambda x}$$

$$\mu=\lambda^{-1}$$

$$\sigma^2=\lambda^{-2}$$

### Normal Distribution

$$f(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

...where mu and sigma are provided. Mu and sigma can be determined from a sample by using a gaussian kernel.

### Pareto Distribution

The [Pareto Distribution](http://statisticalmodeling.wordpress.com/2011/06/23/the-pareto-distribution/) uses $$\alpha$$ for scale and $$\beta$$ for shape.

$$f(x)=1-(\frac{\alpha}{x+\alpha})^\beta$$

$$\mu=\frac{\alpha}{\beta+1}$$

$$\sigma^2=\frac{\alpha^2\beta}{(\beta-1)^2(\beta-2)}$$

### Poisson Distribution

The Poisson distribution is often used for counting events.

$$f(x)=\frac{\lambda^k}{k!}e^{-\lambda}$$

$$\mu=\lambda$$

$$\sigma^2=\lambda$$

### Binomial Distribution

Binomial distributions count the number $$n$$ of events each with a probability of $$p$$, where $$k$$ is the number of successes.

$$f(x)={n \choose k}p^k(1-p)^{n-k}$$

$$\mu=np$$

$$\sigma^2=np(1-p)$$

### Bernoulli Distribution

The Bernoulli Distribution only has two hypotheses: 0 or 1. The mean is the probably of 1.

$$\sigma^2=p(1-p)$$
