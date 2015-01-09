"""
This document combines the formulas and the mock data, providing for
'how good' the formulas actually are.
"""


from mock import main as create_responses
from formulas import update, init_learned, \
    init_weight, init_guess, init_slip, init_transit
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
        'transit': init_transit,
        'transit_weight': init_weight,
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
            prev_card = get_card(prev_response['card'], my_cards)
        else:
            prev_response = {
                'time': response['time'],
                'prev_learned': init_learned,
            }
            prev_card = {
                'transit': init_transit,
                'transit_weight': init_weight,
            }

        my_learner = get_learner(response['learner'], my_learners)
        my_card = get_card(response['card'], my_cards)

        response['prev_learned'] = my_learner['learned']

        c = update(learned=my_learner['learned'],
                   guess=my_card['guess'],
                   guess_weight=my_card['guess_weight'],
                   slip=my_card['slip'],
                   slip_weight=my_card['slip_weight'],
                   transit=my_card['transit'],
                   score=response['score'],
                   time=response['time'],
                   prev_time=prev_response['time'],
                   prev_transit=prev_card['transit'],
                   prev_transit_weight=prev_card['transit_weight'],
                   prev_card_pre_learned=prev_response['prev_learned'])

        my_learner['learned'] = c['learned']
        my_card['guess'] = c['guess']
        my_card['guess_weight'] = c['guess_weight']
        my_card['slip'] = c['slip']
        my_card['slip_weight'] = c['slip_weight']
        prev_card['transit'] = c['prev_transit']
        prev_card['transit_weight'] = c['prev_transit_weight']

        latest_response_per_learner[response['learner']] = response

    # Compute the error rates.
    # Error should sqrt(sum( (o - x)^2 for o in list ))
    guess_error, slip_error, transit_error = 0, 0, 0

    for card in cards:
        my_card = get_card(card['name'], my_cards)
        guess_error += (my_card['guess'] - card['guess']) ** 2
        slip_error += (my_card['slip'] - card['slip']) ** 2
        transit_error += (my_card['transit'] - card['transit']) ** 2

        print('%.2f %.2f %.2f %.2f %.2f %.2f' % (
            my_card['guess'], card['guess'], my_card['slip'], card['slip'],
            my_card['transit'], card['transit']))

    print('guess_error', sqrt(guess_error / len(my_cards)))
    print('slip_error', sqrt(slip_error / len(my_cards)))
    print('transit_error', sqrt(transit_error / len(my_cards)))


if __name__ == '__main__':
    main()
