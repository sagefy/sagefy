"""
Primary learning sequencer.
"""

from models.card_parameters import CardParameters
from modules.sequencer.formulas import update as formula_update
from modules.sequencer.params import init_learned
from models.response import Response
from time import time

"""
Card
- [x] correct
- [x] guess
- [x] slip
- [_] transit  TODO-3

Unit
- [x] learned
- [x] belief
- [ ] unit quality  TODO-3
- [ ] unit difficulty  TODO-3

Set
- [ ] learner-set ability  TODO-3
- [ ] set quality  TODO-3
- [ ] set difficulty  TODO-3
"""


def update(user, card, response):
    """
    Update the card's parameters (and its parents')
    when given a response.
    """

    # TODO-3 split up into smaller methods

    if not card.has_assessment():
        return {
            'response': Response({}),
            'feedback': '',
        }

    errors = card.validate_response(response)
    if errors:
        return {'errors': errors}

    score, feedback = card.score_response(response)
    response = Response({
        'user_id': user['id'],
        'card_id': card['entity_id'],
        'unit_id': card['unit_id'],
        'response': response,
        'score': score,
    })

    card_parameters = CardParameters.get(entity_id=card['entity_id'])
    previous_response = Response.get_latest(user_id=user['id'],
                                            unit_id=card['unit_id'])

    now = time()
    time_delta = now - (int(previous_response['created'].strftime("%s"))
                        if previous_response else now)

    learned = (previous_response['learned']
               if previous_response else init_learned)
    guess_distribution = card_parameters.get_distribution('guess')
    slip_distribution = card_parameters.get_distribution('slip')

    updates = formula_update(score, time_delta,
                             learned, guess_distribution, slip_distribution)

    response['learned'] = updates['learned']
    response, errors = response.save()
    if errors:
        return {'errors': errors, 'feedback': feedback}

    card_parameters.set_distribution('guess', updates['guess_distribution'])
    card_parameters.set_distribution('slip', updates['slip_distribution'])
    card_parameters, errors = card_parameters.save()
    if errors:
        return {'errors': errors, 'feedback': feedback}

    return {'response': response, 'feedback': feedback}
