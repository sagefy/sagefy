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
from formulae import update, init_learned, \
    init_weight, init_guess, init_slip  # init_belief, init_transit
from math import sqrt


def get_learner(name, my_learners):
    return my_learners[name]


def get_card(name, my_cards):
    return my_cards[name]


def main(num_learners=1000, num_cards=50):
    d = create_responses(num_learners, num_cards)
    responses, learners, cards = d['responses'], d['learners'], d['cards']

    my_cards = [{
        'name': card['name'],
        'guess': init_guess,
        'guess_weight': init_weight,
        'slip': init_slip,
        'slip_weight': init_weight,
        'transit': card['transit'],  # TODO instead use init_transit,
    } for card in cards]

    my_learners = [{
        'name': learner['name'],
        'learned': init_learned,
    } for learner in learners]

    latest_response_per_learner = {}

    for i, response in enumerate(responses):
        # response keys: learner, card, time, score

        if response['learner'] in latest_response_per_learner:
            prev_response = latest_response_per_learner[response['learner']]
        else:
            prev_response = {'time': 0}

        my_learner = get_learner(response['learner'], my_learners)
        my_card = get_card(response['card'], my_cards)

        c = update(learned=my_learner['learned'],
                   guess=my_card['guess'],
                   guess_weight=my_card['guess_weight'],
                   slip=my_card['slip'],
                   slip_weight=my_card['slip_weight'],
                   transit=my_card['transit'],
                   score=response['score'],
                   time=response['time'],
                   prev_time=prev_response['time'])

        my_learner['learned'] = c['learned']
        my_card['guess'] = c['guess']
        my_card['guess_weight'] = c['guess_weight']
        my_card['slip'] = c['slip']
        my_card['slip_weight'] = c['slip_weight']

        latest_response_per_learner[response['learner']] = response

    # Compute the error rates.
    # Error should sqrt(sum( (o - x)^2 for o in list ))
    guess_error, slip_error = 0, 0

    for card in cards:
        my_card = get_card(card['name'], my_cards)
        guess_error += (my_card['guess'] - card['guess']) ** 2
        slip_error += (my_card['slip'] - card['slip']) ** 2
        print('%.2f %.2f %.2f %.2f' % (
            my_card['guess'], card['guess'], my_card['slip'], card['slip']))
        # TODO transit_error += (my_card['transit'] - card['transit']) ** 2

    print('guess_error', sqrt(guess_error / len(my_cards)))
    print('slip_error', sqrt(slip_error / len(my_cards)))
    # TODO print('transit_error')


if __name__ == '__main__':
    main()
