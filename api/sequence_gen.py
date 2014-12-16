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
# - Card Difficulty

from time import time
from random import uniform, randrange, sample
import string

p_correct = 0
time = int(time())
current_session_count = 0

question_gap = (5, 60)
session_gap = (60 * 60 * 12, 60 * 60 * 36)
p_correct_adjustment = (-0.01, uniform(0.05, 0.1))
p_correct_new_session = (-0.01, 0.01)
max_questions = (20, 100)
guess = (0.2, 0.4)
slip = (0.05, 0.2)
difficulty = (0.3, 0.7)

cards = []
seen = []

for l in string.ascii_uppercase:
    cards.append({
        'name': l,
        'guess': uniform(*guess),
        'slip': uniform(*slip),
        'difficulty': uniform(*difficulty)
    })


def bool_from_percent(percent):
    return randrange(100) < percent * 100

card = None

while p_correct < 0.95:
    if len(seen) >= len(string.ascii_uppercase):
        seen = []

    while not card or card in seen:
        card = sample(cards, 1)[0]
    seen.append(card)

    if bool_from_percent(card['guess']):
        score = 1
    elif bool_from_percent(card['slip']):
        score = 0
    elif p_correct < card['difficulty'] * uniform(0.5, 1.0):
        score = 0
    else:
        score = int(bool_from_percent(p_correct))

    print(time, score, card['name'])

    current_session_count += 1
    if current_session_count > uniform(*max_questions):
        time += int(uniform(*question_gap))
        p_correct += uniform(*p_correct_adjustment)
        current_session_count = 0
    else:
        time += int(uniform(*session_gap))
        p_correct += uniform(*p_correct_new_session)

    if p_correct < 0:
        p_correct = 0
