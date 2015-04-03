"""
Primary learning sequencer.
"""

from modules.sequencer.formulas import update as formula_update


def main(user_id, context):
    """
    TODO@ Returns what should be displayed next.
    TODO@ Also should return progress.
    Should return in format:
    {
        'path': '/api/path/',
        'method': 'GET',
        'learned': 0.89,
    } or empty dictionary.
    """

    # [ ] set  [ ] unit  [ ] card
    # Direct the learner to my sets page.
    if 'set' not in context:
        return {
            'path': '/api/users/{user_id}/sets/'.format(user_id=user_id),
            'method': 'GET',
        }

    # [x] set  [ ] unit  [ ] card
    # TODO@ If the learner hasn't seen the tree, show the tree.
    # TODO@ If need diagnosis, auto choose the unit and mode.
    # TODO@ Else, go to choose unit.

    # [x] set  [x] unit  [ ] card
    # TODO@ If the unit still needs work, choose a card.
    # TODO@ Otherwise, clear the unit and go back to tree.

    # [x] set  [x] unit  [x] card
    # TODO@ Direct the learner to respond to the card.

    return {}


def update(card, response):
    """
    Update the card's parameters (and its parents')
    when given a response.
    """

    card_parameters = card.fetch_parameters()
    # TODO@ get previous response, if available

    score = response['score']
    time = response['created']
    previous_time = None
    learned = None
    guess_distribution = card_parameters.get_distribution('guess')
    slip_distribution = card_parameters.get_distribution('slip')

    # updates = formula_update(score, time, previous_time,
    #                          learned, guess_distribution, slip_distribution)

    # response, errors = response.update({'learned': updates['learned']})
    # if errors:
    #      return learned, errors
    # card_parameters.set_distribution('guess', updates['guess_distribution'])
    # card_parameters.set_distribution('slip', updates['slip_distribution'])
    # card_parameters, errors = card_parameters.save()
    # if errors:
    #      return updates['learned'], errors

    return learned, []
    # return updates['learned'], []
