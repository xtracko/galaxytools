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
    parser.add_argument('-idx', default=False, action='store_true', help='should output be an indexed text table?')
    return parser.parse_args()


def remove_ions(args):
    outfile = open(args.output, 'w') if args.idx else pybel.Outputfile(args.iformat, args.output, overwrite=True)
    output = []
    for index, mol in enumerate(pybel.readfile(args.iformat, args.input)):
        output.append(str(index) + ",")
        if mol.OBMol.NumHvyAtoms() > 5:
            mol.OBMol.StripSalts(0)
            if 'inchi' in mol.data:
                del mol.data['inchi']  # remove inchi cache so modified mol is saved
            # heck if new small fragments have been created and remove them
            if mol.OBMol.NumHvyAtoms() > 5:
                output[index] = output[index] + mol.write(args.iformat).strip('\n')
        #    else:
        #        output.append(str(index) + ",\n")
        # else:
        #    output.append(str(index) + ",\n")
    print(output)

    if args.idx:
        for line in output:
            outfile.write(line + '\n')
    else:
        for line in output:
            string = line[line.find(",") + 1:]
            if string:
                outfile.write(pybel.readstring(args.iformat, string))


def __main__():
    """
        Remove any counterion and delete any fragment but the largest one for each molecule.
    """
    args = parse_command_line()
    remove_ions(args)


if __name__ == "__main__":
    __main__()
