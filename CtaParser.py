from parglare import Parser, Grammar
from python_dbm import Context
from DBMCta import *
from graphviz import Digraph
import sys,time

#from Cta import DBMTransition

#grammar = r"""
#Guard : Clock '<=' Nat
#| Clock '<' Nat
#| Guard '&' Guard {left}
#| '(' Guard ')';
#Clock : /[a-zA-Z]([a-zA-Z0-9_]*)?/;
#Nat : /\d+/;
#"""

class GuardTree:

	def __init__(self, op, children):
		self.op = op
		self.children = children

	def getClocks(self):
		if self.op == 'True':
			return set([])
		elif self.op == 'False':
			return set([])
		elif self.op == 'Leq':
			return set([self.children[0]])
		elif self.op == 'Lt':
			return set([self.children[0]])
		elif self.op == 'Geq':
			return set([self.children[0]])
		elif self.op == 'Gt':
			return set([self.children[0]])
		elif self.op == 'Eq':
			return set([self.children[0]])
		elif self.op == 'And':
			return self.children[0].getClocks() | self.children[1].getClocks()
		elif self.op == 'Or':
			return self.children[0].getClocks() | self.children[1].getClocks()
		else: 
			raise Exception("Invalid guard")

	def toDBM(self,context):
		if self.op == 'True':
			return true(context)
		elif self.op == 'False':
			return false(context)
		elif self.op == 'Leq':
			return context.__getitem__(self.children[0]) <= self.children[1]
		elif self.op == 'Lt':
			return context.__getitem__(self.children[0]) < self.children[1]
		elif self.op == 'Geq':
			return context.__getitem__(self.children[0]) >= self.children[1]
		elif self.op == 'Gt':
			return context.__getitem__(self.children[0]) > self.children[1]
		elif self.op == 'Eq':
			return context.__getitem__(self.children[0]) == self.children[1]
		elif self.op == 'And':
			return self.children[0].toDBM(context) & self.children[1].toDBM(context)
		elif self.op == 'Or':
			return self.children[0].toDBM(context) | self.children[1].toDBM(context)
		else: 
			raise Exception("Invalid guard")

	def toString(self, parenthesis):
		if self.op == 'True':
			return 'True'
		elif self.op == 'False':
			return 'False'
		elif self.op == 'Leq':
			return self.children[0] + " <= " + str(self.children[1])
		elif self.op == 'Lt':
			return self.children[0] + " < " + str(self.children[1])
		elif self.op == 'Geq':
			return self.children[0] + " >= " + str(self.children[1])
		elif self.op == 'Gt':
			return self.children[0] + " > " + str(self.children[1])
		elif self.op == 'Eq':
			return self.children[0] + " == " + str(self.children[1])
		elif self.op == 'And':
			if parenthesis:
				return "(" + self.children[0].toString(False) + " & " + self.children[1].toString(True) + ")"
			else:
				return self.children[0].toString(False) + " & " + self.children[1].toString(True)
		elif self.op == 'Or':
			if parenthesis:
				return "(" + self.children[0].toString(False) + " | " + self.children[1].toString(True) + ")"
			else:
				return self.children[0].toString(False) + " | " + self.children[1].toString(True)
		else: 
			raise Exception("Invalid guard")

	def __str__(self):
		return self.toString(False)

class Edge:

	def __init__(self, source, channel, sending, act, guard, reset, destination):
		self.source = source
		self.channel = channel
		self.sending = sending
		self.act = act
		self.guard = guard
		self.reset = reset
		self.destination = destination

	def getClocks(self):
		return self.guard.getClocks() | set(self.reset)

	def toDBMEdge(self,context):
		return DBMTransition(self.source, self.destination, self.channel, self.act, 
				     self.guard.toDBM(context), map(lambda x: context.__getitem__(x),
				     self.reset), context, self.sending)

	def resetsToString(self):
		if self.reset:
			return "{" + reduce(lambda r1,r2: r1 + ";" + r2, self.reset) + "}"
		else:
			return "{}"

	def msgToString(self):
		if self.sending:
			return self.channel + "!" + self.act + "(" + str(self.guard) + "," + self.resetsToString() + ")"
		else:
			return self.channel + "?" + self.act + "(" + str(self.guard) + "," + self.resetsToString() + ")"

class Cta:

	def __init__(self, initial, edges):
		self.initial = initial
		self.edges = edges

	def getClocks(self):
		return reduce(lambda x, y: x | y, map(lambda x: x.getClocks(), self.edges), set([]))

	def toDBMCta(self,context):
		return DBMCta(self.initial, map(lambda e: e.toDBMEdge(context), self.edges), context)

	def getStates(self):
		ret = set([self.initial])
		for e in self.edges:
			ret = ret | set([e.source,e.destination])
		return ret

	def toDot(self):
		dot = Digraph()
		for q in self.getStates():
			dot.node(q,q)
		dot.attr('node', shape='none')
		dot.node('0', label='')
		for e in self.edges:
			dot.edge(e.source,e.destination,label = e.msgToString())
		dot.edge('0',self.initial)
		return dot

