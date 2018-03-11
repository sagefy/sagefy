"""
Primary learning sequencer.
"""

from time import time
from database.card_parameters import get_card_parameters, get_distribution, \
  bundle_distribution, insert_card_parameters, update_card_parameters
from database.response import get_latest_response, insert_response
from database.card import validate_card_response, score_card_response
from modules.sequencer.update import update as formula_update
from modules.sequencer.params import init_learned
from schemas.card import scored_kinds

"""
Card
- [x] correct
- [x] guess
- [x] slip
- [_] transit  TODO-3

Unit
- [x] learned
- [x] belief
- [ ] unit quality  TODO-3
- [ ] unit difficulty  TODO-3

Subject
- [ ] learner-subject ability  TODO-3
- [ ] subject quality  TODO-3
- [ ] subject difficulty  TODO-3
"""


def update(db_conn, user, card, response):
  """
  Update the card's parameters (and its parents')
  when given a response.
  """

  # TODO-3 split up into smaller methods

  if card['kind'] not in scored_kinds:
    return {
      'response': {},
      'feedback': '',
    }

  errors = validate_card_response(card, response)
  if errors:
    return {'errors': errors}

  score, feedback = score_card_response(card, response)
  response = {
    'user_id': user['id'],
    'card_id': card['entity_id'],
    'unit_id': card['unit_id'],
    'response': response,
    'score': score,
  }

  card_parameters = get_card_parameters(
    db_conn,
    {'entity_id': card['entity_id']}
  ) or {}
  previous_response = get_latest_response(db_conn, user['id'],
                                          card['unit_id'])

  now = time()
  time_delta = now - (int(previous_response['created'].strftime("%s"))
                      if previous_response else now)

  learned = (previous_response['learned']
             if previous_response else init_learned)
  guess_distribution = get_distribution(card_parameters, 'guess')
  slip_distribution = get_distribution(card_parameters, 'slip')

  updates = formula_update(score, time_delta,
                           learned, guess_distribution, slip_distribution)

  response['learned'] = updates['learned']
  response, errors = insert_response(db_conn, response)
  if errors:
    return {'errors': errors, 'feedback': feedback}

  updated_card_parameters = {
    'entity_id': card['entity_id'],
    'guess_distribution':
    bundle_distribution(updates['guess_distribution']),
    'slip_distribution':
    bundle_distribution(updates['slip_distribution']),
  }
  if card_parameters.get('id'):
    _, errors = update_card_parameters(
      db_conn,
      card_parameters,
      updated_card_parameters
    )
  else:
    _, errors = insert_card_parameters(
      db_conn,
      updated_card_parameters
    )

  if errors:
    return {'errors': errors, 'feedback': feedback}

  return {'response': response, 'feedback': feedback}
