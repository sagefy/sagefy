from math import fsum


def compute_set_learned(units):
    """
    Given a list of units, compute the overall ability.
    """
    return fsum(unit.learned for unit in units) / len(units)


def compute_unit_quality(learners):
    """
    Given a list of learners who are engaged in this unit,
    determine the quality of the unit.

    TODO: Factor in number of learners as well.
    """
    if learners < 100:
        return 0
    return fsum(l.learned for l in learners) / len(learners)


def compute_set_quality(units):
    """
    Given a list of units, compute the set quality.
    """
    return fsum(unit.quality for unit in units) / len(units)
