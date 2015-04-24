import pytest

xfail = pytest.mark.xfail


@xfail
def test_seq_next(app):
    """
    Expect sequencer route to say where to go next
    """

    assert False
