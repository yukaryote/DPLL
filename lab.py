#!/usr/bin/env python3

import sys

sys.setrecursionlimit(10000)


def simplify(formula, var, val):
    """
    Simplifies a CNF formula by removing clauses that evaluate to True.
    Also propagates unit clauses.
    Args:
        formula: CNF formula

    Returns:
        Simplified CNF formula and whether the formula contradicts itself

    >>> form = [[('a', True), ('b', True), ('c', True)],[('a', False), ('f', True)],[('d', False), ('e', True), ('a', True), ('g', True)],[('h', False), ('c', True), ('a', False), ('f', True)]]
    >>> simplify(form, 'a', True)
    [[('f', True)], [('h', False), ('c', True), ('f', True)]]
    >>> simplify(form, 'a', False)
    [[('b', True), ('c', True)], [('d', False), ('e', True), ('g', True)]]
    """
    sim = []
    iscontra = False
    for clause in formula:
        new_clause = []
        if len(clause) == 1:
            if clause[0][0] == var:
                if clause[0][1] == val:
                    continue
                else:
                    iscontra = True
                    break
            else:
                new_clause.append(clause[0])
        else:
            for literal in clause:
                if literal[0] == var:
                    if literal[1] == val:
                        new_clause = []
                        break
                    else:
                        continue
                else:
                    new_clause.append(literal)
        if new_clause:
            sim.append(new_clause)
    if iscontra:
        return False
    else:
        if sim:
            return sim
        else:
            return True


def satisfying_assignment(formula, assign=None):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    >>> satisfying_assignment([[('a', True)], [('b', True)], [('a', False), ('b', False)]])
    """
    if assign is None:
        assign = {}
    if not formula:
        return {}
    shortest = [i[0] for i in formula if len(i) == 1]
    if shortest:
        var = shortest[0][0]
        val = shortest[0][1]
    else:
        var = formula[0][0][0]
        val = formula[0][0][1]
    sim_form = simplify(formula, var, val)
    if sim_form is True:
        assign[var] = val
    elif sim_form is not False:
        result = satisfying_assignment(sim_form, assign)
        if result is not None:
            assign[var] = val
        elif result is None and shortest:
            return None
        elif result is None and not shortest:
            sim_form = simplify(formula, var, not val)
            assign[var] = not val
            return satisfying_assignment(sim_form, assign)
    else:
        return None
    return assign


if __name__ == '__main__':
    import doctest

    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
