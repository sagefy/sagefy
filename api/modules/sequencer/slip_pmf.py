from modules.sequencer.pmf import PMF
from modules.sequencer.formulas import calculate_correct, calculate_incorrect


class SlipPMF(PMF):
    def likelihood(self, data, hypothesis):
        score, learned, guess = \
            data['score'], data['learned'], data['guess']
        return (score
                * calculate_correct(guess, hypothesis, learned)
                + (1 - score)
                * calculate_incorrect(guess, hypothesis, learned))
