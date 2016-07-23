from models.card import Card
from models.card_parameters import CardParameters
from modules.sequencer.formulas import calculate_correct
from modules.sequencer.params import init_learned
from random import shuffle, random
from math import floor
from functools import reduce
from models.response import Response


p_assessment_map = {
    0: 0.7,
    1: 0.7,
    2: 0.7,
    3: 0.7,
    4: 0.7,
    5: 0.7,
    6: 0.8,
    7: 0.9,
    8: 0.95,
    9: 1,
    10: 1,
}


def partition(l, p):
    return reduce(lambda x, y: x[not p(y)].append(y) or x, l, ([], []))


def choose_card(db_conn, user, unit):
    """
    Given a user and a unit, choose an appropriate card.
    Return a card instance.
    """

    # TODO-3 simplify this method

    unit_id = unit['entity_id']
    query = (Card.start_accepted_query()
                 .filter({'unit_id': unit_id})
                 .sample(10))  # TODO-2 index
    # TODO-3 does this belong as a model method?
    # TODO-2 is the sample value decent?
    # TODO-2 has the learner seen this card recently?

    cards = [Card(d) for d in query.run(db_conn)]
    if not len(cards):
        return None

    previous_response = Response.get_latest(db_conn,
                                            user_id=user['id'],
                                            unit_id=unit_id)
    if previous_response:
        learned = previous_response['learned']
        # Don't allow the previous card as the next card
        cards = [
            card
            for card in cards
            if card['entity_id'] != previous_response['card_id']
        ]
    else:
        learned = init_learned

    shuffle(cards)
    assessment, nonassessment = partition(cards, lambda c: c.has_assessment())
    choose_assessment = random() < p_assessment_map[floor(learned * 10)]

    if choose_assessment:
        if not len(assessment):
            return nonassessment[0]
        for card in assessment:
            params = CardParameters.get(db_conn, entity_id=card['entity_id'])
            if params:
                guess = params.get_distribution('guess').get_value()
                slip = params.get_distribution('slip').get_value()
                correct = calculate_correct(guess, slip, learned)
                if 0.25 < correct < 0.75:
                    return card
            else:
                return card
        return assessment[0]

    if len(nonassessment):
        return nonassessment[0]

    if len(assessment):
        return assessment[0]

    return None
