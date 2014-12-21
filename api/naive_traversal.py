units_ = (
    ('A', ('B', 'C'),    0,    0),
    ('B', ('D', 'E'),    0,    0),
    ('C', ('F',),     0.25, 0.96),
    ('D', (),            0,    0),
    ('E', ('G', 'H'),  1.0,  0.8),
    ('F', ('H', 'I'),  1.0, 0.96),
    ('G', (),          1.0, 0.96),
    ('H', (),            0,    0),
    ('I', (),            0,    0),
)


required_learned = 0.99
required_belief = 0.95


def get_unit(name, units):
    """
    """
    for unit in units:
        if unit[0] == name:
            return unit


def traverse(units):
    """
    Receives a list of units, which represent the highest points
    of the graph. (Where no unit requires them.)

    Uses depth first search.
    """
    buckets = {
        'seen': [],
        'diagnose': [],
        'review': [],
        'ready': [],
    }

    for unit in filter_to_top(units):
        judge(unit, units, buckets)

    if len(buckets['diagnose']):
        return ('diagnose', filter_to_top(buckets['diagnose'])[0])

    if len(buckets['review']):
        return ('review', order_units_by_dependencies(buckets['review'])[0])

    if len(buckets['ready']):
        return ('learn', order_units_by_dependencies(buckets['ready'])[0])

    return ('done', [])


def judge(unit, units, buckets):
    """
    """

    name, requires, learned, belief = unit

    if name in buckets['seen']:
        return
    buckets['seen'].append(name)

    if learned > required_learned and belief > required_belief:
        return

    if belief > required_belief:
        buckets['ready'].append(unit)
    elif belief > 0:
        buckets['review'].append(unit)
    else:
        buckets['diagnose'].append(unit)

    requires = [get_unit(n, units) for n in requires]
    for req in requires:
        judge(req, units, buckets)


def filter_to_top(units):
    """
    """
    units_left = [unit[0] for unit in units]

    for unit in units:
        for req in unit[1]:
            if req in units_left:
                units_left.remove(req)

    return [get_unit(u, units) for u in units_left]


def order_units_by_dependencies(units):
    """
    """

    # The algorithm considers how many nodes depend on the given node,
    # rather than how deep in the graph the node is.

    dep = {unit[0]: 0 for unit in units}

    for unit in units:
        for req in unit[1]:
            dep[req] += 1

    order = sorted(dep, key=dep.get, reverse=True)
    return [get_unit(u, units) for u in order]


print(traverse(units_))
