#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import csv
import sys,os

input_file = sys.argv[1]
#input_file = os.sys.path[0] + os.sep + 'sample.csv'
cost = {}
f = open(input_file,'rb')
reader = csv.reader(f, delimiter=",", quotechar='"')
for i in reader:
    try:
        unblended_cost = float(i[20])
    except ValueError:
        unblended_cost = 0.0
    try:
        project = i[22]
    except IndexError:
        project = ""
    cost[project] = float(cost.get(project,0)) + unblended_cost

sorted_cost = sorted(cost.iteritems(), key=lambda d:d[1], reverse=True)
for i,j in sorted_cost:
    print i,"\t",j
