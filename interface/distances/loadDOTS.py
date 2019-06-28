# Pablo Gainza Cirauqui 2016 
# This pymol function loads dot files into pymol. 
# (2018) Modified by Andreas Scheck to load surface similarity scores.
# (2019) Modified by Julius Upmeier zu Belzen to add a normalization feature

from pymol import cmd, stored
import sys, urllib, zlib
import subprocess
import os,math,re
import string
from pymol.cgo import *
from subprocess import Popen, PIPE
#import pymesh
#import Queue
import threading
import os.path
#from utils.xyzrn import *
#from scipy.spatial import distance
import numpy as np
import collections

colorDict = {
'red': [COLOR,  1.0, 0.0, 0.0 ],
'tv_red': [COLOR, 1.0 ,  0.2, 0.2 ],
'raspberry': [COLOR, 0.70, 0.30, 0.40 ],  
'darksalmon': [COLOR, 0.73, 0.55, 0.52 ],
'salmon': [COLOR, 1.0, 0.6, 0.6 ],
'deepsalmon': [COLOR, 1.00, 0.42, 0.42 ],  
'warmpink': [COLOR, 0.85, 0.20, 0.50 ],
'firebrick': [COLOR, 0.698, 0.13, 0.13 ],
'ruby': [COLOR, 0.6, 0.2 ,  0.2 ],
'chocolate': [COLOR, 0.555, 0.222, 0.111 ],  
'brown': [COLOR, 0.65, 0.32, 0.17 ],
'green': [COLOR, 0.0, 1.0, 0.0 ],
'tv_green': [COLOR, 0.2, 1.0, 0.2 ],  
'chartreuse': [COLOR, 0.5, 1.0, 0.0 ],  
'splitpea': [COLOR, 0.52, 0.75 ,  0.00 ],  
'smudge': [COLOR, 0.55, 0.70, 0.40 ],
'palegreen': [COLOR, 0.65, 0.9, 0.65 ],  
'limegreen': [COLOR, 0.0, 1.0, 0.5 ],
'lime': [COLOR, 0.5, 1.0 ,  0.5 ],
'limon': [COLOR, 0.75, 1.00, 0.25 ],
'forest': [COLOR, 0.2, 0.6, 0.2 ],
'blue': [COLOR, 0.0, 0.0, 1.0 ],
'tv_blue': [COLOR, 0.3, 0.3, 1.0 ],
'marine': [COLOR, 0.0, 0.5, 1.0 ],
'slate': [COLOR, 0.5, 0.5, 1.0 ],
'lightblue': [COLOR, 0.75, 0.75, 1.0 ],  
'skyblue': [COLOR, 0.20, 0.50, 0.80 ],
'purpleblue': [COLOR, 0.5, 0.0, 1.0 ],  
'deepblue': [COLOR, 0.25, 0.25, 0.65 ],  
'density': [COLOR, 0.1 ,  0.1, 0.6 ],
'yellow': [COLOR, 1.0 ,  1.0, 0.0 ],
'tv_yellow': [COLOR, 1.0, 1.0, 0.2 ],  
'paleyellow': [COLOR, 1.0, 1.0, 0.5 ],
'yelloworange': [COLOR, 1.0, 0.87, 0.37 ],
'limon': [COLOR, 0.75, 1.00, 0.25 ],
'wheat': [COLOR, 0.99, 0.82, 0.65 ],
'sand': [COLOR, 0.72, 0.55, 0.30 ],
'magenta': [COLOR, 1.0, 0.0, 1.0 ],
'lightmagenta': [COLOR, 1.0 ,  0.2, 0.8 ],
'hotpink': [COLOR, 1.0, 0.0, 0.5 ],
'pink': [COLOR, 1.0, 0.65, 0.85 ],
'lightpink': [COLOR, 1.00 ,  0.75, 0.87 ],
'dirtyviolet': [COLOR, 0.70, 0.50, 0.50 ],  
'violet': [COLOR, 1.0, 0.5, 1.0 ],
'violetpurple': [COLOR, 0.55, 0.25, 0.60 ],
'purple': [COLOR, 0.75, 0.00, 0.75 ],
'deeppurple': [COLOR, 0.6, 0.1, 0.6 ],  
'cyan': [COLOR, 0.0, 1.0, 1.0 ],
'palecyan': [COLOR, 0.8, 1.0, 1.0 ],
'aquamarine': [COLOR, 0.5, 1.0, 1.0 ],
'greencyan': [COLOR, 0.25, 1.00, 0.75 ],  
'teal': [COLOR, 0.00, 0.75, 0.75 ],
'deepteal': [COLOR, 0.1, 0.6, 0.6 ],  
'lightteal': [COLOR, 0.4, 0.7, 0.7 ],  
'orange': [COLOR, 1.0 ,  0.5, 0.0 ],
'tv_orange': [COLOR, 1.0, 0.55, 0.15 ],
'brightorange': [COLOR, 1.0, 0.7, 0.2 ],  
'lightorange': [COLOR, 1.0, 0.8, 0.5 ],
'yelloworange': [COLOR, 1.0, 0.87, 0.37], 
'olive': [COLOR, 0.77, 0.70, 0.00 ],
'deepolive ': [COLOR,  0.6, 0.6, 0.1 ],  
'wheat': [COLOR, 0.99, 0.82, 0.65 ],
'palegreen': [COLOR,  0.65, 0.9, 0.65 ],
'palergreen': [COLOR,  0.81, 0.9, 0.81 ],
'lightblue': [COLOR,  0.75, 0.75, 1.0 ],  
'paleyellow': [COLOR, 1.0, 1.0 ,  0.5 ],  
'lightpink ': [COLOR,  1.00, 0.75, 0.87],  
'palecyan': [COLOR, 0.8, 1.0, 1.0],  
'lightorange': [COLOR, 1.0, 0.8, 0.5 ],
'bluewhite': [COLOR, 0.85, 0.85, 1.00 ],
'white': [COLOR, 1.0, 1.0, 1.0 ],  
'grey90': [COLOR, 0.9, 0.9, 0.9 ],  
'grey80': [COLOR, 0.8, 0.8, 0.8 ],  
'grey70': [COLOR, 0.7, 0.7, 0.7 ],  
'grey60': [COLOR, 0.6, 0.6, 0.6 ],  
'grey50': [COLOR, 0.5, 0.5, 0.5 ],  
'grey40': [COLOR, 0.4, 0.4, 0.4 ],  
'grey30': [COLOR, 0.3, 0.3, 0.3 ],  
'grey20': [COLOR, 0.2, 0.2, 0.2],  
'grey10': [COLOR, 0.1, 0.1, 0.1] ,  
'black': [COLOR, 0.0, 0.0, 0.0]
}
def load_dots_heatmap(filename, which=1, norm=0, min_val=None, max_val=None, t=None, invert=-1, name='ply', dotSize=0.2, lineSize = 0.5, doStatistics=False):

    # casting:
    norm = int(norm)
    if min_val:
        min_val = float(min_val)
    if max_val:
        max_val = float(max_val)
    if t == 'None':
        t = None
    if t:
        t = float(t)

    invert = float(invert)

    lines = open(filename).readlines()
    lines = [line.rstrip() for line in lines]
    shapescore = 0
    lines_surf1 = []
    lines_surf2 = []
    for line in lines:
        if "SHAPESCORE" in line:
            shapescore += 1
        if shapescore == 1 and ("SISCORE" in line or "DISTMIN" in line):
            lines_surf1.append(line.split(','))
        if shapescore == 2 and ("SISCORE" in line or "DISTMIN" in line):
            lines_surf2.append(line.split(','))
    verts_surf1 = [(float(x[2]), float(x[3]), float(x[4]), float(x[1])) for x in lines_surf1]
    verts_surf2 = [(float(x[2]), float(x[3]), float(x[4]), float(x[1])) for x in lines_surf2]
    print('1: {}\n2: {}'.format(len(verts_surf1), len(verts_surf2)))

    color_palette = {0: 'firebrick',
    0.1: 'red',
    0.2: 'orange',
    0.3: 'brightorange',
    0.4: 'yellow',
    0.5: 'limon',
    0.6: 'olive',
    0.7: 'splitpea',
    0.8: 'forest',
    0.9: 'palegreen',
    -1: 'skyblue',
    99: 'grey40'}
  # Draw vertices
    
    obj = []

    if int(which) == 2:
        verts_surf = verts_surf2
        print('Drawing 2')
    else:
        verts_surf = verts_surf1
        print('Drawing 1')

    values = [verts_surf[v_ix][3] for v_ix in range(len(verts_surf))]
    if not min_val:
        min_val = min(values)
    if not max_val:
        max_val = max(values)
    print('norm: {}, min_val: {}, max_val: {}, t: {}, length {}'.format(norm, min_val, max_val, t, len(values)))

    percentiles = range(0, 110, 10)
    print('Percentiles:\n{}'.format('\n  '.join(['{:.0f} %\t{:.3f}'.format(p, np.percentile(values, p)) for p in percentiles])))

    if int(norm) == 1:
        color_positions = np.linspace(min_val, max_val, 9)
    elif int(norm) == 2:
        color_positions = list(np.linspace(min_val, 0, 5)) + list(np.linspace(0, max_val, 5))[1:]
    else:
        color_positions = np.linspace(0.1, 0.9, 9)
    print('Color-scale: red -> {} -> green'.format(', '.join(['{:.3f}'.format(float(c)) for c in color_positions])))

    for v_ix in range(len(verts_surf)):
        vert = verts_surf[v_ix]

        val = -1 * invert * vert[3]

        if t:
            if val < t:
                colorToAdd = colorDict['firebrick']
            else:
                #colorToAdd = colorDict['white']
                colorToAdd = colorDict['palergreen']
        else:

            if val < color_positions[0]:
                colorToAdd = colorDict[color_palette[0]]
            elif val >= color_positions[0] and val < color_positions[1]:
                colorToAdd = colorDict[color_palette[0.1]]
            elif val >= color_positions[1] and val < color_positions[2]:
                colorToAdd = colorDict[color_palette[0.2]]
            elif val >= color_positions[2] and val < color_positions[3]:
                colorToAdd = colorDict[color_palette[0.3]]
            elif val >= color_positions[3] and val < color_positions[4]:
                colorToAdd = colorDict[color_palette[0.4]]
            elif val >= color_positions[4] and val < color_positions[5]:
                colorToAdd = colorDict[color_palette[0.5]]
            elif val >= color_positions[5] and val < color_positions[6]:
                colorToAdd = colorDict[color_palette[0.6]]
            elif val >= color_positions[6] and val < color_positions[7]:
                colorToAdd = colorDict[color_palette[0.7]]
            elif val >= color_positions[7] and val < color_positions[8]:
                colorToAdd = colorDict[color_palette[0.8]]
            elif val >= color_positions[8]:
                colorToAdd = colorDict[color_palette[0.9]]
            else:
                print('negative', val)
                colorToAdd = colorDict[color_palette[-1]]

        # Vertices
        obj.extend(colorToAdd)
        obj.extend([SPHERE, vert[0], vert[1], vert[2], dotSize])

        obj.extend(colorToAdd)
        obj.extend([SPHERE, vert[0], vert[1], vert[2], dotSize])


    name = "vert_"+filename+"_surface_2"
    group_names = name
    cmd.load_cgo(obj,name, 1.0)

cmd.extend('loaddots', load_dots_heatmap)

#load_dots_heatmap("acr_vs_sau_int.log", norm=2)
#load_dots_heatmap("acr_vs_nme_int.log", norm=2)
#load_dots_heatmap("nme_vs_sau.log", norm=2)



