
"""
PMF, or Probability Mass Function.
"""

import operator


class PMF(object):

    def __init__(self, hypotheses=[]):
        """
        Create a new PMF, given a list of hypotheses.
        Internally, hypotheses is a dict of hypo: probability.
        """

        self.hypotheses = {hypothesis: 1 for hypothesis in hypotheses}
        self.normalize()

    def update(self, data):
        """
        Main update function. Updates each hypothesis based on the
        data provided.
        """
        self.hypotheses = {hypothesis:
                           probability * self.likelihood(data, hypothesis)
                           for hypothesis, probability
                           in self.hypotheses.items()}
        self.normalize()

    def likelihood(self, data, hypothesis):
        """
        What is the likelihood of getting this data, given the
        particular hypothesis?
        **This is function should be overwritten.**
        """

        pass

    def normalize(self):
        """
        Make sure that all hypotheses sum up to 1.
        """

        total = sum(probability
                    for hypothesis, probability
                    in self.hypotheses.items())
        self.hypotheses = {hypothesis:
                           probability / total
                           for hypothesis, probability
                           in self.hypotheses.items()}

    def get_mean(self):
        """
        Find the hypothesis that splits the distribution in half.
        """

        at = 0
        for hypothesis in sorted(self.hypotheses.keys()):
            at += self.hypotheses[hypothesis]
            if at >= 0.5:
                return hypothesis

    def get_mode(self):
        """
        Find the hypotheses with the highest probability.
        """

        return max(self.hypotheses.items(), key=operator.itemgetter(1))[0]
