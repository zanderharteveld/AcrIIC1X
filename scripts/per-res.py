import pymol
from pymol import cmd
from pymol import stored
import pandas as pd
from io import StringIO
import numpy as np



def per_res(obj, score, column, min_val=None, max_val=None):
    print('per-res called with parameters\nobj:    {}\nscore:  {}\ncolumn: {}\n'.format(obj, score, column))

    try:
        if stored.obj == obj and stored.score == score:
            print('Using values from memory.')
        else:
            raise AttributeError
    except AttributeError:
        stored.obj = obj
        stored.score = score

        score_lines = ""
        empty = 100
        with open(score, 'r') as ifile:
            while True:
                line = ifile.readline()
                if line.startswith('#BEGIN_POSE_ENERGIES_TABLE'):
                    break
                if len(line) == 0:
                    empty -= 1
                    if emtpy == 0:
                        print('file invalid, no POSE_ENERGIES_TABLE')
                        return

            while True:
                line = ifile.readline()
                if line.startswith('#END_POSE_ENERGIES_TABLE'):
                    break
                if len(line) == 0:
                    empty -= 1
                    if emtpy == 0:
                        print('file invalid, no POSE_ENERGIES_TABLE')
                        return
                score_lines += line

        stored.df = pd.read_table(StringIO(score_lines), sep=' ', index_col='label')


    if not min_val:
        min_val = np.nanpercentile(stored.df[column], 1) #np.nanmin(stored.df[column].iloc[1:])
    if not max_val:
        max_val = np.nanpercentile(stored.df[column], 99) #np.nanmax(stored.df[column].iloc[1:])

    stored.r = 1
    stored.last_resi="{}-{}".format('x', 'X')
    stored.new_resi="{}-{}".format("x", "X")
    stored.column = column

    def assign(resn, resi):
        stored.new_resi = "{}-{}".format(resn, resi)
        if stored.new_resi != stored.last_resi:
            stored.r += 1
            stored.last_resi = "{}-{}".format(resn, resi)
            #print(stored.new_resi[:3] + ' ' + stored.df.index[stored.r] + '   ' + str(stored.df.index[stored.r][:3] == stored.new_resi[:3]) + ' ' + str(stored.df[stored.column].iloc[stored.r]))

        if stored.df.index[stored.r][:3] == stored.new_resi[:3]:
            return stored.df[stored.column].iloc[stored.r]
        else:
            return -1000

    stored.assign = assign
    cmd.alter(obj, 'b = stored.assign(resn, resi)')
    cmd.spectrum("b", "green_red", obj, min_val, max_val)
    cmd.select("nan", "b=-1000")
    cmd.color("grey", "nan")

    print('Coloring from {} to {}'.format(min_val, max_val))
    print('Available scores:')
    print(', '.join(stored.df.columns))
    print('\nPercentiles for {}:'.format(column))
    print('\n'.join(['{:>7} -> {:.1f}'.format(str(p) + ' %', np.nanpercentile(stored.df[column], p)) for p in np.linspace(0, 100, 11)]))

    print('Maybe use:\n\n{}\n'.format('label sele and name CA, "{}{}: {:.3f}".format(resi, resn, b)'))


cmd.extend("per-res", per_res)

"""
cd /Users/JUzB/Documents/epfl/mount_scratch/denovo/downstream/2W2W_A_8/pdbs_test/
load 2W2W_A_8.rp_0001.pdb
run /Users/JUzB/libraries/masif/per-res.py; per-res 2W2W_A_8.rp_0001, sc_2W2W_A_8.rp_0001_0001.pdb, total

"""