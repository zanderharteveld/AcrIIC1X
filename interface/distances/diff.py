import sys


def dist(x, y, z, coord):
    x2, y2, z2 = [float(c) for c in coord.split(',')]
    return ((x-x2)**2+(y-y2)**2+(z-z2)**2)**.5


def diff(in1, which1, in2, which2, out, cutoff, x, y, z):
    start = "core.scoring.sc.ShapeIdentityCalculator: DISTMIN"
    end = "0.0,0.0,0.0\n"

    matches = 0
    mismatches = 0
    cut = 0
    coord2val = {}

    if not in1 == "None":
        with open(in1, 'r') as i1:
            while(which1 > 0):
                line = i1.readline()
                if "SHAPESCORE" in line:
                    which1 -= 1
            # load 1 in memory:
            for line in i1:
                if "SHAPESCORE" in line:
                    break
                if "SISCORE" in line or "DISTMIN" in line:
                    split = line.split(',')
                    coord = ",".join(split[2:5])
                    val = split[1]
                    coord2val[coord] = val

    with open(in2, 'r') as i2, open(out, 'w') as o:
        while(which2 > 0):
            line = i2.readline()
            if "SHAPESCORE" in line:
                which2 -= 1



        o.write("SHAPESCORE differences\n")

        for line in i2:
            if "SHAPESCORE" in line:
                break
            if "SISCORE" in line or "DISTMIN" in line:
                split = line.split(',')
                coord = ",".join(split[2:5])
                val = split[1]



                try:
                    if dist(x, y, z, coord) > cutoff:
                        diff = 0.0
                        cut += 1
                        continue
                    else:
                        if len(coord2val) > 0:
                            diff = float(val) - float(coord2val[coord])
                        else:
                            diff = float(val)
                    o.write('{},{:.6f},{},{}'.format(start, diff, coord, end))
                    matches += 1
                except KeyError:
                    mismatches += 1

    print('{} / {} ({:.1f} %) matches.'.format(matches, matches + mismatches, 100*(matches/(matches+mismatches))))
    print('{} / {} ({:.1f} %) cut off.'.format(cut, matches + mismatches, 100*(cut/(matches+mismatches))))

if __name__ == '__main__':
    in1 = sys.argv[1]
    which1 = int(sys.argv[2])
    in2 = sys.argv[3]
    which2 = int(sys.argv[4])

    out = sys.argv[5]
    cutoff = float(sys.argv[6])
    x = float(sys.argv[7])
    y = float(sys.argv[8])
    z = float(sys.argv[9])

    diff(in1, which1, in2, which2, out, cutoff, x, y, z)

    print('DONE')