def genContext(clocks, name = 'c'):
	return Context(clocks,name)

class Declaration:
	def __init__(self, name, cta):
		self.name = name
		self.cta = cta
		self.instrId = 'dec'

class Query:
	def __init__(self, cta1name, cta2name):
		self.cta1name = cta1name
		self.cta2name = cta2name
		self.instrId = 'query'

class Show:
	def __init__(self, ctaName):
		self.ctaName = ctaName
		self.instrId = 'show'

def execute(script):
	env = dict()
	for c in script:
		if c.instrId == 'dec':
			print "Loading " + c.name + "."
			env[c.name] = c.cta
		elif c.instrId == 'query':
			print "Checking refinements between " + c.cta1name + " and " + c.cta2name + "."
			query(env, c.cta1name, c.cta2name)
		elif c.instrId == 'show':
			print "Showing " + c.ctaName + "."
			try:
				cta = env[c.ctaName]
			except KeyError:
				print "Cta " + c.ctaName + " undeclared."
			cta.toDot().render('output/' + c.ctaName, view=True, cleanup=True)
		else:
			raise Exception("Invalid command: " + c.instrId)

def query(env, cta1name, cta2name):
	start_time = time.time()
	try:
		cta1 = env[cta1name]
	except KeyError:
		print "Cta " + cta1name + " undeclared."
	try:
		cta2 = env[cta2name]
	except KeyError:
		print "Cta " + cta2name + " undeclared."
	c = genContext(cta1.getClocks() | cta2.getClocks())
	dbmCta1 = cta1.toDBMCta(c)
	dbmCta2 = cta2.toDBMCta(c)
#	print "Send and receive restriction refinement check: %r." % srRefines(dbmCta1,dbmCta2)
	print ("Send restriction and receive procrastination refinement check: %r."  
		% srpRefines(dbmCta1,dbmCta2))
#	print "Asymmetric refinement check: %r." % aRefines(dbmCta1,dbmCta2)
	print "LLESP check: %r." % llesp(dbmCta1,dbmCta2)
	end_time = time.time()
	print "Query time: %s seconds." % (end_time - start_time)

#actions = {
#	"Command": [lambda _, nodes: [Declaration(nodes[1], Cta(nodes[4], nodes[6]))],
#		    lambda _, nodes: [Declaration(nodes[1], Cta(nodes[4], []))],
#		    lambda _, nodes: [Query(nodes[0],nodes[2])],
#		    lambda _, nodes: [Show(nodes[2])],
#		    lambda _, nodes: nodes[0] + nodes[2]],
#	"Guard": [lambda _, nodes: GuardTree('True',[]),
#		  lambda _, nodes: GuardTree('False',[]),
#		  lambda _, nodes: GuardTree('Leq',[nodes[0],nodes[2]]),
#		  lambda _, nodes: GuardTree('Lt',[nodes[0],nodes[2]]),
#		  lambda _, nodes: GuardTree('Geq',[nodes[0],nodes[2]]),
#		  lambda _, nodes: GuardTree('Gt',[nodes[0],nodes[2]]),
#		  lambda _, nodes: GuardTree('Eq',[nodes[0],nodes[2]]),
#		  lambda _, nodes: GuardTree('And',[nodes[0],nodes[2]]),
#		  lambda _, nodes: GuardTree('Or',[nodes[0],nodes[2]]),
#		  lambda _, nodes: nodes[1]],
#	"Clock": lambda _, nodes: nodes[0],
#	"String": lambda _, value: value.encode('ascii','ignore'),
#	"Nat": lambda _, value: int(value),
#	"Name": lambda _, value: value.encode('ascii','ignore'),
#	"Initial": lambda _, nodes: nodes[1],
#	"Edges": [lambda _, nodes: [nodes[0]],
#	          lambda _, nodes: [nodes[0]] + nodes[2]],
#	"Edge": [lambda _, nodes: Edge(nodes[0],nodes[1],nodes[2],nodes[3],nodes[5],nodes[8],nodes[11]),
#		 lambda _, nodes: Edge(nodes[0],nodes[1],nodes[2],nodes[3],nodes[5],[],nodes[10]),
#		 lambda _, nodes: Edge(nodes[0],nodes[1],nodes[2],nodes[3],nodes[5],[],nodes[7]),
#		 lambda _, nodes: Edge(nodes[0],nodes[1],nodes[2],nodes[3],GuardTree('True',[]),nodes[6],nodes[9]),
#		 lambda _, nodes: Edge(nodes[0],nodes[1],nodes[2],nodes[3],GuardTree('True',[]),[],nodes[8]),
#		 lambda _, nodes: Edge(nodes[0],nodes[1],nodes[2],nodes[3],GuardTree('True',[]),[],nodes[6]),
#		 lambda _, nodes: Edge(nodes[0],nodes[1],nodes[2],nodes[3],GuardTree('True',[]),[],nodes[4])],
#	"State": lambda _, nodes: nodes[0],
#	"Channel": lambda _, nodes: nodes[0],
#	"Act": lambda _, nodes: nodes[0],
#	"IO": [lambda _, value: True,
#	       lambda _, value: False],
#	"Clocks": [lambda _, nodes: [nodes[0]],
#	          lambda _, nodes: [nodes[0]] + nodes[2]]
#}

