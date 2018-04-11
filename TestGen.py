#!/usr/bin/python
import sys

if len(sys.argv) <= 2:
	print "Missing arguments. Terminating."
else:
	if len(sys.argv) > 3:
		print "Ignoring exceeding arguments."
	n = int(sys.argv[1])
	if n < 0:
		print "First argument must be greater or equal than zero. Terminating."
	else:
		clocks = int(sys.argv[2])
		if clocks <= 0:
			print "Second argument must be greater than zero. Terminating."
		else:
			file = open("test","w")
			print "Generating CTA with " + str(n) + " states and " + str(clocks) + " clocks." 
			gr = ""
			gs = ""
			rst = "{"
			for i in xrange(clocks - 1):
				gr = gr + "x" + str(i) + " < 1000 & "
				gs = gs + "x" + str(i) + " == 1000 & "
				rst = rst + "x" + str(i) + "; "
			gr = gr + "x" + str(clocks - 1) + " < 1000"
			gs = gs + "x" + str(clocks - 1) + " == 1000"
			rst = rst + "x" + str(clocks - 1) + "}"

			file.write("Cta A = {\n") 
			file.write("Init q0;\n")
			for i in xrange(n - 1):
				file.write("q" + str(i) + " pq!a(" + gs + "," + rst + ") q" + str(i + 1) + ";\n") 
				file.write("q" + str(i) + " pq?b(" + gr + "," + rst + ") q" + str(i + 1) + ";\n")
			#file.write("q" + str(n - 2) + " pq!a(" + gs + "," + rst + ") q" + str(n - 1) + ";\n") 
			#file.write("q" + str(n - 2) + " pq?b(" + gr + "," + rst + ") q" + str(n - 1) + "\n")
			file.write("};\n\n")
			#file.write("Cta B = {\n") 
			#file.write("Init q0;\n")
			#for i in xrange(n - 1):
			#	file.write("q" + str(i) + " pq!a(" + gs + "," + rst + ") q" + str(i + 1) + ";\n") 
			#	file.write("q" + str(i) + " pq?b(" + gr + "," + rst + ") q" + str(i + 1) + ";\n")
			#file.write("q" + str(n - 1) + " pq!a(" + gs + "," + rst + ") q" + str(n) + ";\n") 
			#file.write("q" + str(n - 1) + " pq?b(" + gr + "," + rst + ") q" + str(n) + "\n")
			#file.write("};\n\n")
			file.write("A refines? A;") 
			file.close() 
			print "Done."
