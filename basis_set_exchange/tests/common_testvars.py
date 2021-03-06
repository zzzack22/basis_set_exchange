'''
Some data common to all tests
'''

import basis_set_exchange as bse

# Use random for getting sets of elements
rand_seed = 39466  # from random.org

# Load all the metadata once
data_dir = bse.api._default_data_dir
bs_metadata = bse.get_metadata()
bs_names = bse.get_all_basis_names()
bs_formats = list(bse.get_formats().keys())
ref_formats = list(bse.get_reference_formats().keys())
all_families = bse.get_families()
all_roles = bse.get_roles()
true_false = [True, False]

# All files in the data dir
all_files = bse.fileio.get_all_filelist(data_dir)
all_metadata_files = all_files[0]
all_table_files = all_files[1]
all_element_files = all_files[2]
all_component_files = all_files[3]

# A representative sample of basis sets
bs_names_sample = ['6-31g', '6-31+g*', 'aug-cc-pvtz', 'lanl2dz', 'def2-tzvp', 'tzp', 'sto-3g']


def bool_matrix(size):
    '''Returns an identity matrix of a given size consisting of bool types
    '''
    ret = [[False for i in range(size)] for j in range(size)]
    for x in range(size):
        ret[x][x] = True
    return ret
