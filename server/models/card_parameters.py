from modules.model import Model
from modules.validations import is_required, is_string, is_dict
from modules.sequencer.guess_pmf import GuessPMF
from modules.sequencer.slip_pmf import SlipPMF
from modules.sequencer.params import init_guess, init_slip, precision


class CardParameters(Model):
    tablename = 'cards_parameters'

    schema = dict(Model.schema.copy(), **{
        'entity_id': {
            'validate': (is_required, is_string),  # TODO@ validate foreign
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

        """

    def get_slip(self):
        """

        """

    def get_transit(self):
        """

        """

    def get_num_learners(self):
        """

        """
