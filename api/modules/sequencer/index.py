"""
Primary learning sequencer.
"""

from modules.sequencer.formulas import update as formula_update
from modules.sequencer.params import init_learned
from models.response import Response
from time import time

"""
Card
- [x] correct
- [x] guess
- [x] slip
- [_] transit  TODO@

Unit
- [x] learned
- [x] belief
- [ ] unit quality  TODO@
- [ ] unit difficulty  TODO@

Set
- [ ] learner-set ability  TODO@
- [ ] set quality  TODO@
- [ ] set difficulty  TODO@
"""


def update(user, card, response):
    """
    Update the card's parameters (and its parents')
    when given a response.
    """

    # TODO split up into smaller methods

    errors = card.validate_response(response)
    if errors:
        return {'errors': errors}

    score, feedback = card.score_response(response)
    response = Response({
        'user_id': user['id'],
        'card_id': card['id'],
        'unit_id': card['unit_id'],
        'response': response,
        'score': score,
    })
    # errors = response.validate()
    # if errors:
    #     return {'errors': errors, 'feedback': feedback}

    card_parameters = card.fetch_parameters()
    previous_response = Response.get_latest(user_id=user['id'],
                                            unit_id=card['unit_id'])

    now = time()
    time_delta = now - (previous_response['created'].to_epoch_time()
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
