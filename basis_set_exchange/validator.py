"""
Functions related to validating JSON files (including against schema)
"""

import jsonschema

from . import api
from . import fileio


def _validate_extra_references(bs_data):
    '''Extra checks for references files'''
    pass


def _validate_extra_metadata(bs_data):
    '''Extra checks for metadata files'''

    # Check that family is lowercase
    fam = bs_data['basis_set_family']
    if not fam.islower():
        raise RuntimeError("Family '{}' is not lowercase".format(fam))


def _validate_extra_component(bs_data):
    '''Extra checks for component basis files'''

    # Make sure size of the coefficient matrix matches the number of exponents
    for el in bs_data['basis_set_elements'].values():
        if not 'element_electron_shells' in el:
            continue

        for s in el['element_electron_shells']:
            nprim = len(s['shell_exponents'])
            if nprim <= 0:
                raise RuntimeError("Invalid number of primitives: {}".format(nprim))

            for g in s['shell_coefficients']:
                if nprim != len(g):
                    raise RuntimeError("Number of coefficients doesn't match number of primitives ({} vs {}".format(
                        len(g), nprim))

            # If more than one AM is given, that should be the number of
            # general contractions
            nam = len(s['shell_angular_momentum'])
            if nam > 1:
                ngen = len(s['shell_coefficients'])
                if ngen != nam:
                    raise RuntimeError("Number of general contractions doesn't match combined AM ({} vs {}".format(
                        ngen, nam))


def _validate_extra_element(bs_data):
    '''Extra checks for basis metadata files'''
    pass


def _validate_extra_table(bs_data):
    '''Extra checks for table basis files'''
    pass


_validate_map = {
    'references': _validate_extra_references,
    'metadata': _validate_extra_metadata,
    'component': _validate_extra_component,
    'element': _validate_extra_element,
    'table': _validate_extra_table
}


def validate_data(file_type, bs_data):
    """
    Validates json basis set data against a schema

    Parameters
    ----------
    file_type : str
        Type of file to read. May be 'component', 'element', 'table', or 'references'
    bs_data:
        Data to be validated

    Raises
    ------
    RuntimeError
        If the file_type is not valid (and/or a schema doesn't exist)
    ValidationError
        If the given file does not pass validation
    FileNotFoundError
        If the file given by file_path doesn't exist
    """

    if file_type not in _validate_map:
        raise RuntimeError("{} is not a valid file_type".format(file_type))

    schema = api.get_schema(file_type)
    jsonschema.validate(bs_data, schema)
    _validate_map[file_type](bs_data)


def validate_file(file_type, file_path):
    """
    Validates a file against a schema

    Parameters
    ----------
    file_type : str
        Type of file to read. May be 'component', 'element', 'table', or 'references'
    file_path:
        Full path to the file to be validated

    Raises
    ------
    RuntimeError
        If the file_type is not valid (and/or a schema doesn't exist)
    ValidationError
        If the given file does not pass validation
    FileNotFoundError
        If the file given by file_path doesn't exist
    """

    file_data = fileio._read_plain_json(file_path, False)
    validate_data(file_type, file_data)
