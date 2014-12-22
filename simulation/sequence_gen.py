# time, score
# p(score == 1) should increase over time
# times should come in batches over one-two hours, on a few days a week
# produce large variation

# Factors:
# - Time
# - Prior
# - Response
# - Card Guess
# - Card Slip

from random import uniform, randrange, sample

question_gap = (5, 60)
session_gap = (60 * 60 * 12, 60 * 60 * 36)
p_correct_adjustment = (-0.01, uniform(0.05, 0.1))
p_correct_new_session = (-0.01, 0.01)
max_questions = (20, 100)
guess = (0.2, 0.4)
slip = (0.05, 0.2)
card_names = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')


def bool_from_percent(percent):
    return randrange(100) < percent * 100

cards = []

for l in card_names:
    cards.append({
        'name': l,
        'guess': uniform(*guess),
        'slip': uniform(*slip)
    })


def get_score(card, p_correct):
    r = p_correct * (1 - card['slip']) + (1 - p_correct) * card['guess']
    return int(bool_from_percent(r))


def generate_responses():
    p_correct = 0
    t = 1
    current_session_count = 0

    seen = []

    card = None
    responses = []

    while p_correct < 0.99:
        if len(seen) >= len(card_names):
            seen = []

        while not card or card in seen:
            card = sample(cards, 1)[0]
        seen.append(card)

        score = get_score(card, p_correct)

        responses.append({
            'time': t,
            'score': score,
            'card': card['name']
        })

        current_session_count += 1
        if current_session_count > uniform(*max_questions):
            t += int(uniform(*session_gap))
            p_correct += uniform(*p_correct_adjustment)
            current_session_count = 0
        else:
            t += int(uniform(*question_gap))
            p_correct += uniform(*p_correct_new_session)

        if p_correct < 0:
            p_correct = 0

    return responses

if __name__ == '__main__':
    print(generate_responses())
