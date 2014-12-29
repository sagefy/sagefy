"""
TODO Description of this file.

Given we can reliably compute `correct` and `learned`, the other calculations
should be formulated as follows:

0) [ ] Ensure each function works as expected.

1) [ ] Using the given `transit`, find formulations of `guess` and `slip` so
    that the error rate is trivially small after
    a sufficient number of examples.
    The error rate should ideally be near or less than 0.01.

2) [ ] Once `guess` and `slip` are established, find a formulation for transit.
    Ideally, it's error rate should be less than 0.01.

3) [ ] Describe how `belief` should act in a variety of scenarios. Find a
    formula that meets these scenarios, and compute the error versus the
    expected results.

4) [ ] Only after the other primary attributes are reliably compute-able,
    compute sufficient attributes to support learner search.
"""


from mock import main as create_responses
from formulae import update, init_learned, init_belief, \
    init_guess, init_slip  # , init_transit
from math import sqrt


def main(num_learners=250, num_cards=10):
    d = create_responses(num_learners, num_cards)
    responses, learners, cards = d['responses'], d['learners'], d['cards']

    my_cards = [{
        'name': card['name'],
        'guess': init_guess,
        'slip': init_slip,
        'transit': card['transit'],  # TODO instead use init_transit,
    } for card in cards]

    my_learners = [{
        'name': learner['name'],
        'learned': init_learned,
        'belief': init_belief,
    } for learner in learners]

    for i, response in enumerate(responses):
        # response keys: learner, card, time, score

        prev_response = get_previous_response(responses, i)

        # TODO create functions, ensure they work as expected
        my_learner = [ml for ml in my_learners
                      if ml['name'] == response['learner']][0]
        my_card = [mc for mc in my_cards
                   if mc['name'] == response['card']][0]

        c = update(learned=my_learner['learned'],
                   belief=my_learner['belief'],
                   guess=my_card['guess'],
                   slip=my_card['slip'],
                   transit=my_card['transit'],
                   score=response['score'],
                   time=response['time'],
                   prev_time=prev_response['time'],
                   prev_learned=0,  # TODO
                   prev_transit=0)  # TODO

        my_learner['learned'] = c['learned']
        my_learner['belief'] = c['belief']
        my_card['guess'] = c['guess']
        my_card['slip'] = c['slip']
        # TODO my_card['transit'] = c['transit']

    # Compute the error rates.
    # Error should sqrt(sum( (o - x)^2 for o in list ))
    guess_error, slip_error = 0, 0
    for mc in my_cards:
        card = [card for card in cards if card['name'] == mc['name']][0]

        guess_error += (my_card['guess'] - card['guess']) ** 2
        slip_error += (my_card['slip'] - card['slip']) ** 2
        # TODO transit_error +=
        # TODO belief_error +=

    print('guess_error', sqrt(guess_error / len(my_cards)))
    print('slip_error', sqrt(slip_error / len(my_cards)))
    # TODO print('transit_error')
    # TODO print('belief_error')


def get_previous_response(responses, i):
    # TODO test this making sure it works as expected
    learner = responses[i]['learner']
    while True:
        i -= 1
        if i < 0:
            return {'time': None}
        if responses[i]['learner'] == learner:
            return responses[i]


if __name__ == '__main__':
    main()
