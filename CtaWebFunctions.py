"""Cta Web Functions

This module provides functions to be used when interfacing with the Flask
webframework specifically it allows for CtaRefinement tool to accept String
data types and return Strings back for rendering within webtemplates.

This file can also be imported as a module and contains the following
functions:

    * webRefines - checks for refinements between two Cta Objects returns
                    a String output of refinement outcome.
    * webSrRefines - implements webRefines with a restrictor function.
    * webSrpRefines - implements webRefines with a procrastinator function.
    * webARefines - implements webRefines with a asymettric function.
    * webllesp - checks llesp characteristics between two Cta returns
                a String output.
    * webQuery - implements webllesp with Cta enviroment variables
    * webExecuteScript - iterates through numerous Ctas present in query String 
                        passes to webQuery
    * webRefinementChecker - key function loads grammar file and provides error 
        checking on String passed - should be used as the main funcation.
    * main - passes to webRefinementChecker
"""


from DBMCta import *
from CtaParser import *

def webRefines(ctaA,ctaB,f):
    	assert ctaA.context == ctaB.context
	if not ctaA.initial == ctaB.initial: 
		return False
	for t in ctaA.transitions:
		if not search(lambda x : f(t,x),ctaB.transitions):
			return "No matching edge for " + str(t) + " of left machine. \n" + "False.\n"
	for t in ctaB.transitions:
		if not search(lambda x : f(x,t),ctaA.transitions):
			return "No matching edge for " + str(t) + " of right machine .\n" + "False.\n"
	return "True"

def webSrRefines(ctaA,ctaB):
    	return webRefines(ctaA, ctaB, restrictionFunction)

def webSrpRefines(ctaA,ctaB):
	return webRefines(ctaA, ctaB, procrastinatorFunction)

def webARefines(ctaA,ctaB):
	return webRefines(ctaA, ctaB, asymmetricFunction)


def webllesp(ctaA,ctaB):
    	assert ctaA.context == ctaB.context
	for q in ctaA.states:
		PP = ctaA.post(ctaA.pre(q),q)
		if not q in ctaB.states:
			return "State " + q + " not present in second machine.\n" + "False."
		if not (PP & ctaB.les(q)) <= (PP & ctaA.les(q)):
			return "Refinement is not llesp at state " + q + ".\n" + "False."
	return "True."



def webQuery(env, cta1name, cta2name):
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
		% webSrpRefines(dbmCta1,dbmCta2))
	returnStringList.append("LLESP check: " + webllesp(dbmCta1,dbmCta2)+"\n")
	end_time = time.time()
	returnStringList.append("Query time: %s seconds. \n" % (end_time - start_time))
        return returnString.join(returnStringList)

def webExecute(script):
        returnStringList = []
        returnString = ""
    	env = dict()
	for c in script:
		if c.instrId == 'dec':
			returnStringList.append("Loading " + c.name + ".\n")
			env[c.name] = c.cta
		elif c.instrId == 'query':
			returnStringList.append("Checking refinements between " + c.cta1name + " and " + c.cta2name + ".\n")
			response = webQuery(env, c.cta1name, c.cta2name)
			returnStringList.append(response)
		elif c.instrId == 'show':
			returnStringList.append("Showing " + c.ctaName + ".\n")
			try:
				cta = env[c.ctaName]
			except KeyError:
				returnStringList.append("Cta " + c.ctaName + " undeclared.\n")
			cta.toDot().render('output/' + c.ctaName, view=True, cleanup=True)
		else:
			raise Exception("Invalid command: " + c.instrId)
        return returnString.join(returnStringList)


def webScriptRefinementChecker(script):
    try:
        g = Grammar.from_file("grammar")
        parser = Parser(g, actions=actions)
    except Exception as e:
        return str(e) + " Parse generation: Failed. Terminating.\n"
        sys.exit()
    try:
        script = parser.parse(script)
    except Exception as e:
        return "Parser generation: Done. Parse input: Failed." + str(e) + ". Terminating.\n" 
        sys.exit()
    try:
        response = webExecute(script)
    except Exception as e:
        return str(e) + "Script execution: Failed. Terminating.\n"
        sys.exit()
    return "Parse input: Done.\nParser generation: Done.\n" + response + "Script execution: Done.\nTerminating.\n"


def main():
    script = str(input("Please enter script: "))
    print webScriptRefinementChecker(script)


if __name__=="__main__":
    main()

