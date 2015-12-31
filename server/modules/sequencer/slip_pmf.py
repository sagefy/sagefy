from modules.sequencer.pmf import PMF
from modules.sequencer.formulas import calculate_correct, calculate_incorrect
from modules.sequencer.params import adjust_slip


class SlipPMF(PMF):
    def likelihood(self, data, hypothesis):
        """
        Given new data and one of the slip hypotheses,
        update the probability of that hypothesis.
        """

        score, learned, guess = \
            data['score'], data['learned'], data['guess']
        return (score
                * calculate_correct(guess, hypothesis, learned)
                + (1 - score)
                * calculate_incorrect(guess, hypothesis, learned))

    def get_value(self):
        """
        The PMF tends to overestimate guess,
        even though correlation is decent,
        so let's trim it down a bit.
        TODO-3 Why does this PMF overestimate slip?
        """

        return super().get_value() * adjust_slip
