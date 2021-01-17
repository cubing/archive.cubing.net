#!/usr/bin/python

import sys
import operator
RGC = 0.25
UC = 0.12
UPC = 0.09
U2C = 0.23
RC = 0.08
RPC = 0.08
R2C = 0.14
FC = 0.1
FPC = 0.19
F2C = 0.3
DC = 0.1
D2C = 0.35
DPC = 0.1
BC = 0.15
B2C = 0.35
BPC = 0.1
SGC = 0.15

def mincost(alg):
    ialg = alg.replace('(', '')
    ialg = ialg.replace(')', '')
    ialg = ialg.replace("2'", '2')
    ialg = ialg.replace('  ', ' ')
    ialg = ialg.replace('u', 'U')
    ialg = ialg.replace('r', 'R')
    ialg = ialg.replace('d', 'D')
    ialg = ialg.replace('f', 'F')
    ialg = ialg.replace('b', 'B')
    ialg = ialg.replace('l', 'L')
    ialg = ialg.replace('M', 'R')
    ialg = ialg.replace('S', 'F')
    ialg = ialg.replace('E', 'D')
    parts = ialg.split(' ')
    return sorted([cost(0, parts, 'G0 '),
     cost(1, parts, 'G1 '),
     cost(2, parts, 'G2 ')], key=operator.itemgetter(1))[0]



def LstToAlg(lst):
    str = ' '.join(lst)
    str = str.replace('L x', 'r')
    str = str.replace('x L', 'r')
    str = str.replace("L' x'", "r'")
    str = str.replace("x' L'", "r'")
    str = str.replace('L2 x2', 'r2')
    str = str.replace('x2 L2', 'r2')
    str = str.replace("R x'", 'l')
    str = str.replace("x' R", 'l')
    str = str.replace("R' x", "l'")
    str = str.replace("x R'", "l'")
    str = str.replace('x2 R2', 'l2')
    str = str.replace('R2 x2', 'l2')



def generateVariations(alg, maxRot = 3):
    rots = ['x',
     "x'",
     'x2',
     'y',
     "y'",
     'y2',
     'z',
     "z'",
     'z2']
    for rot in rots:
        for p in range(0, len(alg)):
            r = list(alg)
            r[p] = ((rot + ' ') + r[p])
            yield r





def mirrorF(alg, times = 1):
    if ((times % 2) == 0):
        return alg
    else:
        if (alg == 'R'):
            return "L'"
        if (alg == "R'"):
            return 'L'
        if (alg == 'R2'):
            return 'L2'
        if (alg == "L'"):
            return 'R'
        if (alg == 'L'):
            return "R'"
        if (alg == 'L2'):
            return 'R2'
        if (alg[0] == 'G'):
            return alg
        if (alg[-1] == "'"):
            return alg[:-1]
        elif (alg[-1] == '2'):
            return alg
        else:
            return (alg + "'")



def postProcess(alg):
    res = ''
    parts = alg.split(' ')
    c = 0
    for p in parts:
        if (p == ''):
            pass
        elif (p == '!'):
            c += 1
            res += '! '
        else:
            res += (mirrorF(p, c) + ' ')

    return res



