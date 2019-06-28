import os
import sys
import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def main(infiles, outfile, prefixed):

    for infile in infiles:
        with open(infile, 'r') as json_in:
            data = json.load(json_in)

        prefixed_data = {}
        if prefixed:
            for p in prefixed:
                prefixed_data[p] = {}

        print('\n{}\n{}\n'.format(infile, '='*len(infile)))
        for key in sorted(data):
            pf = False
            for p in prefixed_data:
                if p in key:
                    prefixed_data[p][key.replace(p, '')] = data[key]
                    pf = True
                    break
            if not pf:
                print('{:>20}\t{:.3f}'.format(key, float(data[key])))

    fig, axes = plt.subplots(len(prefixed_data), 1, sharex=True)

    for n, p in enumerate(prefixed_data):
        key_list = list(sorted(prefixed_data[p]))
        for infile in infiles:
            p_data = [prefixed_data[p][k] for k in key_list]

            axes[n].plot(p_data, label=infile)

        axes[n].set_ylabel(p + '*')
        axes[n].xticklabels = key_list
        axes[n].xticks = range(len(key_list))

    axes[0].set_title('Per residue scores')

    plt.savefig(outfile)


if __name__ == '__main__':
    infiles = sys.argv[1].split(',')
    outfile = sys.argv[2]

    try:
        if sys.argv[3] in ['None', '-', '.']:
            prefixed = None
        else:
            prefixed = sys.argv[3].split(',')
    except IndexError:
        prefixed = None

    main(infile, outfile, prefixed)
