import sys
import pandas as pd

"""
Renumbers pdb file as follows:
* uses 2nd and 6th column (atom id, residue id)
* needs infile, outfile, atom id start, resdiue id start as parameters in that order
"""

def renumber(infile, outfile, atid_start, resid_start, chain):
    # "ATOM   1387  N   ASN B  26     -39.683  -8.929 -66.762  1.00 27.36      B    N  "
    # columns 7 - 11         Integer       serial       Atom  serial number.
    # columns 23 - 26        Integer       resSeq       Residue sequence number.

    last_resid = None
    resid = resid_start
    n = 0
    with open(infile, 'r') as ifile, open(outfile, 'w') as ofile:
        for line in ifile:
            #print("line.startswith('ATOM') [{}] or line.startswith('TER') [{}] or line.startswith('HETATM') [{}] or (line.strip()) == '') [{}] -> {}".format(line.startswith('ATOM') , line.startswith('TER') , line.startswith('HETATM') , ((line.strip()) == ''), (line.startswith('ATOM') or line.startswith('TER') or line.startswith('HETATM') or (line.strip()) == '')))
            if not (line.startswith('ATOM') or line.startswith('TER') or line.startswith('HETATM') or (line.strip()) == ''):
                print('Line {} does not start with ATOM or TER:\n{}'.format(n, line))
                #raise NotImplementedError
                continue
            if line.startswith('TER'):
                ofile.write('TER\n')
                continue
            if line.strip() == '':
                continue
            if not last_resid:  # just init
                last_resid = int(line[22:26].strip())

            # next resid?
            if last_resid != int(line[22:26].strip()):
                resid += 1

            last_resid = int(line[22:26].strip())
            atid = atid_start + n

            if chain:
                o_line = line[:7] + '{:>4}'.format(atid) + line[11:21] + chain + '{:>4}'.format(resid) + line[26:]
            else:
                o_line = line[:7] + '{:>4}'.format(atid) + line[11:22] + '{:>4}'.format(resid) + line[26:]

            ofile.write(o_line)
            n += 1


if __name__ == '__main__':
    chain = None
    infile = sys.argv[1]
    outfile = sys.argv[2]

    atid_start = int(sys.argv[3])
    resid_start = int(sys.argv[4])

    try:
        chain = sys.argv[5]
    except IndexError:
        pass

    print('Renumbering {} to {} with atom id start {} and residue id start {}'.format(infile,
                                                                                      outfile,
                                                                                      atid_start,
                                                                                      resid_start))
    if chain:
        if len(chain) !=1:
            print('The chain has to be one character only.')
            raise AttributeError
        print('Setting chain to {}'.format(chain))
    renumber(infile, outfile, atid_start, resid_start, chain)
    print('Find the renumbered file at {}'.format(outfile))
