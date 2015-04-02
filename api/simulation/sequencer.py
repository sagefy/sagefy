"""
This document combines the formulas and the mock data, providing for
'how good' the formulas actually are.
"""

import os
import sys
import inspect
currentdir = os.path.dirname(
    os.path.abspath(
        inspect.getfile(
            inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from mock import main as create_responses
from modules.sequencer.formulas import update
from modules.sequencer.guess_pmf import GuessPMF
from modules.sequencer.slip_pmf import SlipPMF
from modules.sequencer.params import init_learned, init_guess, \
    init_slip, init_transit
from math import sqrt


def get_learner(name, my_learners):
    return my_learners[name]


def get_card(name, my_cards):
    return my_cards[name]


def main(num_learners=1000, num_cards=50):
    d = create_responses(num_learners, num_cards)
    responses, learners, cards = d['responses'], d['learners'], d['cards']

    precision = 20

    my_cards = [{
        'name': card['name'],
        'guess_distro': GuessPMF({
            h: 1 - (init_guess - h) ** 2
            for h in [h / precision for h in range(1, precision)]}),
        'slip_distro': SlipPMF({
            h:  1 - (init_slip - h) ** 2
            for h in [h / precision for h in range(1, precision)]}),
        'transit': init_transit,
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
            prev_response = {
                'time': response['time'],
                'prev_learned': init_learned,
            }

        my_learner = get_learner(response['learner'], my_learners)
        my_card = get_card(response['card'], my_cards)

        response['prev_learned'] = my_learner['learned']

        c = update(learned=my_learner['learned'],
                   guess_distro=my_card['guess_distro'],
                   slip_distro=my_card['slip_distro'],
                   score=response['score'],
                   time=response['time'],
                   prev_time=prev_response['time'])

        my_learner['learned'] = c['learned']
        my_card['guess_distro'] = c['guess_distro']
        my_card['slip_distro'] = c['slip_distro']

        latest_response_per_learner[response['learner']] = response

    # Compute the error rates.
    # Error should sqrt(sum( (o - x)^2 for o in list ))
    guess_error, slip_error, transit_error = 0, 0, 0

    for card in cards:
        my_card = get_card(card['name'], my_cards)
        my_card['guess'] = my_card['guess_distro'].get_value()
        my_card['slip'] = my_card['slip_distro'].get_value()
        guess_error += (my_card['guess'] - card['guess']) ** 2
        slip_error += (my_card['slip'] - card['slip']) ** 2
        transit_error += (my_card['transit'] - card['transit']) ** 2

    print('guess_error', sqrt(guess_error / len(my_cards)))
    print('slip_error', sqrt(slip_error / len(my_cards)))
    print('transit_error', sqrt(transit_error / len(my_cards)))

    guess_error, slip_error, transit_error = 0, 0, 0

    for card in cards:
        guess_error += (init_guess - card['guess']) ** 2
        slip_error += (init_slip - card['slip']) ** 2
        transit_error += (init_transit - card['transit']) ** 2

    print('CONTROL guess_error', sqrt(guess_error / len(my_cards)))
    print('CONTROL slip_error', sqrt(slip_error / len(my_cards)))
    print('CONTROL transit_error', sqrt(transit_error / len(my_cards)))

if __name__ == '__main__':
    main()
