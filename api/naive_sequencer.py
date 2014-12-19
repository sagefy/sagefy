from math import exp, fsum
from sequence_gen import generate_responses


"""
Learning parameters:

- **Learned**: The probability of having learned the skill
- **Guess**: The probability of guessing an card response
- **Slip**: The probability of slipping on a card
- **Transit**: The probability of learning the skill on the given card
- **Belief**: The probability of the learned being accurate
- **Quality**: How well does the entity promote learning?
"""

init_learned = 0.4
required_learned = 0.95
init_belief = 0.5
required_belief = 0.95
init_guess = 0.2
max_guess = 0.4
init_slip = 0.05
max_slip = 0.2
init_transit = 0.05
belief_k = 0.000001  # The factor that alters the impact of time on belief
# TODO: What should `belief_k` be?


def main():
    responses = generate_responses()
    # schema: card, time (seconds), score
    cards = {}
    learner = {
        'learned': init_learned,
        'belief': init_belief,
    }
    rows = []

    for i, response in enumerate(responses):
        if response['card'] not in cards:
            cards[response['card']] = {
                'guess': init_guess,
                'slip': init_slip,
                'transit': init_transit,
            }

        card = cards[response['card']]

        row_stats = response.copy()

        # compute_correct  - no prior belief
        row_stats['correct'] = compute_correct(
            learned=learner['learned'],
            guess=card['guess'],
            slip=card['slip'],
        )

        # compute_belief - always first update
        row_stats['belief'] = learner['belief'] = compute_belief(
            time0=responses[i - 1]['time'] if i > 1 else response['time'],
            time1=response['time'],
            learned=learner['learned'],
            belief=learner['belief'],
        )

        # compute_guess - before learned
        row_stats['guess'] = card['guess'] = compute_guess(
            score=response['score'],
            learned=learner['learned'],
            guess=card['guess'],
        )

        # compute_slip - before learned
        row_stats['slip'] = card['slip'] = compute_slip(
            score=response['score'],
            learned=learner['learned'],
            slip=card['slip'],
        )

        # ### compute_learned  ###
        row_stats['learned'] = learner['learned'] = compute_learned(
            score=response['score'],
            learned=learner['learned'],
            guess=card['guess'],
            slip=card['slip'],
            transit=card['transit'],
        )

        # compute_transit - after learned
        if i > 3:
            prev_card = cards[rows[i - 3]['card']]
            row_stats['transit'] = prev_card['transit'] = compute_transit(
                transit=prev_card['transit'],
                learned0=rows[i - 3]['learned'],
                learned3=learner['learned'],
            )

        # TODO: compute_set_learned - after learned
        # TODO: compute_unit_quality - after learned
        # TODO: compute_set_quality - after unit quality

        rows.append(row_stats)
        print(row_stats)

        if learner['learned'] > 0.95 and learner['belief'] > 0.95:
            break

    return rows


def compute_correct(learned=init_learned, guess=init_guess, slip=init_slip):
    """
    Determines how likely the learner will respond to a card well.
    """
    return learned * (1 - slip) + (1 - learned) * guess


def compute_belief(time0, time1, learned=init_learned, belief=init_belief):
    """
    Determines how likely we believe in `learned`, given the time since the
    last response.
    """
    strength = 2 * learned * belief / (learned + belief)
    # Intentionally `time0 - time1`, as this produces a negative number.
    return exp(belief_k * (time0 - time1) / strength)


def compute_guess(score, learned=init_learned, guess=init_guess):
    """
    Determines how to update guess, given a score.
    Based on the following observation:
    - P(Answer is a Guess | Correct) = 1 - P(Learned)

    TODO: Alternatively, make use of `belief`.
    """
    guess += score * ((max_guess - guess) * (1 - learned)) ** 2
    guess -= (1 - score) * (guess * (1 - learned)) ** 2
    return guess


def compute_slip(score, learned=init_learned, slip=init_slip):
    """
    Determines how to update slip, given a score.
    Based on the following observation:
    - P(Answer is a Slip | Incorrect) = P(Learned)

    TODO: Alternatively, make use of `belief`.
    """
    slip -= score * (slip * learned) ** 2
    slip += (1 - score) * ((max_slip - slip) * learned) ** 2
    return slip


def compute_learned(score, learned=init_learned, guess=init_guess,
                    slip=init_slip, transit=init_transit):
    """
    Given a learner response,
    determines how likely the learner knows the skill.
    TODO: Alternatively, this computation can also make use of `belief`.
    """
    positive = (learned * (1 - slip)
                / (learned * (1 - slip) + (1 - learned) * guess))
    negative = (learned * slip
                / (learned * slip + (1 - learned) * (1 - guess)))
    posterior = score * positive + (1 - score) * negative
    return posterior + (1 - posterior) * transit


def compute_transit(transit, learned0, learned3):
    """
    Determines the update to transit, given the `learned` score
    before the card, and the `learned` score after two additional cards.
    Note that transit is both on assessment and non-assessment cards.

    (l0) A (l1) B (l2) C (l3)

    TODO: Alternatively, make use of `belief`.
    """
    delta = learned3 / learned0 - 1
    sign = 1 if delta > 0 else -1
    return transit + sign * min((transit * delta) ** 2, 0.01)


def compute_set_learned(units):
    """
    Given a list of units, compute the overall ability.
    """
    return fsum(unit.learned for unit in units) / len(units)


def compute_unit_quality(learners_units):
    """
    Given a list of learners x units, determine the quality of the unit.

    TODO: Factor in number of learners.
    """
    if learners_units < 100:
        return 0
    return fsum(lu.learned for lu in learners_units) / len(learners_units)


def compute_set_quality(units):
    """
    Given a list of units, compute the set quality.
    """
    return fsum(unit.quality for unit in units) / len(units)

if __name__ == '__main__':
    main()
