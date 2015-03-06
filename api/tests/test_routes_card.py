import pytest

xfail = pytest.mark.xfail


@xfail
def test_get_card():
    """
    Expect to get the card information for displaying to a contributor.
    """

    assert False

    # TODO model
    # TODO get unit data
    # TODO join through requires both ways
    # TODO list of topics
    # TODO list of versions
    # TODO sequencer data: learners, transit, guess, slip, difficulty


@xfail
def test_get_card_404():
    """
    Expect to fail to get an unknown card. (404)
    """

    assert False


@xfail
def test_learn_card():
    """
    Expect to get a card for learn mode. (200)
    """

    assert False


@xfail
def test_learn_card_relevant():
    """
    Expect to learn card to only provide relevant data. (200)
    """

    assert False


@xfail
def test_learn_card_401():
    """
    Expect to require log in to get a card for learn mode. (401)
    """

    assert False


@xfail
def test_learn_card_404():
    """
    Expect to fail to get an unknown card for learn mode. (404)
    """

    assert False


@xfail
def test_learn_card_400():
    """
    Expect the card for learn mode to make sense,
    given the learner context. (400)
    """

    assert False


@xfail
def test_respond_card():
    """
    Expect to respond to a card. (200)
    """

    assert False


@xfail
def test_respond_card_401():
    """
    Expect to require log in to get an unknown card. (401)
    """

    assert False


@xfail
def test_respond_card_404():
    """
    Expect to fail to respond to an unknown card. (404)
    """

    assert False


@xfail
def test_respond_card_400():
    """
    Expect respond to a card to make sense. (400)
    """

    assert False
