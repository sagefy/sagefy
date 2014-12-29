def guess_likelihood(score, guess, slip, learned):
    if score == 1:
        return learned + (1 - learned) * guess
    if score == 0:
        return 1 - (learned + (1 - learned) * guess)


def guess_normal(score, guess, slip, learned):
    if score == 1:
        return learned
    if score == 0:
        return 1 - learned


def slip_likelihood(score, guess, slip, learned):
    if score == 1:
        return learned * slip + (1 - learned)
    if score == 0:
        return 1 - (learned * slip + (1 - learned))


def slip_normal(score, guess, slip, learned):
    if score == 1:
        return learned
    if score == 0:
        return 1 - learned


def guess_bayes(score, guess, slip, learned):
    return (guess_likelihood(score, guess, slip, learned)
            / guess_normal(score, guess, slip, learned))


def slip_bayes(score, guess, slip, learned):
    return (slip_likelihood(score, guess, slip, learned)
            / slip_normal(score, guess, slip, learned))


def update_guess(score, guess, slip, learned):
    return (guess
            * guess_likelihood(score, guess, slip, learned)
            / guess_normal(score, guess, slip, learned))


def update_slip(score, guess, slip, learned):
    return (slip
            * slip_likelihood(score, guess, slip, learned)
            / slip_normal(score, guess, slip, learned))


# ### TESTS ### #

print('If a learner answers correctly, guess should go up or stay the same.')

assert update_guess(1, 0.3, 0.1, 0.7) >= 0.3
assert update_guess(1, 0.1, 0.3, 0.7) >= 0.1
assert update_guess(1, 0.01, 0.01, 0.01) >= 0.01
assert update_guess(1, 0.99, 0.99, 0.99) >= 0.99

print('If a learner answers correctly, slip should go down or stay the same.')

assert update_slip(1, 0.3, 0.1, 0.7) <= 0.1
assert update_slip(1, 0.1, 0.3, 0.7) <= 0.3
assert update_slip(1, 0.01, 0.01, 0.01) <= 0.01
assert update_slip(1, 0.99, 0.99, 0.99) <= 0.99

print('If a learner answers incorrectly, ' +
      'guess should go down or stay the same.')

assert update_guess(0, 0.3, 0.1, 0.7) <= 0.3
assert update_guess(0, 0.1, 0.3, 0.7) <= 0.1
assert update_guess(0, 0.01, 0.01, 0.01) <= 0.01
assert update_guess(0, 0.99, 0.99, 0.99) <= 0.99

print('If a learner answers incorrectly, slip should go up or stay the same.')

assert update_slip(0, 0.3, 0.1, 0.7) >= 0.1
assert update_slip(0, 0.1, 0.3, 0.7) >= 0.3
assert update_slip(0, 0.01, 0.01, 0.01) >= 0.01
assert update_slip(0, 0.99, 0.99, 0.99) >= 0.99

print('A learner with a low learned tells us more about guess ' +
      'than a learner with a high learned when the answer is correct.')

assert update_guess(1, 0.3, 0.1, 0.2) > update_guess(1, 0.3, 0.1, 0.8)
assert update_guess(1, 0.01, 0.01, 0.01) > update_guess(1, 0.01, 0.01, 0.99)
assert update_guess(1, 0.99, 0.99, 0.01) > update_guess(1, 0.99, 0.99, 0.99)

print('A learner with a high learned tells us more about slip ' +
      'than a learner with a low learned when the answer is incorrect.')

assert update_slip(0, 0.3, 0.1, 0.2) < update_slip(0, 0.3, 0.1, 0.8)
assert update_slip(0, 0.01, 0.01, 0.01) < update_slip(0, 0.01, 0.01, 0.99)
assert update_slip(0, 0.99, 0.99, 0.01) < update_slip(0, 0.99, 0.99, 0.99)

print('If l / n is negative or zero, ' +
      'probability drops to zero or less than zero.')

assert guess_bayes(0, 0.3, 0.1, 0.7) > 0
assert guess_bayes(0, 0.01, 0.01, 0.01) > 0
assert guess_bayes(0, 0.99, 0.99, 0.99) > 0
assert guess_bayes(1, 0.3, 0.1, 0.7) > 0
assert guess_bayes(1, 0.01, 0.01, 0.01) > 0
assert guess_bayes(1, 0.99, 0.99, 0.99) > 0

assert slip_bayes(0, 0.3, 0.1, 0.7) > 0
assert slip_bayes(0, 0.01, 0.01, 0.01) > 0
assert slip_bayes(0, 0.99, 0.99, 0.99) > 0
assert slip_bayes(1, 0.3, 0.1, 0.7) > 0
assert slip_bayes(1, 0.01, 0.01, 0.01) > 0
assert slip_bayes(1, 0.99, 0.99, 0.99) > 0

print('If n / l < p, then the probability goes above one.')

assert guess_bayes(0, 0.3, 0.1, 0.7) ** -1 > 0.3
assert guess_bayes(0, 0.01, 0.01, 0.01) ** -1 > 0.01
assert guess_bayes(0, 0.99, 0.99, 0.99) ** -1 > 0.99
assert guess_bayes(1, 0.3, 0.1, 0.7) ** -1 > 0.3
assert guess_bayes(1, 0.01, 0.01, 0.01) ** -1 > 0.01
assert guess_bayes(1, 0.99, 0.99, 0.99) ** -1 > 0.99

assert slip_bayes(0, 0.3, 0.1, 0.7) ** -1 > 0.1
assert slip_bayes(0, 0.01, 0.01, 0.01) ** -1 > 0.01
assert slip_bayes(0, 0.99, 0.99, 0.99) ** -1 > 0.99
assert slip_bayes(1, 0.3, 0.1, 0.7) ** -1 > 0.1
assert slip_bayes(1, 0.01, 0.01, 0.01) ** -1 > 0.01
assert slip_bayes(1, 0.99, 0.99, 0.99) ** -1 > 0.99
