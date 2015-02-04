#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,time,subprocess
import warnings,logging
from scapy.all import traceroute

warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
domains = raw_input('Please input one or more IP/domain: ')
target =  domains.split(' ')
dport = [80]
if len(target) >= 1 and target[0]!='':
    res,unans = traceroute(target,dport=dport,retry=-2)
    res.graph(target="> test.svg")
    time.sleep(1)
    output = target[0] + '.png'
    subprocess.Popen(["/usr/bin/convert", "test.svg", output])
else:
    print "IP/domain number of errors,exit"
