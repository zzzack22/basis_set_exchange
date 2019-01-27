'''
Handlers for command line subcommands
'''

import os
import argparse
import argcomplete
from .. import api
from .. import version
from ..misc import compact_elements


def _format_columns(lines, prefix=''):
    if len(lines) == 0:
        return ''

    ncols = 0
    for l in lines:
        ncols = max(ncols, len(l))

    if ncols == 0:
        return ''

    # We only find the max strlen for all but the last col
    maxlen = [0] * (ncols - 1)
    for l in lines:
        for c in range(ncols - 1):
            maxlen[c] = max(maxlen[c], len(l[c]))

    fmtstr = prefix + '  '.join(['{{:{x}}}'.format(x=x) for x in maxlen])
    fmtstr += '  {}'
    return [fmtstr.format(*l) for l in lines]


def cli_list_basis_sets(args):
    metadata = api.filter_basis_sets(args.substr, args.family, args.role, args.data_dir)

    if args.no_description:
        liststr = metadata.keys()
    else:
        liststr = _format_columns([(k, v['description']) for k, v in metadata.items()])

    return '\n'.join(liststr)


def cli_list_families(args):
    families = api.get_families(args.data_dir)
    return '\n'.join(families)


def cli_list_formats(args):
    all_formats = api.get_formats()

    if args.no_description:
        liststr = all_formats.keys()
    else:
        liststr = _format_columns(all_formats.items())

    return '\n'.join(liststr)


def cli_list_ref_formats(args):
    all_refformats = api.get_reference_formats()

    if args.no_description:
        liststr = all_refformats.keys()
    else:
        liststr = _format_columns(all_refformats.items())

    return '\n'.join(liststr)


def cli_list_roles(args):
    all_roles = api.get_roles()

    if args.no_description:
        liststr = all_roles.keys()
    else:
        liststr = _format_columns(all_roles.items())

    return '\n'.join(liststr)


def cli_lookup_by_role(args):
    return api.lookup_basis_by_role(args.primary_basis, args.role)


def cli_get_basis(args):
    name = args.name.lower()
    metadata = api.get_metadata(args.data_dir)
    if not name in metadata:
        raise RuntimeError(
            "Basis set {} does not exist. For a complete list of basis sets, use the 'list-basis-sets' command".format(
                name))

    return api.get_basis(
        name=args.name,
        elements=args.elements,
        version=args.version,
        fmt=args.fmt,
        uncontract_general=args.unc_gen,
        uncontract_spdf=args.unc_spdf,
        uncontract_segmented=args.unc_seg,
        make_general=args.make_gen,
        optimize_general=args.opt_gen,
        data_dir=args.data_dir,
        header=not args.noheader)


def cli_get_refs(args):
    name = args.name.lower()
    metadata = api.get_metadata(args.data_dir)
    if not name in metadata:
        raise KeyError(
            "Basis set {} does not exist. For a complete list of basis sets, use the 'list-basis-sets' command".format(
                name))

    return api.get_references(
        basis_name=args.name, elements=args.elements, version=args.version, fmt=args.fmt, data_dir=args.data_dir)
    return 0


def cli_get_info(args):
    name = args.name.lower()
    metadata = api.get_metadata(args.data_dir)
    if not name in metadata:
        raise KeyError(
            "Basis set {} does not exist. For a complete list of basis sets, use the 'list-basis-sets' command".format(
                name))

    bs_meta = metadata[name]
    ret = []
    ret.append('-' * 80)
    ret.append(name)
    ret.append('-' * 80)
    ret.append('    Display Name: ' + bs_meta['display_name'])
    ret.append('     Description: ' + bs_meta['description'])
    ret.append('            Role: ' + bs_meta['role'])
    ret.append('          Family: ' + bs_meta['family'])
    ret.append('  Function Types: ' + ','.join(bs_meta['functiontypes']))
    ret.append('  Latest Version: ' + bs_meta['latest_version'])
    ret.append('')

    aux = bs_meta['auxiliaries']
    if len(aux) == 0:
        ret.append('Auxiliary Basis Sets: None')
    else:
        ret.append('Auxiliary Basis Sets:')
        ret.extend(_format_columns(list(aux.items()), '    '))

    ver = bs_meta['versions']
    ret.append('')
    ret.append('Versions:')

    # Print 3 columns - version, elements, revision description
    version_lines = _format_columns([(k, compact_elements(v['elements']), v['revdesc']) for k, v in ver.items()],
                                    '    ')
    ret.extend(version_lines)

    return '\n'.join(ret)


def cli_get_notes(args):
    return api.get_basis_notes(args.name, args.data_dir)


def cli_get_family(args):
    return api.get_basis_family(args.name, args.data_dir)


def cli_get_versions(args):
    name = args.name.lower()
    metadata = api.get_metadata(args.data_dir)
    if not name in metadata:
        raise KeyError(
            "Basis set {} does not exist. For a complete list of basis sets, use the 'list-basis-sets' command".format(
                name))

    version_data = {k: v['revdesc'] for k, v in metadata[name]['versions'].items()}

    if args.no_description:
        liststr = version_data.keys()
    else:
        liststr = _format_columns(version_data.items())

    return '\n'.join(liststr)


def cli_get_family_notes(args):
    return api.get_family_notes(args.family, args.data_dir)
