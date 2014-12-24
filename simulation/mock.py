"""
Simulates learner responses for a unit. Can be used for prototyping and testing
learner models.
"""

from random import uniform, sample, randrange

# How many seconds between questions
question_gap = (5, 60)

# How many seconds between sessions
session_gap = (60 * 60 * 12, 60 * 60 * 36)

# How many questions per session
max_questions = (10, 20)

# Typical ranges for parameters we will be estimating later
guess = (0.01, 0.4)
slip = (0.01, 0.2)
transit = (0.01, 0.05)

# When to end the responses per learner
max_learned = 0.99
degrade = 0.2


def main(num_learners=1, num_cards=10):
    """
    Primary function. Given a number of learners and number of available cards,
    simulates responses for a hypothetical unit.

    Returns responses in an list, with the following attributes:
    learner, card, time, score
    """

    cards = create_cards(num_cards)
    return {
        'responses': create_responses(num_learners, cards),
        'cards': cards,
    }


def create_cards(num_cards):
    """
    Produces random set of cards with underlying values for
    guess, slip, and transit.
    """

    return [{
        'name': str(chr(65 + i)),
        'guess': uniform(*guess),
        'slip': uniform(*slip),
        'transit': uniform(*transit),
    } for i in range(num_cards)]


def create_responses(num_learners, cards):
    """
    Generates a set of responses based on a set of cards
    and number of learners.
    """

    start_time = 1
    responses = []

    for i in range(num_learners):
        learner = str(chr(65 + i))
        responses += create_responses_as_learner(learner, start_time, cards)
        start_time += int(uniform(*session_gap))

    responses = sorted(responses, key=lambda d: d['time'])
    return responses


def create_responses_as_learner(learner, start_time, cards):
    """
    Creates a set of simulated responses for a learner.
    """

    learned = 0
    count = 0
    cards_seen = []
    responses = []
    time = start_time
    score = 0

    while learned < max_learned or score != 1:
        card = choose_card(cards, cards_seen)
        score = get_score(learned, card)

        responses.append({
            'learner': learner,
            'time': time,
            'card': card['name'],
            'score': score,
        })

        time, count = update_time(time, count)

        if count > 0:
            learned += card['transit']
        else:
            learned -= degrade

    return responses


def choose_card(cards, cards_seen):
    """
    Selects a card at random from the set that hasn't been seen yet.
    If we've seen all the cards, chooses a random card instead.
    """

    card = None
    if len(cards_seen) == len(cards):
        cards_seen = []
    while not card or card in cards_seen:
        card = sample(cards, 1)[0]
    cards_seen.append(card)
    return card


def get_score(learned, card):
    """
    Given a probability of learned and card information,
    produce a response that reflects that score.
    """
    correct = learned * (1 - card['slip']) + (1 - learned) * card['guess']
    return int(bool_from_percent(correct))


def bool_from_percent(percent, steps=1000000):
    """
    Given a percentage, returns a boolean that reflects that likelihood.
    """

    return percent * steps > randrange(steps)


def update_time(time, count):
    """
    Updates the time and count, simulating user learning sessions.
    """

    count += 1
    if count > uniform(*max_questions):
        time += int(uniform(*session_gap))
        count = 0
    else:
        time += int(uniform(*question_gap))

    return time, count


if __name__ == '__main__':
    d = main(10, 10)
    for r in d['responses']:
        print(r['learner'], r['card'], r['score'], r['time'])

    print('\n')

    for c in d['cards']:
        print('%s %f %f %f' % (c['name'], c['guess'], c['slip'], c['transit']))
