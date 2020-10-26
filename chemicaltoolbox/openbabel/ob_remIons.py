#!/usr/bin/env python
"""
    Input: molecular input file.
    Output: Molecule file with removed ions and fragments.
    Copyright 2012, Bjoern Gruening and Xavier Lucas
"""
import argparse

from openbabel import openbabel, pybel
openbabel.obErrorLog.StopLogging()


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('-iformat', default='sdf', help='input file format')
    parser.add_argument('-i', '--input', required=True, help='input file name')
    parser.add_argument('-o', '--output', required=True, help='output file name')
    parser.add_argument('-idx', default=False, action='store_true', help='should output be indexed table?')
    return parser.parse_args()


def remove_ions(args):
    if args.idx:
        with open(args.output, 'w') as outfile:
            for cnt, mol in enumerate(pybel.readfile(args.iformat, args.input)):
                if mol.OBMol.NumHvyAtoms() > 5:
                    mol.OBMol.StripSalts(0)
                    if 'inchi' in mol.data:
                        del mol.data['inchi']  # remove inchi cache so modified mol is saved
                    # Check if new small fragments have been created and remove them
                    if mol.OBMol.NumHvyAtoms() > 5:
                        outfile.write(str(cnt) + "," + mol.write(args.iformat))
                    else:
                        outfile.write(str(cnt) + ",\n")
                else:
                    outfile.write(str(cnt) + ",\n")
        outfile.close()
    else:
        outfile = pybel.Outputfile(args.iformat, args.output, overwrite=True)
        for mol in pybel.readfile(args.iformat, args.input):
            if mol.OBMol.NumHvyAtoms() > 5:
                mol.OBMol.StripSalts(0)
                if 'inchi' in mol.data:
                    del mol.data['inchi']  # remove inchi cache so modified mol is saved
                # Check if new small fragments have been created and remove them
                if mol.OBMol.NumHvyAtoms() > 5:
                    outfile.write(mol)
        outfile.close()


def __main__():
    """
        Remove any counterion and delete any fragment but the largest one for each molecule.
    """
    args = parse_command_line()
    remove_ions(args)


if __name__ == "__main__":
    __main__()
