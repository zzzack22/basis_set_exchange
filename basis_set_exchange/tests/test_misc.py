"""
Tests of BSE miscellaneous functions
"""

import pytest
from basis_set_exchange import misc


# yapf: disable
@pytest.mark.parametrize("elements, expected", [([1], "H"),
                                                ([1, 2], "H,He"),
                                                ([1, 10], "H,Ne"),
                                                ([1, 2, 3, 11, 23, 24], "H-Li,Na,V,Cr")])
# yapf: enable
def test_compact_string(elements, expected):
    '''Test compacting a string of elements (and then expanding them)'''
    compacted = misc.compact_elements(elements)
    assert compacted == expected

    expanded = misc.expand_elements(compacted)
    assert expanded == elements

    expanded = misc.expand_elements(compacted, True)
    assert expanded == [str(x) for x in elements]


# yapf disable
@pytest.mark.parametrize("compact_el, expected",
                         [("H-Li,C-O,Ne", [1, 2, 3, 6, 7, 8, 10]), ("H-N,8,Na-12", [1, 2, 3, 4, 5, 6, 7, 8, 11, 12]),
                          (['C', 'Al-15,S', 17, '18'], [6, 13, 14, 15, 16, 17, 18])])
# yapf enable
def test_expand_elements(compact_el, expected):
    expanded = misc.expand_elements(compact_el)
    assert expanded == expected
