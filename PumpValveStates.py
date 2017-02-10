

import csv
import time

PVS = False
V1 = 0
V2 = 0
V3 = 0
V4 = 0
P1 = 0
P2 = 0
P3 = 0
P4 = 0
P5 = 0
P6 = 0
start = 0
stop1 = 0
stop2 = 0
stop3 = 0
stop4 = 0
stop5 = 0
stop6 = 0

def fileStart(filename,assayStart):
    global start
    global matrix
    start = assayStart
    matrix = [[]]


def fileStop():
    with open('PVS.csv',"wb") as f:
        writer = csv.writer(f)
        f.write('Time(s),V1,V2,V3,V4,B1,B2,B3,B4,B5,B6')
        writer.writerows(matrix)

def change():
    global matrix
    sec = round(time.time()-start, 2)
    list = [sec,V1,V2,V3,V4,P1,P2,P3,P4,P5,P6]
    matrix.append (list)

def valveOpen(V):
    change()
    global V1,V2,V3,V4
    if V == 'V1':
        V1 = 1
    if V == 'V2':
        V2 = 1
    if V == 'V3':
        V3 = 1
    if V == 'V4':
        V4 = 1
    change()

def valveClose(V):
    global V1,V2,V3,V4
    change()
    if V == 'V1':
        V1 = 0
    if V == 'V2':
        V2 = 0
    if V == 'V3':
        V3 = 0
    if V == 'V4':
        V4 = 0
    change()

def pumpStart(P, rate, vol):
    global P1, P2, P3, P4, P5, P6, stop1, stop2, stop3,stop4,stop5,stop6
    change()
    if P == 'B1':
        P1 = rate
    if P == 'B2':
        P2 = rate
    if P == 'B3':
        P3 = rate
    if P == 'B4':
        P4 = rate
    if P == 'B5':
        P5 = rate
    if P == 'B6':
        P6 = rate
    change()

def pumpStop(P):
    global P1, P2, P3, P4, P5, P6, stop1, stop2, stop3,stop4,stop5,stop6
    change()
    if P == 'B1':
        P1 = 0
    if P == 'B2':
        P2 = 0
    if P == 'B3':
        P3 = 0
    if P == 'B4':
        P4 = 0
    if P == 'B5':
        P5 = 0
    if P == 'B6':
        P6 = 0
    change()

