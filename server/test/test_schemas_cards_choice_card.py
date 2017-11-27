from schemas.cards.choice_card import has_correct_options


def test_has_correct_options():
  optionsA = [{
      'correct': True,
  }]
  optionsB = [{
      'correct': False,
  }]
  assert has_correct_options(optionsA) is None
  assert isinstance(has_correct_options(optionsB), str)
