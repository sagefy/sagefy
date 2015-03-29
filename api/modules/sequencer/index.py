"""
Primary learning sequencer.
"""


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
