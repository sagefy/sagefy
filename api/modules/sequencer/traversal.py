from modules.sequencer.params import max_learned, max_belief, diag_belief
from models.response import Response
from modules.sequencer.formulas import calculate_belief
from time import time


def traverse(user, set_):
    """
    TODO@ Given a user and a set, sort all the units in the set based on need.
    Return status of (diagnose, learn, review, done) and list of units.

    Routes that use this:

    - @post('/api/cards/{card_id}/responses')
        - needs a status and a list of units per that status
    - @get('/api/sets/{set_id}/tree')
        - needs a status per unit, and the dependencies in graph form
    - @get('/api/sets/{set_id}/units')
        - needs units under the status "review" or "learn", in priority order
    """

    buckets = {
        'diagnose': [],
        'learn': [],
        'review': [],
    }

    units = set_.list_units()
    for unit in units:
        status = judge(unit)
        buckets[status].append(unit)

    # Make sure the buckets are in the correct orderings
    buckets['diagnose'] = order_units_by_need(buckets['diagnose'])
    buckets['diagnose'].reverse()
    buckets['learn'] = order_units_by_need(buckets['learn'])
    buckets['review'] = order_units_by_need(buckets['review'])

    return buckets


def order_units_by_need(units):
    """
    Order the given units by the number of units dependent.

    For example, if unit A requires unit B, and unit B requires unit C,
    but nothing requires C,
    then the order would be C (2), B (1), then A (0).

    Units with more dependencies will come at the beginning of the list,
    units with fewer dependencies will come at the end.
    This function only considers the units provided; not all units in the set.

    The algorithm considers how many nodes depend on the given node,
    rather than how deep in the graph the node is.
    """

    ids_to_units = {unit['entity_id']: unit for unit in units}
    dependents = match_unit_dependents(units)
    dependents = {unit_id: len(deps) for unit_id, deps in dependents.items()}
    ids = sorted(dependents, key=dependents.get, reverse=True)
    return [ids_to_units[id_] for id_ in ids]


def match_unit_dependents(units):
    """
    For each unit, provide a set of units that depend on the given unit.
    """

    ids_to_units = {unit['entity_id']: unit for unit in units}
    dependents = {unit['entity_id']: set() for unit in units}

    def _(unit, dep):
        for required_id in unit['require_ids']:
            dependents[required_id].add(dep)
            required_unit = ids_to_units[required_id]
            _(required_unit, dep)

    for unit in units:
        _(unit, unit)

    return dependents


def judge(unit, user):
    """
    Given a unit and a user, pass judgement on which bucket to file it under.
    """

    response = Response.get_latest(
        user_id=user['id'],
        unit_id=unit['entity_id']
    )
    if response:
        learned = response['learned']
        now = time()
        print(response['created'])
        time_delta = now - (int(response['created'].strftime("%s"))
                            if response else now)
        belief = calculate_belief(learned, time_delta)
    else:
        learned = 0
        belief = 0

    if learned >= max_learned:
        if belief > max_belief:
            return "done"

        if belief <= max_belief:
            return "review"

    if belief > diag_belief:
        return "learn"

    return "diagnose"
