from python_dbm import Context

class DBMTransition:
	
	def __init__(self, src, dst, channel, action, guard, resets, context, sending):
		self.src = src
		self.dst = dst	
		self.channel = channel	
		self.action = action
		self.sending = sending
		assert guard.context == context
		self.guard = guard
		self.context = context
		self.resets = []
		for x in resets: self.addReset(x)

	def addReset(self, clock):
		assert clock.context == self.context
		self.resets.append(clock)

	def isSending(self):
		return self.sending

	def isReceiving(self):
		return not self.sending

	def resetsToString(self):
		if self.resets:
			return "{" + reduce(lambda r1,r2: r1 + ";" + r2,map(lambda r: r.name, self.resets)) + "}"
		else:
			return "{}"

	def __str__(self):
		if self.isSending():
			return self.src + " " + self.channel + "!" + self.action + "(" + str(self.guard) + "," + self.resetsToString() + ") " + self.dst
		else:
			return self.src + " " + self.channel + "?" + self.action + "(" + str(self.guard) + "," + self.resetsToString() + ") " + self.dst
		
class DBMCta:

	def __init__(self, initial, transitions, context):
		self.transitions = set([])
		self.states = set([initial])
		self.context = context
		self.initial = initial
		self.generate(transitions)

	def generate(self,transitions):
		for t in transitions: 
			assert t.context == self.context
			self.addState(t.src)
			self.addState(t.dst)
			self.addTransition(t)
			
	def addState(self,state):
		self.states.add(state)
#		if state not in self.states:
#			self.states.append(state)

	def addTransition(self,t):
		self.transitions.add(t)
#		if t not in self.transitions:
#			self.transitions.append(t)

	def pre(self,q):
		assert q in self.states
		ret = reduce(lambda g1, g2: g1 | g2, 
			map(lambda t: reset(t.guard,t.resets),
				filter(lambda t: t.dst == q,self.transitions)),
			false(self.context)).down() 
		if q == self.initial:
			ret = ret | self.context.getZeroFederation()
		return ret

	def sending(self,q):
		return reduce(lambda g1, g2: g1 | g2,
			map(lambda t: t.guard,filter(lambda t: t.src == q and t.isSending(),
				self.transitions)),
			false(self.context))

	def receiving(self,q):
		return reduce(lambda g1, g2: g1 | g2,
			map(lambda t: t.guard,filter(lambda t: t.src == q and t.isReceiving(),
				self.transitions)),
			false(self.context))
	def les(self,q):
		assert q in self.states
		qs = self.sending(q)
		if qs.isEmpty():
			return qs
		qr = self.receiving(q)
		if qr.isEmpty():
			return qs.down()
		return (qs - (qr - qs.down()).down()).down()

	def post(self, g, q):
		assert q in self.states
		cles = self.les(q)
		return (g - cles).up() | (g.up() & cles)		
			
def reset(g,R):
	ret = g
	for r in R:
		ret = ret.resetValue(r)
	return ret

def refines(ctaA,ctaB,f):
	assert ctaA.context == ctaB.context
	if not ctaA.initial == ctaB.initial: 
		return False
	for t in ctaA.transitions:
		if not search(lambda x : f(t,x),ctaB.transitions):
			print "No matching edge for " + str(t) + " of left machine" 
			return False
#		l = filter(lambda x : f(t,x), ctaB.transitions)
#		if l == []: 
#			print "No matching edge for " + str(t) + " of left machine" 
#			return False
	for t in ctaB.transitions:
		if not search(lambda x : f(x,t),ctaA.transitions):
			print "No matching edge for " + str(t) + " of right machine" 
			return False
#		l = filter(lambda x : f(x,t), ctaA.transitions)
#		if l == []: 
#			print "No matching edge for " + str(t) + " of right machine" 
#			return False
	return True 

def search(f,l):
	for x in l:
		if f(x):
			return True
	return False

def structurePres(t1,t2):
	if not t1.isSending() == t2.isSending():
		return False
	if not t1.src == t2.src: 
		return False
	if not t1.dst == t2.dst: 
		return False
	if not t1.channel == t2.channel: 
		return False
	if not t1.action == t2.action: 
		return False
	for x in t1.resets:
		if x.name not in map(lambda x: x.name, t2.resets):
			return False
	for x in t2.resets:
		if x.name not in map(lambda x: x.name, t1.resets):
			return False
	return True

def restrictionFunction(t1,t2):
	if structurePres(t1,t2):
		return t1.guard <= t2.guard
	else:
		return False

def asymmetricFunction(t1,t2):
	if structurePres(t1,t2):
		if t1.isSending():
			return t1.guard <= t2.guard
		else:
			return t2.guard <= t1.guard
	else:
		return False

def procrastinatorFunction(t1,t2):
	if structurePres(t1,t2):
		if t1.isSending():
			return t1.guard <= t2.guard
		else:
			return t1.guard <= t2.guard and t2.guard.down() <= t1.guard.down()
	else:
		return False

def llesp(ctaA,ctaB):
	assert ctaA.context == ctaB.context
	for q in ctaA.states:
		PP = ctaA.post(ctaA.pre(q),q)
		if not q in ctaB.states:
			print "State " + q + " not present in second machine."
			return False
		if not (PP & ctaB.les(q)) <= (PP & ctaA.les(q)):
			print "Refinement is not llesp at state " + q + "."
			return False
	return True

def srRefines(ctaA,ctaB):
	return refines(ctaA, ctaB, restrictionFunction)

def srpRefines(ctaA,ctaB):
	return refines(ctaA, ctaB, procrastinatorFunction)

def aRefines(ctaA,ctaB):
	return refines(ctaA, ctaB, asymmetricFunction)
				
def true(c):
	return c.getZeroFederation().setInit()

def false(c):
	return true(c) - true(c)
