from modules.model import Model
from modules.validations import is_required, is_string, is_dict
from modules.sequencer.guess_pmf import GuessPMF
from modules.sequencer.slip_pmf import SlipPMF
from modules.sequencer.params import init_guess, init_slip, precision, \
    init_transit


class CardParameters(Model):
    tablename = 'cards_parameters'

    schema = dict(Model.schema.copy(), **{
        'entity_id': {  # TODO-3 validate foreign
            'validate': (is_required, is_string),
        },
        'guess_distribution': {
            'validate': (is_required, is_dict,),
        },
        'slip_distribution': {
            'validate': (is_required, is_dict,),
        },
    })

    def get_distribution(self, kind):
        """
        Parse own distribution hypotheses,
        changing the keys back into numbers.
        """

        key = '{kind}_distribution'.format(kind=kind)
        if key in self:
            distribution = self[key]
            distribution = {float(k): v for k, v in distribution.items()}
        else:
            init = init_guess if kind == 'guess' else init_slip
            distribution = {
                h: 1 - (init - h) ** 2
                for h in [h / precision for h in range(1, precision)]
            }
            self[key] = distribution
        if kind == 'guess':
            return GuessPMF(distribution)
        if kind == 'slip':
            return SlipPMF(distribution)

    def set_distribution(self, kind, distribution):
        """
        Given the kind and the distribution,
        prepare for saving the distribution to the database.
        """

        key = '{kind}_distribution'.format(kind=kind)
        self[key] = {str(k): v for k, v in distribution.hypotheses.items()}
        return self

    def get_guess(self):
        """
        Gets the guess value for the card.
        """

        guess_distribution = self.get_distribution('guess')
        return guess_distribution.get_value()

    def get_slip(self):
        """
        Gets the slip value for the card.
        """

        slip_distribution = self.get_distribution('slip')
        return slip_distribution.get_value()

    def get_transit(self):
        """
        Gets the transit value for the card.
        TODO-2 use a formulation for transit.
        """

        return init_transit

    def get_num_learners(self):
        """
        Gets the number of learners who interact with the card.
        TODO-3 calculate based on the responses table.
        """

        return 0

    def get_values(self):
        """
        Get the value outputs for the card parameters.
        """

        return {
            'guess': self.get_guess(),
            'slip': self.get_slip(),
            'transit': self.get_transit(),
            'num_learners': self.get_num_learners(),
        }
