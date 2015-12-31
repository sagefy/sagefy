import pytest

xfail = pytest.mark.xfail


# TODO-3 outline tests  https://docs.sagefy.org/f_planning/sequencer

@xfail
def test_x(app):
    """
    Expect ...
    """

    assert False


"""
Expect to estimate diagnosis duration.
Expect to show progress in diagnosis.
Expect end of diagnosis to return to tree.
Expect to show progress in learning unit.
Expect to focus on non-assessment cards for low learned.
Expect to focus on medium difficulty card for medium learned.
Expect to intervene with non-assessment after pattern of incorrect responses.
Expect to focus on challenging cards for high learned.
Expect to follow card require chains.
Expect to follow unit require chains.
Expect recommend to switch to unit after significant gain.
Expect to show congrats tree after proficient in all units.
Expect to recommend sets after proficient in all units.
Expect to remind me when to review units.
"""
