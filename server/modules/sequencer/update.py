from modules.sequencer.params import init_transit
from modules.sequencer.pmf import update_pmf, \
  get_guess_pmf_value, get_guess_pmf_likelihood, \
  get_slip_pmf_value, get_slip_pmf_likelihood
from modules.sequencer.formulas import update_learned


def update(score, time_delta, learned,
           guess_distribution, slip_distribution):
  """
  Given a learner and a card, update both statistics.

  Input:

  - Score - What what the score (0 - wrong or 1 - correct)?
  - Time - When did the score come in (in seconds)?
  - Prev Time [Previous Card] - When was the last time we saw
    a learner response for this skill?
  - * * *
  - Learned [Learner] - Before seeing the response, how likely did we already
    believe the learner knew the skill?
  - Guess [Card] - Before the response, how likely would a learner who
    didn't know the skill still get the right answer?
  - Slip [Card] - Before the response, how likely woud a learner who
    did know the skill still get a wrong answer?
  - Weight [Card] - How much should we consider previous examples?
  - Transit [Card] - Before seeing the data,
    how likely did we think the learner would learn the skill by seeing
    the card?

  Output:

  - Correct - Before seeing the score, how likely was the learner
    to answer the card well?
    (doesn't update anything)
  - Learned [Learner] - How likely is it that the learner knows the skill?
    (main calculation)
  - Guess [Card] - If the learner doesn't know the skill, how likely are they
    to get the answer right anyways?
    (should come before learned)
  - Slip [Card] - If the learner knows the skill,
    how likely are they to still answer incorrectly?
    (should come before learned)
  - Weight [Card] - How much should we consider previous examples?
    (scale before guess, slip, transit, update after)
  - Transit [Card (Prior)] - How likely is it the learner
    learned the skill as the result of seeing that card?
    (after learned)
  """

  guess = get_guess_pmf_value(guess_distribution)
  slip = get_slip_pmf_value(slip_distribution)
  transit = init_transit

  learned2 = update_learned(score, learned,
                            guess, slip, transit,
                            time_delta)
  guess_distribution = update_pmf(guess_distribution, {
    'score': score,
    'learned': learned,
    'guess': guess,
    'slip': slip,
  }, get_guess_pmf_likelihood)
  slip_distribution = update_pmf(slip_distribution, {
    'score': score,
    'learned': learned,
    'guess': guess,
    'slip': slip,
  }, get_slip_pmf_likelihood)

  return {
    'learned': learned2,
    'guess_distribution': guess_distribution,
    'slip_distribution': slip_distribution,
  }
