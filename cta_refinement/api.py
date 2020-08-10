from flask import json, jsonify, abort, request, Blueprint, session, make_response,Response
from settings import EXAMPLESDIRECTORY, DBMDIRECTORY
import os, sys
sys.path.append(DBMDIRECTORY)
from CtaWebFunctions import *


REFINER_API = Blueprint('api', __name__)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return REFINER_API

@REFINER_API.route('/api/cta/<string:cta_name>', methods=['GET','POST','PUT','DELETE'])
def add_cta(cta_name):  # noqa: E501
    """Adds/Removes/Updates/Gets a CTA from the session

    Adds/Removes/Updates/Gets a CTA to the session # noqa: E501

    :param CTA: CTA to add/update/delete/get
    :type CTA: dict | bytes

    :rtype: None
    """
    if request.method == 'GET':
        try:
            return jsonify(get_cta(cta_name)), 200
        except:
            return handle_404_error(404)
    
    if request.method == 'POST':
        try:
            cta = request.get_json()
            name = cta["name"]
            definition = cta["CTA"]

            if cta_present(name):
                return "A CTA with the name " + name + " already exists in this session.", 400 
            else:
                append_cta(name, definition)
                return json.dumps(session["CTA List"]), 200
        except:
            return handle_404_error(404)

    if request.method == 'PUT':
        try:
            new_cta = request.get_json()
            name = new_cta["name"]
            definition = new_cta["CTA"]

            if cta_present(cta_name):
                cta_obj = get_cta(cta_name)
                cta_obj["CTA"] = definition
                return json.dumps(session["CTA List"]), 200
                #return "CTA '" + cta_obj["name"] +  "' successfully updated.", 200
            else:
                return handle_404_error(404)
        except:
            return handle_400_error(400)

    if request.method == 'DELETE':
        try:
            for cta in session["CTA List"]:
                if cta["name"] == cta_name:
                    session["CTA List"].remove(cta)
                    return json.dumps(session["CTA List"]), 200
                else:
                    return handle_404_error(404)
        except:
            return handle_400_error(400)


@REFINER_API.route('/api/grammar', methods=['GET'])
def get_grammar():  # noqa: E501
    """Gets CTA grammar rules.

    This will return the grammar rules for specifying CTAs  # noqa: E501

    :rtype: object
    """
    try:
        f = open(DBMDIRECTORY+"grammar","r")
        grammar = f.readlines()
        return jsonify(grammar_rules=grammar), 200
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
        return jsonify(name=sample_name,sample_script=example), 200
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
        return str(examples), 200
    except:
        return handle_400_error(400)

@REFINER_API.route('/api/cta/<string:cta_name1>/refines/<string:cta_name2>', methods=['GET'])
def refine_ctas(cta_name1,cta_name2):  # noqa: E501
    """Gets refinements between two CTAs.

    By passing in the appropriate options, you can search for ctas which are currently defined in the system  # noqa: E501

    :param cta_name: gets refinements between two ctas
    :type cta_name: str

    :rtype: Refinement
    """
    try:
        cta1 = get_cta(cta_name1)
        cta2 = get_cta(cta_name2)

        script = ("Cta " + cta_name1 + " = " + str(cta1["CTA"]) + "; Cta " + cta_name2 + " = " 
        + str(cta2["CTA"]) + ";" + cta_name1 + " refines? " + cta_name2 + ";")
        scriptResponse = webScriptRefinementChecker(str(script),"none","png")
        return jsonify(result=scriptResponse), 200
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

    :rtype: Dictionary{Name of CTA : Definition of CTA}
    """

    try:
        script = session.get('currentScript')
        rf_script = reformat_script(script)
        parse_ctas(rf_script)
        return json.dumps(session["CTA List"]), 200
    except:
        return handle_404_error(404)

def parse_ctas(script):
    """ Parses a script and extracts CTAs from it. 
        Appends the 'session' variable with a 'CTA List' dictionary.

        :param script: Cta refinement script
        :type script: string
    """
    cta_name = ""
    while script.find("Cta") != -1:
        sp_script = script.split()
        index = sp_script.index("Cta")
        cta_name = sp_script[index + 1]
        index = index + 3
        cta_definitioninition = ""

        while not end_of_cta(sp_script[index],sp_script[index + 1]):
            cta_definitioninition = cta_definitioninition + sp_script[index] + " "
            index = index + 1
        cta_obj = {"name" : cta_name, "CTA" : cta_definitioninition + "}"}
        if session.has_key("CTA List"):
            if not cta_present(cta_name):
                append_cta(cta_name,cta_definitioninition)
        else:
            session["CTA List"] = [cta_obj]

        start = script.find("Cta") + 3
        script = script[start:]


def end_of_cta(str,str2):
    """
    Signifies the end of a CTA object within a script

    :param str: String to test for object end tokens
    :type str: string
    :param str2: String to test for object end tokens
    :type str2: string

    :rtype: boolean
    """
    return str.find("};") != -1 or str[-1].find("}") != -1 and str2[0].find(";") != -1

def reformat_script(script):
    """
    Reformats script for compatibility with 'parse_cta' function, and returns the new version

    :param script: CTA refinement script
    :type script: string

    :rtype: string
    """
    sp_script = script.split()
    rf_script = ""
    new_str = ""
    for str in sp_script:
        if str.find(";") != -1:
            for i in str:
                if i == ";":
                    new_str = new_str + " ; "
                else:
                    new_str = new_str + i
            rf_script = rf_script + new_str + " "
            new_str = "" 
        else:
            rf_script = rf_script + str + " "
    return rf_script

def cta_present(name):
    c = -1
    for cta in session["CTA List"]:
        if cta["name"] == name:
            c = c + 1
    return c != -1
    

def append_cta(name, definition):
    definition = definition + "}"
    cta_obj = {"name": name, "CTA": definition}
    if session.has_key("CTA List"):
        session["CTA List"].append(cta_obj)
    else:
        session["CTA List"] = [cta_obj]

def get_cta(name):
    for cta in session["CTA List"]:
        if cta["name"] == name:
            return cta

@REFINER_API.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Invalid Operation'}), 400)


@REFINER_API.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'CTA Not found'}), 404)


#@REFINER_API.errorhandler(500)
#def handle_500_error(_error):
#    """Return a http 500 error to client"""
#    return make_response(jsonify({'error': 'Server error'}), 500)
