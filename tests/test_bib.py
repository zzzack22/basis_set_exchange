"""
Validation of bibtex output
"""

from bse import api
import pytest
import check_bibtex


# Load all the metadata once
_bs_names = api.get_all_basis_names()

@pytest.mark.skipif(check_bibtex.available == False, reason="Latex/Bibtex commands not found, so I can't verify bib files")
@pytest.mark.parametrize('basis_name', _bs_names)
def test_bibtex(basis_name):
    bib_str = api.get_references(basis_name, fmt='bib')
    check_bibtex.validate_bibtex(bib_str)
