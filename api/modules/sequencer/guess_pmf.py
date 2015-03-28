from modules.sequencer.pmf import PMF
from modules.sequencer.formulas import calculate_correct, calculate_incorrect


class GuessPMF(PMF):
    def likelihood(self, data, hypothesis):
        score, learned, slip = \
            data['score'], data['learned'], data['slip']
        return (score
                * calculate_correct(hypothesis, slip, learned)
                + (1 - score)
                * calculate_incorrect(hypothesis, slip, learned))
