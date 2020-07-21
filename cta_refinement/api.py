from flask import jsonify, abort, request, Blueprint, session, make_response,Response
from settings import EXAMPLESDIRECTORY, DBMDIRECTORY
import os, sys
sys.path.append(DBMDIRECTORY)
from CtaWebFunctions import *


REFINER_API = Blueprint('api', __name__)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return REFINER_API

@REFINER_API.route('/api/cta/<string:ctaName>', methods=['GET','POST','PUT','DELETE'])
def add_cta(ctaName):  # noqa: E501
    """Adds/Removes/Updates/Gets a CTA from the session

    Adds/Removes/Updates/Gets a CTA to the session # noqa: E501

    :param CTA: CTA to add/update/delete/get
    :type CTA: dict | bytes

    :rtype: None
    """
    if request.method == 'GET':
        try:
            return session["ctaList"][ctaName]
        except:
            return handle_404_error(404)
    if request.method == 'POST':
        return 'post'
    if request.method == 'PUT':
        return 'put'
    if request.method == 'DELETE':
        try:
            session["ctaList"].pop(ctaName)
            return "Successfully deleted", 200
        except:
            return handle_404_error(404)

@REFINER_API.route('/api/grammar', methods=['GET'])
def get_grammar():  # noqa: E501
    """Gets CTA grammar rules.

    This will return the grammar rules for specifying CTAs  # noqa: E501

    :rtype: object
    """
    try:
        f = open(DBMDIRECTORY+"grammar","r")
        grammar = f.readlines()
        return jsonify(grammar_rules=grammar)
    except:
        return handle_404_error(404)

@REFINER_API.route('/api/sample-scripts/<sample_name>', methods=['GET'])
def get_sample(sample_name):  # noqa: E501
    """returns a specified sample script

    By passing in the specified sample script name you are able to get a sample script  # noqa: E501

    :param sample_name: 
    :type sample_name: str

    :rtype: object
    """
    try:
        f = open(EXAMPLESDIRECTORY+sample_name,"r")
        example = f.readlines()
        return jsonify(name=sample_name,sample_script=example)
    except:
        return handle_404_error(404)

@REFINER_API.route('/api/sample-scripts', methods=['GET'])
def get_samples():  # noqa: E501
    """returns a list of available sample scripts

    Returns a list of available sample scripts which can be passed as a parameter to retrieve specific sample  # noqa: E501


    :rtype: None
    """
    try:
        examples = []
        for files in os.listdir(EXAMPLESDIRECTORY):
            examples.append(files)
        return str(examples)
    except:
        return handle_400_error(400)

@REFINER_API.route('/api/cta/<string:ctaName1>/refines/<string:ctaName2>', methods=['GET'])
def refine_ctas(ctaName1,ctaName2):  # noqa: E501
    """Gets refinements between two CTAs.

    By passing in the appropriate options, you can search for ctas which are currently defined in the system  # noqa: E501

    :param ctaName: gets refinements between two ctas
    :type ctaName: str

    :rtype: Refinement
    """
    try:
        cta1 = session["ctaList"][ctaName1]
        cta2 = session["ctaList"][ctaName2]

        script = ("Cta " + ctaName1 + " = " + str(cta1) + "; Cta " + ctaName2 + " = " 
        + str(cta2) + ";" + ctaName1 + " refines? " + ctaName2 + ";")
        scriptResponse = webScriptRefinementChecker(str(script),"none","png")
        return jsonify(result=scriptResponse)
    except:
        return handle_404_error(404)

@REFINER_API.route('/api/cta', methods=['GET'])
def search_cta(skip=None, limit=None):  # noqa: E501
    """Searches CTAs in your session.

    By passing in the appropriate options, you can search for ctas which are currently defined in the system  # noqa: E501

    :param skip: number of records to skip for pagination
    :type skip: int
    :param limit: maximum number of records to return
    :type limit: int

    :rtype: List[CTA]
    """

    script = session.get('currentScript')
    rf = reformatScript(script)

    parseCTAs(rf)
    return jsonify(session['ctaList'].items())

def parseCTAs(script):
    ctaName = ""
    while script.find("Cta") != -1:
        spScript = script.split()
        index = spScript.index("Cta")
        ctaName = spScript[index + 1]
        index = index + 3
        ctaDefinition = ""

        while not endOfCTA(spScript[index],spScript[index + 1]):
            ctaDefinition = ctaDefinition + spScript[index] + " "
            index = index + 1
        if session.has_key("ctaList"):
            session["ctaList"].update({ctaName : ctaDefinition + "}"})
        else:
            session["ctaList"] = {ctaName : ctaDefinition + "}"}
        
        start = script.find("Cta") + 3
        script = script[start:]


def endOfCTA(str,str2):
    return str.find("};") != -1 or str[-1].find("}") != -1 and str2[0].find(";") != -1

def reformatScript(script):
    spScript = script.split()
    rfScript = ""
    newStr = ""
    for str in spScript:
        if str.find(";") != -1:
            for i in str:
                if i == ";":
                    newStr = newStr + " ; "
                else:
                    newStr = newStr + i
            rfScript = rfScript + newStr + " "        
            newStr = "" 
        else:
            rfScript = rfScript + str + " "
    return rfScript



@REFINER_API.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Invalid Operation'}), 400)


@REFINER_API.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'CTA Not found'}), 404)


@REFINER_API.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)