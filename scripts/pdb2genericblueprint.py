import sys

three2single = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
                'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
                'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W',
                'ALA': 'A', 'VAL': 'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}


def convert(infile, outfile, bdr):
    last_resid = None
    with open(infile, 'r') as ifile, open(outfile, 'w') as ofile:
        for line in ifile:
            if not line.startswith('ATOM'):
                continue

            resid = int(line[22:26].strip())

            aa = three2single[line[17:20]]
            if resid != last_resid:
                if last_resid:
                    ofile.write('\n{} {} . PIKAA {}'.format(resid, aa, aa))
                else:
                    ofile.write('{} {} . PIKAA {}'.format(resid, aa, aa))

            last_resid = resid

if __name__ == '__main__':
    infile = sys.argv[1]
    outfile = sys.argv[2]
    #bdr = sys.argv[3].lower in ['true', 't', 'yes', 'y', 'bdr']
    bdr = False
    convert(infile, outfile, bdr)
