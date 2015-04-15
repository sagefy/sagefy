import pytest

xfail = pytest.mark.xfail


# TODO @outline tests  https://docs.sagefy.org/f_planning/sequencer

@xfail
def test_x(app):
    """
    Expect ...
    """

    assert False


"""
Expect to estimate diagnosis duration.
Expect to show progress in diagnosis.
Expect diagnosis to not show feedback to responses.
Expect end of diagnosis to return to tree.
Expect choose unit to show time estimate and learning objective.
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
Expect to track number of units that depend on the given unit.
Expect to prefer units with more dependencies in choose unit.
Expect choose unit to only show available units. (No requires remaining.)

UI
---------

My Sets should link to search for sets.
Search Sets should show difficulty estimates.
Search Sets should link to tree of units.
Search Sets should have button to add to my sets.
My Sets should indicate sets needing diagnosis/review.
My Sets should indicate sets needing progress.
Menu should show current unit selected.
Menu should show link to current set tree.
Menu should show links to discuss card, unit, set as applicable.
Choose Unit should visually emphasize the first unit.
Choose Unit should show time estimate and learning objective per unit.
"""
