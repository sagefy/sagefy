"""
Primary learning sequencer.
"""

from database.card_parameters import get_card_parameters, get_distribution, \
    bundle_distribution, insert_card_parameters, update_card_parameters
from modules.sequencer.update import update as formula_update
from modules.sequencer.params import init_learned
from database.response import get_latest_response, insert_response
from time import time
from schemas.card import assessment_kinds

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

Subject
- [ ] learner-subject ability  TODO-3
- [ ] subject quality  TODO-3
- [ ] subject difficulty  TODO-3
"""


def update(db_conn, user, card, response):
    """
    Update the card's parameters (and its parents')
    when given a response.
    """

    # TODO-3 split up into smaller methods

    if card['kind'] not in assessment_kinds:
        return {
            'response': {},
            'feedback': '',
        }

    errors = card.validate_response(response)  # MMM
    if errors:
        return {'errors': errors}

    score, feedback = card.score_response(response)  # MMM
    response = {
        'user_id': user['id'],
        'card_id': card['entity_id'],
        'unit_id': card['unit_id'],
        'response': response,
        'score': score,
    }

    card_parameters = get_card_parameters(
        {'entity_id': card['entity_id']},
        db_conn
    ) or {}
    previous_response = get_latest_response(user['id'],
                                            card['unit_id'],
                                            db_conn)

    now = time()
    time_delta = now - (int(previous_response['created'].strftime("%s"))
                        if previous_response else now)

    learned = (previous_response['learned']
               if previous_response else init_learned)
    guess_distribution = get_distribution(card_parameters, 'guess')
    slip_distribution = get_distribution(card_parameters, 'slip')

    updates = formula_update(score, time_delta,
                             learned, guess_distribution, slip_distribution)

    response['learned'] = updates['learned']
    response, errors = insert_response(response, db_conn)
    if errors:
        return {'errors': errors, 'feedback': feedback}

    updated_card_parameters = {
        'entity_id': card['entity_id'],
        'guess_distribution':
            bundle_distribution(updates['guess_distribution']),
        'slip_distribution':
            bundle_distribution(updates['slip_distribution']),
    }
    if card_parameters.get('id'):
        _, errors = update_card_parameters(
            card_parameters,
            updated_card_parameters,
            db_conn
        )
    else:
        _, errors = insert_card_parameters(
            updated_card_parameters,
            db_conn
        )

    if errors:
        return {'errors': errors, 'feedback': feedback}

    return {'response': response, 'feedback': feedback}
