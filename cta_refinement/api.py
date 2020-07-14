from flask import jsonify, abort, request, Blueprint, session, make_response
from settings import EXAMPLESDIRECTORY
import os

REFINER_API = Blueprint('api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REFINER_API

@REFINER_API.route('/api/cta/<string:ctaName>', methods=['GET','POST','PUT','DELETE'])
def add_cta(CTA=None):  # noqa: E501
    """Adds/Removes/Updates/Gets a CTA from the session

    Adds/Removes/Updates/Gets a CTA to the session # noqa: E501

    :param CTA: CTA to add/update/delete/get
    :type CTA: dict | bytes

    :rtype: None
    """

    return 'do some magic!'


@REFINER_API.route('/api/gramar', methods=['GET'])
def get_grammar():  # noqa: E501
    """Gets CTA grammar rules.

    This will return the grammar rules for specifying CTAs  # noqa: E501


    :rtype: object
    """
    return 'do some magic!'

@REFINER_API.route('/api/sample-scripts/<sample_name>', methods=['GET'])
def get_sample(sample_name):  # noqa: E501
    """returns a specified sample script

    By passing in the specified sample script name you are able to get a sample script  # noqa: E501

    :param sample_name: 
    :type sample_name: str

    :rtype: object
    """
    f = open(EXAMPLESDIRECTORY+sample_name,"r")
    example = f.readlines()
    return jsonify(name=sample_name,sample_script=example)

@REFINER_API.route('/api/sample-scripts', methods=['GET'])
def get_samples():  # noqa: E501
    """returns a list of available sample scripts

    Returns a list of available sample scripts which can be passed as a parameter to retrieve specific sample  # noqa: E501


    :rtype: None
    """
    examples = []
    for files in os.listdir(EXAMPLESDIRECTORY):
        examples.append(files)
    return str(examples)

@REFINER_API.route('/api/cta/<string:ctaName1>/refines/<string:ctaName2>', methods=['GET'])
def refine_ctas(ctaName1,ctaName2):  # noqa: E501
    """Gets refinements between two CTAs.

    By passing in the appropriate options, you can search for ctas which are currently defined in the system  # noqa: E501

    :param ctaName: gets refinements between two ctas
    :type ctaName: str

    :rtype: Refinement
    """
    return 'do some magic!'

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
    return 'do some magic!'


