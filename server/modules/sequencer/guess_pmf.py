from modules.sequencer.pmf import PMF
from modules.sequencer.formulas import calculate_correct, calculate_incorrect
from modules.sequencer.params import adjust_guess


class GuessPMF(PMF):
    def likelihood(self, data, hypothesis):
        """
        Given new data and one of the guess hypotheses,
        update the probability of that hypothesis.
        """

        score, learned, slip = \
            data['score'], data['learned'], data['slip']
        return (score
                * calculate_correct(hypothesis, slip, learned)
                + (1 - score)
                * calculate_incorrect(hypothesis, slip, learned))

    def get_value(self):
        """
        The PMF tends to overestimate guess,
        even though correlation is decent,
        so let's trim it down a bit.
        TODO-3 Why does this PMF overestimate guess?
        """

        return super().get_value() * adjust_guess
