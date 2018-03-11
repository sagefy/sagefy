from random import shuffle, random
from math import floor
from functools import reduce  # pylint: disable=redefined-builtin
from modules.sequencer.formulas import calculate_correct
from modules.sequencer.params import init_learned
from database.response import get_latest_response
from database.card import list_random_cards_in_unit
from database.card_parameters import get_card_parameters, \
  get_card_parameters_values
from schemas.card import scored_kinds


P_SCORED_MAP = {
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


def partition(input_list, condition):
  return reduce(lambda x, y: x[not condition(y)].append(y) or x, input_list, ([], []))


def get_learned(db_conn, user, unit):
  unit_id = unit['entity_id']
  previous_response = get_latest_response(db_conn, user['id'], unit_id)
  if previous_response:
    return previous_response['learned']
  return init_learned


def get_card_batch(db_conn, user, unit):
  unit_id = unit['entity_id']
  cards = list_random_cards_in_unit(db_conn, unit_id)
  if not cards:
    return None, None, None
  previous_response = get_latest_response(db_conn, user['id'], unit_id)
  if previous_response:
    # Don't allow the previous card as the next card
    cards = [
      card
      for card in cards
      if card['entity_id'] != previous_response['card_id']
    ]
  params = {}
  for card in cards:
    params[card['entity_id']] = get_card_parameters_values(
      get_card_parameters(db_conn, {'entity_id': card['entity_id']}) or {}
    )
  shuffle(cards)
  scored, unscored = partition(
    cards,
    lambda c: c['kind'] in scored_kinds
  )
  return scored, unscored, params


def choose_scored_card(scored, all_params, learned):
  for card in scored:
    params = all_params[card['entity_id']]
    if params:
      guess = params['guess']
      slip = params['slip']
      correct = calculate_correct(guess, slip, learned)
      if 0.25 < correct < 0.75:
        return card
  return scored[0]


def choose_unscored_card(scored, unscored):
  if unscored:
    return unscored[0]
  if scored:
    return scored[0]
  return None


def choose_card(db_conn, user, unit):
  """
  Given a user and a unit, choose an appropriate card.
  Return a card instance.
  """

  # TODO-3 simplify this method
  # TODO-2 is the sample value decent?
  # TODO-2 has the learner seen this card recently?

  learned = get_learned(db_conn, user, unit)
  scored, unscored, params = get_card_batch(db_conn, user, unit)
  if not scored and not unscored:
    return None
  choose_scored = random() < P_SCORED_MAP[floor(learned * 10)]
  if choose_scored and scored:
    return choose_scored_card(scored, params, learned)
  return choose_unscored_card(scored, unscored)
