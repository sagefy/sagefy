---
title: Sequencer Background
layout: default
---

<script
src="//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>

Existing Systems
----------------

### Bayesian Knowledge Tracing

### Knowledge Spaces

### Item Response Theory

### Spaced Repetition

Distribution Types
------------------

## Beta Distribution

[Beta distributions](http://en.wikipedia.org/wiki/Beta_distribution) map probabilities from 0 to 1, where $$\alpha$$ is the count of positive examples and $$\beta$$ is the count of negative examples. Computation is fairly straightforward for most statistics.

$$\mu=\frac{\alpha}{\alpha+\beta}$$

$$\sigma^2=\frac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}$$

Prior Distributions
-------------------

### Forgetting Curve

The Ebbinghaus model uses the following formula:

$$r=e^{-\frac{\tau}{s}}$$

where $$r$$ is retention, $$\tau$$ is time, and $$s$$ is strength.

### Learning Curve

A compliment to the Ebbinghaus Forgetting Curve:

$$a=1-e^{-\frac{\tau}{s}}$$

Other models suggest a sigmoid function. CDF of the logistic distribution:

$$a=\frac{1}{1+e^{-\frac{\tau-\mu}{s}}}$$

### Item Response Theory Distributions

### Bayesian Knowledge Tracing Distribution
