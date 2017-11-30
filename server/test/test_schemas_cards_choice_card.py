from schemas.cards.choice_card import has_correct_options


def test_has_correct_options():
  options_a = [{
    'correct': True,
  }]
  options_b = [{
    'correct': False,
  }]
  assert has_correct_options(options_a) is None
  assert isinstance(has_correct_options(options_b), str)
