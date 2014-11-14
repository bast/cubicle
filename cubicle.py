#!/usr/bin/env python

import sys
import string
from optparse import OptionParser

#-------------------------------------------------------------------------------

def parse_args(argv):

    usage = '''
      %prog: utility to add/subtract/scale cube files
      example: ./%prog --calc="0.5*example.cube -0.5*example.cube"'''

    parser = OptionParser(usage)

    parser.add_option('--calc',
                      help = 'cubes with prefactors',
                      metavar='"f*cube1 g*cube2 h*cube3 ..."')

    (options, args) = parser.parse_args()

    if len(argv) == 1:
        # user has given no arguments: print help and exit
        print(parser.format_help().strip())
        sys.exit()

    return options

#-------------------------------------------------------------------------------

def file_to_array(s1):

    s1 = string.split(s1, '\n')
    s2 = ''
    for i in range(len(s1)):
        if i > 1:
            s2 += string.replace(s1[i], '\n', ' ')
    for x in range(10):
        s2 = string.replace(s2, '  ', ' ')

    return string.split(s2, ' ')

#-------------------------------------------------------------------------------

def compute_cube(calc):

    f_l = []
    cube_l = []
    for word in calc.split():
        a = word.split('*')
        f_l.append(float(a[0]))
        with open(a[1], 'r') as f:
            cube_l.append(file_to_array(f.read()))

    nr_atoms = int(cube_l[0][1])

    dim_x = int(cube_l[0][ 5])
    dim_y = int(cube_l[0][ 9])
    dim_z = int(cube_l[0][13])

    first = 17 + nr_atoms*5

    new_cube = []
    for i in range(len(cube_l[0])):
        if i < first:
            new_cube.append(cube_l[0][i])
        else:
            new_cube.append(0.0)
            for j in range(len(cube_l)):
                new_cube[i] += f_l[j]*float(cube_l[j][i])

    output = []

    header = open(calc.split()[0].split('*')[-1]).readlines()
    for x in range(6 + nr_atoms):
        output.append(string.replace(header[x], '\n', ''))

    index = first
    for i in range(dim_x):
        for j in range(dim_y):
            s = ''
            count = 0
            for k in range(dim_z):
                if count < 6:
                    s += '%13.5e' % new_cube[index]
                    count += 1
                else:
                    output.append(s)
                    s = '%13.5e' % new_cube[index]
                    count = 1
                if k == dim_z - 1:
                    output.append(s)
                index += 1

    return '\n'.join(output)

#-------------------------------------------------------------------------------

def test_compute_cube():

    calc = "0.5*example.cube -0.25*example.cube -0.25*example.cube"
    result = compute_cube(calc)
    with open('zero.cube', 'r') as f:
        reference = f.read()
    result += '\n'
    same = (result == reference)
    assert(same)

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    options = parse_args(sys.argv)
    print(compute_cube(options.calc))
