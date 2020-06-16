#!/usr/bin/python
from CtaParser import *
import sys

if len(sys.argv) <= 1:
	print "No input file provided. Terminating."
else:
	if len(sys.argv) > 2:
		print "Ignoring exceeding arguments."
	scriptFile = sys.argv[1]
	refinementChecker(scriptFile)
