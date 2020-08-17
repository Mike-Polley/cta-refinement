"""Cta Web Functions
This module provides functions to be used when interfacing with the Flask
webframework specifically it allows for CtaRefinement tool to accept String
data types and return Strings back for rendering within webtemplates.
This file can also be imported as a module and contains the following
functions:
    * web_refines - checks for refinements between two Cta Objects returns
                    a String output of refinement outcome.
    * web_sr_refines - implements web_refines with a restrictor function.
    * web_srp_refines - implements web_refines with a procrastinator function.
    * web_A_refines - implements web_refines with a asymettric function.
    * web_llesp - checks llesp characteristics between two Cta returns
                a String output.
    * web_query - implements web_llesp with Cta enviroment variables
    * web_execute - iterates through numerous Ctas present in query String 
                        passes to web_query
    * web_refinement_checker - key function loads grammar file and provides error 
        checking on String passed - should be used as the main funcation.
    * main - passes to webRefinementChecker
"""


from DBMCta import *
from CtaParser import *
import os


def web_refines(ctaA,ctaB,f):
	""" checks for refinements between two Cta Objects returns
		a String output of refinement outcome.
	"""
	assert ctaA.context == ctaB.context
	if not ctaA.initial == ctaB.initial: 
		return False
	for t in ctaA.transitions:
		if not search(lambda x : f(t,x),ctaB.transitions):
			return "No matching edge for " + str(t) + " of left machine.\n " + "False.\n"
	for t in ctaB.transitions:
		if not search(lambda x : f(x,t),ctaA.transitions):
			return "No matching edge for " + str(t) + " of right machine.\n " + "False.\n"
	return "True"

def web_sr_refines(ctaA,ctaB):
	""" implements web_refines with a restrictor function.
	"""
	return web_refines(ctaA, ctaB, restrictionFunction)

def web_srp_refines(ctaA,ctaB):
	""" implements web_refines with a procrastinator function.
	"""
	return web_refines(ctaA, ctaB, procrastinatorFunction)

def web_A_refines(ctaA,ctaB):
	""" implements web_refines with a asymettric function.
	"""
	return web_refines(ctaA, ctaB, asymmetricFunction)


def web_llesp(ctaA,ctaB):
	""" checks llesp characteristics between two Cta returns
		a String output.
	"""
	assert ctaA.context == ctaB.context
	for q in ctaA.states:
		PP = ctaA.post(ctaA.pre(q),q)
		if not q in ctaB.states:
			return "State " + q + " not present in second machine.\n" + "False.\n"
		if not (PP & ctaB.les(q)) <= (PP & ctaA.les(q)):
			return "Refinement is not llesp at state " + q + ".\n" + "False.\n"
	return "True."

def web_query(env, cta1name, cta2name):
	""" implements web_llesp with Cta enviroment variables
	"""
	returnStringList = []
	returnString = ""
	start_time = time.time()
	try:
		cta1 = env[cta1name]
	except KeyError:
		returnStringList.append("Cta " + cta1name + " undeclared. ")
	try:
		cta2 = env[cta2name]
	except KeyError:
		returnStringList.append("Cta " + cta2name + " undeclared. ")
	c = genContext(cta1.getClocks() | cta2.getClocks())
	dbmCta1 = cta1.toDBMCta(c)
	dbmCta2 = cta2.toDBMCta(c)
	returnStringList.append("Send restriction and receive procrastination refinement check: %r.\n"  
		% web_srp_refines(dbmCta1,dbmCta2))
	returnStringList.append("LLESP check: " + web_llesp(dbmCta1,dbmCta2)+"\n")
	end_time = time.time()
	returnStringList.append("Query time: %s seconds. \n" % (end_time - start_time))
        return returnString.join(returnStringList)

def web_execute(script,tf,format):
	""" iterates through numerous Ctas present in query String 
		passes to web_query
	"""
	returnStringList = []
	returnString = ""
	env = dict()
	for c in script:
		if c.instrId == 'dec':
			returnStringList.append("Loading " + c.name + ".\n")
			env[c.name] = c.cta
		elif c.instrId == 'query':
			returnStringList.append("Checking refinements between " + c.cta1name + " and " + c.cta2name + ".\n")
			response = web_query(env, c.cta1name, c.cta2name)
			returnStringList.append(response)
		elif c.instrId == 'show':
			returnStringList.append("Showing " + c.ctaName + ".\n")
			try:
				cta = env[c.ctaName]
			except KeyError:
				returnStringList.append("Cta " + c.ctaName + " undeclared.\n")
			cta.toDot(format).render("/var/www/cta_refinement/cta_refinement/static/files/imagetemp/"+tf, view=False, cleanup=True)
		else:
			raise Exception("Invalid command: " + c.instrId)
        return returnString.join(returnStringList)


""" Creates variable for dbmModules for grammar file"""
if "dbmModules" not in os.getcwd():
	dir = os.path.join(os.getcwd(),"dbmModules")
else:
	dir = os.getcwd()

def web_script_refinement_checker(script,tf,format):
    """ key function loads grammar file and provides error 
        checking on String passed - should be used as the main funcation.
	"""
    try:
        g = Grammar.from_file(os.path.join("/var/www/cta_refinement/cta_refinement/dbmModules","grammar"))
        parser = Parser(g, actions=actions)
    except Exception as e:
        print dir 
        return str(e) + " Parse generation: Failed. Terminating.\n"
        sys.exit()
    try:
        script = parser.parse(script)
    except Exception as e:
        return "Parser generation: Done. Parse input: Failed." + str(e) + ". Terminating.\n" 
        sys.exit()
    try:
        response = web_execute(script,tf,format)
    except Exception as e:
        return str(e) + "Script execution: Failed. Terminating.\n"
        sys.exit()
    return "Parser generation: Done.\nParse input: Done.\n" + response + "Script execution: Done.\nTerminating.\n"


def main():
    script = str(input("Please enter script: "))
    print web_script_refinement_checker(script)


if __name__=="__main__":
    main()