def cost(grip, alg, p = '', c = 0.0, rh = True):
    if (len(alg) == 0):
        return (postProcess(p),
         c)
    cur = alg[0]
    nalg = alg[1:]
    if rh:
        cur = mirrorF(cur)
    if (cur[0] == 'R'):
        if ((grip == 0) and (cur == 'R')):
            return cost(1, nalg, (p + 'R '), (c + RC), rh)
        if ((grip == 0) and (cur == "R'")):
            return sorted([cost(1, alg, (p + 'G1 '), (c + RGC), rh),
             cost(2, alg, (p + 'G2 '), (c + RGC), rh)], key=operator.itemgetter(1))[0]
        if ((grip == 0) and (cur == 'R2')):
            return cost(2, nalg, (p + 'R2 '), (c + R2C), rh)
        if ((grip == 1) and (cur == 'R')):
            return cost(2, nalg, (p + 'R '), (c + RC), rh)
        if ((grip == 1) and (cur == "R'")):
            return cost(0, nalg, (p + "R' "), (c + RPC), rh)
        if ((grip == 1) and (cur == 'R2')):
            return sorted([cost(0, alg, (p + 'G0 '), (c + RGC), rh),
             cost(2, alg, (p + 'G2 '), (c + RGC), rh)], key=operator.itemgetter(1))[0]
        if ((grip == 2) and (cur == 'R')):
            return sorted([cost(0, alg, (p + 'G0 '), (c + RGC), rh),
             cost(1, alg, (p + 'G1 '), (c + RGC), rh)], key=operator.itemgetter(1))[0]
        if ((grip == 2) and (cur == "R'")):
            return cost(1, nalg, (p + "R' "), (c + RPC), rh)
        if ((grip == 2) and (cur == 'R2')):
            return cost(0, nalg, (p + 'R2 '), (c + R2C), rh)
    elif (cur[0] == 'F'):
        if ((grip == 0) and (cur == 'F')):
            return cost(0, nalg, (p + 'F '), (c + FC), rh)
        if ((grip == 0) and (cur == "F'")):
            return cost(0, nalg, (p + "F' "), (c + FPC), rh)
        if ((grip == 0) and (cur == 'F2')):
            return cost(0, nalg, (p + 'F2 '), (c + F2C), rh)
        return cost(0, alg, (p + 'G0 '), (c + RGC), rh)
    elif (cur[0] == 'D'):
        if (cur == 'D'):
            return cost(grip, nalg, (p + 'D '), (c + DC), rh)
        if (cur == 'D2'):
            return cost(grip, nalg, (p + 'D2 '), (c + D2C), rh)
        if ((grip == 0) and (cur == "D'")):
            return cost(1, alg, (p + 'G1 '), (c + RGC), rh)
        if ((grip == 1) and (cur == "D'")):
            return cost(1, nalg, (p + "D' "), (c + DPC), rh)
        if ((grip == 2) and (cur == "D'")):
            return cost(1, alg, (p + 'G1 '), (c + RGC), rh)
    elif (cur[0] == 'U'):
        if (cur == "U'"):
            return cost(grip, nalg, (p + "U' "), (c + UPC), rh)
        if (grip == 0):
            return cost(1, alg, (p + 'G1 '), (c + RGC), rh)
        if (grip == 2):
            return cost(1, alg, (p + 'G1 '), (c + RGC), rh)
        if ((grip == 1) and (cur == 'U')):
            return cost(1, nalg, (p + 'U '), (c + UC), rh)
        if ((grip == 1) and (cur == 'U2')):
            return cost(1, nalg, (p + 'U2 '), (c + U2C), rh)
    elif (cur[0] == 'B'):
        if (grip == 1):
            return sorted([cost(0, alg, (p + 'G0 '), (c + RGC), rh),
             cost(2, alg, (p + 'G2 '), (c + RGC), rh)], key=operator.itemgetter(1))[0]
        if ((grip == 0) and (cur == "B'")):
            return cost(0, nalg, (p + "B' "), (c + BPC), rh)
        if ((grip == 0) and (cur == 'B2')):
            return cost(0, nalg, (p + 'B2 '), (c + B2C), rh)
        if ((grip == 0) and (cur == 'B')):
            return cost(2, alg, (p + 'G2 '), (c + RGC), rh)
        if ((grip == 2) and (cur == 'B')):
            return cost(2, nalg, (p + 'B '), (c + BC), rh)
        if ((grip == 2) and (cur == 'B2')):
            return cost(2, nalg, (p + 'B2 '), (c + B2C), rh)
        if ((grip == 2) and (cur == "B'")):
            return cost(0, alg, (p + 'G0 '), (c + RGC), rh)
    elif (cur[0] == 'L'):
        if (grip == 1):
            return cost(1, alg, (p + '! '), (c + SGC), (not rh))
        if ((grip == 0) or (grip == 2)):
            return cost(1, alg, (p + 'G1 '), (c + RGC), rh)
    else:
        print (('WTF UNEXPECTED LITERAL ERROR: ' + `cur`) + '. IGNORING LITERAL.')
        return cost(grip, nalg, p, c, rh)


if (__name__ == '__main__'):
    if (len(sys.argv) > 1):
        print mincost(' '.join(sys.argv[1:]))
    else:
        print 'Blank parameter. Enter an algorithm as argument to the program.'

#+++ okay decompyling
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
