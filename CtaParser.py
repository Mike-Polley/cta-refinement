from parglare import Parser, Grammar
from udbm import Context
from DBMCta import *
from graphviz import Digraph
import sys,time
from functools import *

class GuardTree:

	def __init__(self, op, children):
		self.op = op
		self.children = children

	def get_clocks(self):
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
			return self.children[0].get_clocks() | self.children[1].get_clocks()
		elif self.op == 'Or':
			return self.children[0].get_clocks() | self.children[1].get_clocks()
		else: 
			raise Exception("Invalid guard")

	def to_DBM(self,context):
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
			return self.children[0].to_DBM(context) & self.children[1].to_DBM(context)
		elif self.op == 'Or':
			return self.children[0].to_DBM(context) | self.children[1].to_DBM(context)
		else: 
			raise Exception("Invalid guard")

	def to_string(self, parenthesis):
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
				return "(" + self.children[0].to_string(False) + " & " + self.children[1].to_string(True) + ")"
			else:
				return self.children[0].to_string(False) + " & " + self.children[1].to_string(True)
		elif self.op == 'Or':
			if parenthesis:
				return "(" + self.children[0].to_string(False) + " | " + self.children[1].to_string(True) + ")"
			else:
				return self.children[0].to_string(False) + " | " + self.children[1].to_string(True)
		else: 
			raise Exception("Invalid guard")

	def __str__(self):
		return self.to_string(False)

class Edge:

	def __init__(self, source, channel, sending, act, guard, reset, destination):
		self.source = source
		self.channel = channel
		self.sending = sending
		self.act = act
		self.guard = guard
		self.reset = reset
		self.destination = destination

	def get_clocks(self):
		return self.guard.get_clocks() | set(self.reset)

	def to_DBM_edge(self,context):
		return DBMTransition(self.source, self.destination, self.channel, self.act, 
				     self.guard.to_DBM(context), map(lambda x: context.__getitem__(x),
				     self.reset), context, self.sending)

	def resets_to_string(self):
		if self.reset:
			return "{" + reduce(lambda r1,r2: r1 + ";" + r2, self.reset) + "}"
		else:
			return "{}"

	def msg_to_string(self):
		if self.sending:
			return self.channel + "!" + self.act + "(" + str(self.guard) + "," + self.resets_to_string() + ")"
		else:
			return self.channel + "?" + self.act + "(" + str(self.guard) + "," + self.resets_to_string() + ")"

class Cta:

	def __init__(self, initial, edges):
		self.initial = initial
		self.edges = edges

	def get_clocks(self):
		return reduce(lambda x, y: x | y, map(lambda x: x.get_clocks(), self.edges), set([]))

	def to_DBM_Cta(self,context):
		return DBMCta(self.initial, map(lambda e: e.to_DBM_edge(context), self.edges), context)

	def get_states(self):
		ret = set([self.initial])
		for e in self.edges:
			ret = ret | set([e.source,e.destination])
		return ret

	def to_dot(self):
		dot = Digraph()
		for q in self.get_states():
			dot.node(q,q)
		dot.attr('node', shape='none')
		dot.node('0', label='')
		for e in self.edges:
			dot.edge(e.source,e.destination,label = e.msg_to_string())
		dot.edge('0',self.initial)
		return dot

def gen_context(clocks, name = 'c'):
	return Context(clocks,str(name))

class Declaration:
	def __init__(self, name, cta):
		self.name = name
		self.cta = cta
		self.instr_id= 'dec'

class Query:
	def __init__(self, cta_1_name, cta_2_name):
		self.cta_1_name = str(cta_1_name)
		self.cta_2_name = str(cta_2_name)
		self.instr_id= 'query'

class Show:
	def __init__(self, cta_name):
		self.cta_name = str(cta_name)
		self.instr_id= 'show'

def execute(script):
	env = dict()
	for c in script:
		if c.instr_id== 'dec':
			print("Loading " + str(c.name) + ".")
			env[str(c.name)] = c.cta
		elif c.instr_id== 'query':
			print("Checking refinements between " + str(c.cta_1_name) + " and " + str(c.cta_2_name) + ".")
			query(env, str(c.cta_1_name), str(c.cta_2_name))
		elif c.instr_id== 'show':
			print("Showing " + str(c.cta_name) + ".")
			try:
				cta = env[str(c.cta_name)]
			except KeyError:
				print("Cta " + str(c.cta_name) + " undeclared.")
			cta.to_dot().render('output/' + str(c.cta_name), view=True, cleanup=True)
		else:
			raise Exception("Invalid command: " + str(c.instrId))

def query(env, cta_1_name, cta_2_name):
	start_time = time.time()
	try:
		cta1 = env[cta_1_name]
	except KeyError:
		print("Cta " + str(cta_1_name) + " undeclared.")
	try:
		cta2 = env[cta_2_name]
	except KeyError:
		print("Cta " + str(cta_2_name) + " undeclared.")
	c = gen_context(cta1.get_clocks() | cta2.get_clocks())
	dbmCta1 = cta1.to_DBM_Cta(c)
	dbmCta2 = cta2.to_DBM_Cta(c)
	print ("Send restriction and receive procrastination refinement check: %r."  
		% srp_refines(dbmCta1,dbmCta2))
	print("LLESP check: %r." % llesp(dbmCta1,dbmCta2))
	end_time = time.time()
	print("Query time: %s seconds." % (end_time - start_time))

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

def refinement_checker(scriptFile):
	try:
		g = Grammar.from_file("grammar")
		parser = Parser(g, actions=actions)
	except Exception as e:
		print(e)
		print("Parse generation: Failed.")
		print("Terminating.")
		sys.exit()
	print("Parser generation: Done.")
	try:
		script = parser.parse(scriptFile)
		print("Parse input: Done.")
	except Exception as e:
		print(e)
		print("Parse input: Failed.")
		print("Terminating.")
		sys.exit()
	try:
		execute(script)
	except Exception as e:
		print(e)
		print("Script execution: Failed.")
		print("Terminating.")
		sys.exit()
	print("Script execution: Done.")
	print("Terminating.")
