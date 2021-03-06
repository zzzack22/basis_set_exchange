'''
Miscellaneous helper functions
'''

from . import lut


def _Z_from_str(s):
    if s.isdecimal():
        return int(s)
    else:
        return lut.element_Z_from_sym(s)


def compact_elements(elements):
    """
    Create a string (with ranges) given a list of element numbers

    For example, [1, 2, 3, 6, 7, 8, 10] will return "H-Li,C-O,Ne"
   """

    if len(elements) == 0:
        return

    # We have to convert to integers for this function
    elements = [int(el) for el in elements]

    # Just to be safe, sort the list
    el = sorted(set(elements))

    ranges = []
    i = 0
    while i < len(el):
        start_el = el[i]
        end_el = start_el

        i += 1
        while i < len(el):
            if el[i] != end_el + 1:
                break

            end_el += 1
            i += 1

        if start_el == end_el:
            ranges.append([start_el])
        else:
            ranges.append([start_el, end_el])

    # Convert to elemental symbols
    range_strs = []
    for r in ranges:
        sym = lut.element_sym_from_Z(r[0], True)

        if len(r) == 1:
            range_strs.append(sym)
        elif len(r) == 2 and r[1] == r[0] + 1:
            sym2 = lut.element_sym_from_Z(r[1], True)
            range_strs.append(sym + "," + sym2)
        else:
            sym2 = lut.element_sym_from_Z(r[1], True)
            range_strs.append(sym + "-" + sym2)

    return ",".join(range_strs)


def expand_elements(compact_el, as_str=False):
    """
    Create a list of integers given a string or list of compacted elements

    This is partly the opposite of compact_elements, but is more flexible.

    compact_el can be a list or a string. If compact_el is a list, each element is processed individually
    as a string (meaning list elements can contain commas, ranges, etc)
    If compact_el is a string, it is split by commas and then each section is processed.

    In all cases, element symbols (case insensitive) and Z numbers (as integers or strings)
    can be used interchangeably. Ranges are also allowed in both lists and strings.

    Some examples:
        "H-Li,C-O,Ne" will return [1, 2, 3, 6, 7, 8, 10]
        "H-N,8,Na-12" will return [1, 2, 3, 4, 5, 6, 7, 8, 11, 12]
        ['C', 'Al-15,S', 17, '18'] will return [6, 13, 14, 15, 16, 17, 18]

    If as_str is True, the list will contain strings of the integers
    (ie, the first example above will return ['1', '2', '3', '6', '7', '8', '10']
    """

    # Works for both strings and lists
    if len(compact_el) == 0:
        return []

    # If compact_el is a list, make it a comma-separated string
    if isinstance(compact_el, list):
        compact_el = [str(x) for x in compact_el]
        compact_el = ','.join(compact_el)

    # Split on commas
    tmp_list = compact_el.split(',')

    # Now go over each one and replace elements with ints
    el_list = []
    for el in tmp_list:
        if not '-' in el:
            el_list.append(_Z_from_str(el))
        else:
            begin, end = el.split('-')
            begin = _Z_from_str(begin)
            end = _Z_from_str(end)
            el_list.extend(list(range(begin, end + 1)))

    if as_str is True:
        return [str(x) for x in el_list]
    else:
        return el_list


def transform_basis_name(name):
    """
    Transforms the name of a basis set to an internal representation

    This makes comparison of basis set names easier by, for example,
    converting the name to all lower case.
    """

    return name.lower()
