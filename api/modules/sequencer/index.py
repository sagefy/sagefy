"""
Primary learning sequencer.
"""

from modules.sequencer.formulas import update as formula_update
from modules.sequencer.params import init_learned
from models.response import Response
from modules.sequencer.traversal import traverse
from time import time


def next(user, context):
    """
    Returns what should be displayed next.
    Also should return `learned` progress.
    Should return in format:
    {
        'path': '/api/path',
        'method': 'GET',
        'learned': 0.89,
    } or empty dictionary.
    """

    # TODO@ leverage `state` in context for easier logic

    # [ ] set  [ ] unit  [ ] card
    # Direct the learner to my sets page.
    if 'set' not in context:
        return {
            'method': 'GET',
            'path': '/api/users/{user_id}/sets'
                    .format(user_id=user['id']),
        }

    # [x] set  [ ] unit  [ ] card
    if 'unit' not in context:
        mode, units = traverse(user, context)
        # If need diagnosis, auto choose the unit and mode.
        # Return learner to the tree.
        if mode == 'diagnose':
            user.set_learning_context(state='diagnose', unit=units[0])
            return {
                'method': 'GET',
                'path': '/api/sets/{set_id}/tree'
                        .format(set_id=context['set']['id'])
            }
        # If state requests choose unit,
        # Direct to that page.
        if context['state'] == 'choose_unit':
            return {
                'method': 'GET',
                'path': '/api/sets/{set_id}/units'
                        .format(set_id=context['set']['id'])
            }
        # If ready to learn, show tree for now,
        # But later direct to choose units.
        if mode == 'learn':
            user.set_learning_context(state='diagnose')
            return {
                'method': 'GET',
                'path': '/api/sets/{set_id}/tree'
                        .format(set_id=context['set']['id'])
            }

    # [x] set  [x] unit  [ ] card
    if 'card' not in context:
        # If sufficient progress or time has passed,
        # clear the unit and go back to tree.
        if sufficient_progress(context):
            user.set_learning_context(unit=None)
            return {
                'method': 'GET',
                'path': '/api/sets/{set_id}/tree'
                        .format(set_id=context['set']['id'])
            }
        # Otherwise, choose a card. ...and include `learned`.
        else:
            next_card = choose_next_card(context)
            return {
                'method': 'GET',
                'path': '/api/cards/{card_id}/learn'
                        .format(card_id=next_card['id'])
                # TODO@ add `learned`
            }

    # [x] set  [x] unit  [x] card
    # Direct the learner to respond to the card.
    return {
        'method': 'POST',
        'path': '/api/cards/{card_id}/responses'
                .format(card_id=context['card']['id']),
        # TODO@ add `learned`
    }


def sufficient_progress(context):
    """

    """

    return False


def choose_next_card(context):
    """

    """

    return False


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
    errors = response.validate()
    if errors:
        return {'errors': errors, 'feedback': feedback}

    card_parameters = card.fetch_parameters()
    previous_response = Response.get_latest(user_id=user['id'],
                                            unit_id=card['unit_id'])

    now = time()
    time_delta = now - (previous_response['created'].to_epoch_time()
                        if previous_response else now)

    learned = (previous_response['learner']
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
