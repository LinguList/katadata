#!C:/Python27/python
import os, sys
import site
import logging
import logging.config
import cgi, cgitb

sys.path.insert(0,'C:/python27/lingpy-2.5')
#logging.config.fileConfig('/home/ec2-user/logging.ini')
#cgitb.enable()
form = cgi.FieldStorage()
file = form.getvalue('filename')
#file = 'wordlist.qlc';
if form.getvalue('concept'):
	concept = form.getvalue('concept')
else:
	concept = 'all'
if form.getvalue('method'):
	_method = form.getvalue('method')
else:
	_method = 'lexstat'
if form.getvalue('cluster_method'):
	_cluster_method = form.getvalue('cluster_method')
else:
	_cluster_method = 'upgma'
print "Content-type: text/html"
print 
print '<html>'
print '<head>'
print '</head>'
print '<body>'
print '<h2>Concept:'+concept +'</h2>'
print '<h2>Method:'+_method +'</h2>'
print '<h2>Cluster:'+ _cluster_method +'</h2>'

from lingpy import *
file = "C:/xampp/htdocs/uploads/"+ str(file)
lex = LexStat(file)
lex.get_scorer()
lex.cluster(method=_method,cluster_method=_cluster_method, threshold=0.6, ref="cognates")
lex.output('qlc',filename='result',ignore=['scorer'])
lex.calculate('tree', ref='cognates')
print (lex.tree)
#print lex.tree.asciiArt()
print '</body>'
print '</html>'
