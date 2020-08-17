""" Module provides unit testing functionality for dbmModules
    requires module pytest.
    To run at command line enter: pytest TestWeb.py
"""
import pytest
import sys
sys.path.append("/var/www/cta_refinement/cta_refinement/dbmModules/")
from CtaWebFunctions import web_script_refinement_checker
from CtaParser import loadGrammarFile


def testGrammarFile():
    """Test successful load of grammar file
    """
    g = loadGrammarFile("/var/www/cta_refinement/cta_refinement/dbmModules/grammar")
    assert type(g).__name__ is "Grammar"

def testInputFailure():
    """Test script failure response
    """
    assert web_script_refinement_checker("fail","dummyFile","png") == (
    'Parser generation: Done. Parse input: Failed.Error at '+
    '1:4:"fail*" => Expected: refines?. Terminating.\n')

def testInputSuccess():
    """Test simple successful script
    """
    response = web_script_refinement_checker(("Cta A = {Init q0;"+
    "q0 pq!a(x0 == 1000 & x1 == 1000,{x0; x1}) q1;"+
    "q0 pq?b(x0 < 1000 & x1 < 1000,{x0; x1}) q1;"+
    "};"+ 
    "A refines? A;"),"dummyFile","png")
    assert ("Parser generation: Done.\nParse input: Done.\n"+
    "Loading A.\nChecking refinements between A and A.\nSend"+
    " restriction and receive procrastination refinement check:"+
    " 'True'.\nLLESP check: True.\n") in response