actions = {
	"Command": [lambda _, nodes: [Declaration(nodes[1], Cta(nodes[4], nodes[5]))],
		    lambda _, nodes: [Declaration(nodes[1], Cta(nodes[4], []))],
		    lambda _, nodes: [Query(nodes[0],nodes[2])],
		    lambda _, nodes: [Show(nodes[2])],
		    lambda _, nodes: nodes[0] + nodes[1]],
	"Guard": [lambda _, nodes: GuardTree('True',[]),
		  lambda _, nodes: GuardTree('False',[]),
		  lambda _, nodes: GuardTree('Leq',[nodes[0],nodes[2]]),
		  lambda _, nodes: GuardTree('Lt',[nodes[0],nodes[2]]),
		  lambda _, nodes: GuardTree('Geq',[nodes[0],nodes[2]]),
		  lambda _, nodes: GuardTree('Gt',[nodes[0],nodes[2]]),
		  lambda _, nodes: GuardTree('Eq',[nodes[0],nodes[2]]),
		  lambda _, nodes: GuardTree('And',[nodes[0],nodes[2]]),
		  lambda _, nodes: GuardTree('Or',[nodes[0],nodes[2]]),
		  lambda _, nodes: nodes[1]],
	"Clock": lambda _, nodes: nodes[0],
	"String": lambda _, value: value.encode('ascii','ignore'),
	"Nat": lambda _, value: int(value),
	"Name": lambda _, value: value.encode('ascii','ignore'),
	"Initial": lambda _, nodes: nodes[1],
	"Edges": [lambda _, nodes: [nodes[0]],
	          lambda _, nodes: [nodes[0]] + nodes[1]],
	"Edge": [lambda _, nodes: Edge(nodes[0],nodes[1],nodes[2],nodes[3],nodes[5],nodes[8],nodes[11]),
		 lambda _, nodes: Edge(nodes[0],nodes[1],nodes[2],nodes[3],nodes[5],[],nodes[10]),
		 lambda _, nodes: Edge(nodes[0],nodes[1],nodes[2],nodes[3],nodes[5],[],nodes[7]),
		 lambda _, nodes: Edge(nodes[0],nodes[1],nodes[2],nodes[3],GuardTree('True',[]),nodes[6],nodes[9]),
		 lambda _, nodes: Edge(nodes[0],nodes[1],nodes[2],nodes[3],GuardTree('True',[]),[],nodes[8]),
		 lambda _, nodes: Edge(nodes[0],nodes[1],nodes[2],nodes[3],GuardTree('True',[]),[],nodes[6]),
		 lambda _, nodes: Edge(nodes[0],nodes[1],nodes[2],nodes[3],GuardTree('True',[]),[],nodes[4])],
	"State": lambda _, nodes: nodes[0],
	"Channel": lambda _, nodes: nodes[0],
	"Act": lambda _, nodes: nodes[0],
	"IO": [lambda _, value: True,
	       lambda _, value: False],
	"Clocks": [lambda _, nodes: [nodes[0]],
	          lambda _, nodes: [nodes[0]] + nodes[2]]
}

def refinementChecker(scriptFile):
	try:
		g = Grammar.from_file("grammar")
		parser = Parser(g, actions=actions)
	except Exception as e:
		print e
		print "Parse generation: Failed."
		print "Terminating."
		sys.exit()
	print "Parser generation: Done."
	try:
		script = parser.parse_file(scriptFile)
		print "Parse input: Done."
	except Exception as e:
		print e
		print "Parse input: Failed."
		print "Terminating."
		sys.exit()
	try:
		execute(script)
	except Exception as e:
		print e
		print "Script execution: Failed."
		print "Terminating."
		sys.exit()
	print "Script execution: Done."
	print "Terminating."
