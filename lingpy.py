#!/usr/bin/python3.4

import os, sys
import site
import logging
import logging.config
import cgi, cgitb
#import pandas as pd
#import json

sys.path.insert(0,'/usr/local/lib/python3.4/site-packages/lingpy-2.5-py3.4.egg')
#logging.config.fileConfig('/home/ec2-user/logging.ini')
cgitb.enable()
form = cgi.FieldStorage()
file = form.getvalue('filename')
#file = 'wordlist.qlc';
if form.getvalue('method'):
	_method = form.getvalue('method')
else:
	_method = 'lexstat'
if form.getvalue('cluster_method'):
	_cluster_method = form.getvalue('cluster_method')
else:
	_cluster_method = 'upgma'
print('Content-type: text/html\r\n')
print('<html>')
print('<head>')
print('</head>')
print('<body>')
print('<h2>Method:'+_method +'</h2>')
print('<h2>Cluster:'+ _cluster_method +'</h2>')



from lingpy import *
from lingpy.sequence.sound_classes import sampa2uni
from glob import glob
from lingpy.compare.partial import Partial
D = {
        0 : ['concept', 'language', 'sampa_original', 'sampa', 'ipa', 'tokens']
        }
idx = 1

file = "/var/www/html/uploads/" +str(file)
csv = csv2list(file, strip_lines=False)
i = 0
while True:
    if csv[i][0] == 'ID':
        found = i
        break
    else:
        i += 1

reps = [("'", '?'),
        ('ù', 'u'),
        ('/', '?'),
        ('ø', 'o'),]

for i, line in enumerate(csv[i+1:]):
    if len(line) != 4:
        print('error in line {0} in file {1}'.format(i,'ss'))

    _, concept, language, sampa = line
    if sampa.strip() and sampa.strip() != '-':
        sampa_o = sampa
        sampas = sampa.split(',')
        for sampa in sampas:
            sampa = sampa.strip()
            for s, t in reps:
                sampa = sampa.replace(s, t)
            print(sampa)
            if sampa:
                ipa = sampa2uni(sampa)
                ipa = ipa.replace(' ', '_')
                tks = ipa2tokens(ipa, merge_vowels=False, semi_diacritics='')
                D[idx] = [concept, language, sampa_o, sampa, ipa, tks]
                idx += 1

wl = Wordlist(D)
wl.output('tsv', filename='an-data-wordlist', prettify=False, ignore='all')
lex = LexStat(wl)
print(lex.height, lex.width)
#lex.cluster(method=_method,cluster_method=_cluster_method, threshold=0.45)
lex.cluster(method='sca', threshold=0.45)
alm = Alignments(lex, ref='scaid')
alm.align()
alm.output('tsv', filename='an-data-aligned', prettify=False, ignore='all')
alm.output('html',filename='result')

lex = Partial('an-data-aligned.tsv');
lex.get_scorer(preprocessing=False,runs=10000)
lex.cluster(method=_method,cluster_method=_cluster_method,threshold=0.45)
lex.calculate('tree',ref='scaid')
print(lex.tree)
print('</body>')
print('</html>')
