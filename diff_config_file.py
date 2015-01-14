#!/usr/bin/env python
#diff config files

import os, sys, difflib

config_file1 = os.sys.path[0] + os.sep + 'config_file1.txt'
config_file2 = os.sys.path[0] + os.sep + 'config_file2.txt'
output_file = os.sys.path[0] + os.sep + 'config_file1_file2.html'

def readfile(filename):
    try:
        fileHandle = open(filename, 'r')
        text = fileHandle.read().splitlines()
        fileHandle.close()
        return text
    except IOError as error:
        print "Read file error" + str(error)
        sys.exit()

if config_file1 == "" or config_file2 == "":
    print "Config file empty"
    sys.exit()

file1_lines = readfile(config_file1)
file2_lines = readfile(config_file2)

diff = difflib.HtmlDiff()
diff_html = diff.make_file(file1_lines, file2_lines)
f = open(output_file,'w')
f.write(str(diff_html))
f.close()
