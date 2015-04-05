"""
TODO How to write a PMF for `transit`.
Perhaps someone more savvy than me can figure it out.

What I do know is:

    transit = (learned_post - learned_pre) / (1 - learned_pre)
"""

from modules.sequencer.pmf import PMF


class TransitPMF(PMF):
    def likelihood(self, data, hypothesis):
        """
        Given new data and one of the transit hypotheses,
        update the probability of that hypothesis.
        """

        raise Exception("No method implemented.")
