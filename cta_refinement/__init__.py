""" Provides the URL routes for the Web Interface implementation.
"""
from flask import Flask, render_template, request, url_for, redirect 
from flask import send_file, Markup, jsonify, make_response, session
import sys
import os
import tempfile
from settings import DBM_DIRECTORY, JSON_DIRECTORY, GO_GENERATOR
sys.path.append(DBM_DIRECTORY), sys.path.append(GO_GENERATOR)
from CtaWebFunctions import *
import random
import json
from flask_swagger_ui import get_swaggerui_blueprint
from api import get_blueprint
from Cta_Loader import load_automata
from Golang_generator import generate_go_lang

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/",methods=["POST","GET"])
def home():
    """ Renders the homepage (index.html)
    """
    return render_template("index.html", pageName="Home")

@app.route("/share/output",methods=["POST","GET"])
@app.route("/output",methods=["POST","GET"])
def output():
    """ Logic for handling the refinement. Gets the AJAX call and file type 
        format, creates a temporary file for the picture passes it to webscript
        refinement checker URL passes the result back.
        If the user chooses to generate GO lang pass to go lang tool and pass
        back
    """
    if request.args.get('c', 0, type=str) == 'false':
        try:
            a = request.args.get('a', 0, type=str)
            session.update({'currentScript' : str(a)})
            format = str(request.args.get('b', 0, type=str))
            tf = tempfile.NamedTemporaryFile().name
            script_response = web_script_refinement_checker(str(a),tf,format)
            tf = "files/imagetemp" + tf + "." + format
            return jsonify(result=Markup(script_response),image=url_for('static'
            ,filename=tf))
        except:
            return handle_404_json_error(404)
    else:
        try:
            a = request.args.get('a', 0, type=str)
            automata_list = load_automata(a)
            golang_line = generate_go_lang(automata_list)
            return jsonify(result=Markup(golang_line))
        except:
            return handle_404_json_error(404)



@app.route("/grammar")
def grammar():
    """ Returns the grammar rules - opens file and passes to template.
    """
    try:
        file = open(DBM_DIRECTORY+"grammar","r")
        src = file.readlines()
        return render_template("grammar.html",src=src,len=len(src),
        pageName="Grammar Rules")
    except:
        return handle_404_error(404)

@app.route("/sample-scripts/atm")
def atm():
    """ Returns the atm sample script - uses AJAX call opens file passes
        back JSON
    """
    try:
        file = open(DBM_DIRECTORY+"Examples/ATM","r")
        src = file.read()
        return jsonify(src=Markup(src))
    except:
        return handle_404_json_error(404)

@app.route("/sample-scripts/fisher-mutual-exclusion")
def fisher():
    """ Returns the fisher-mutual-exclusion sample script - uses AJAX call opens 
        file passes back JSON
    """
    try:
        file = open(DBM_DIRECTORY+"Examples/FisherMutualExclusion","r")
        src = file.read()
        return jsonify(src=Markup(src))
    except:
        return handle_404_json_error(404)

@app.route("/sample-scripts/ford-credit-portal")
def ford():
    """ Returns the ford creadit portal sample script - uses AJAX call opens 
        file passes back JSON
    """
    try:
        file = open(DBM_DIRECTORY+"Examples/FordCreditWebPortal","r")
        src = file.read()
        return jsonify(src=Markup(src))
    except:
        return handle_404_json_error(404)

@app.route("/sample-scripts/ooi-word-counting")
def ooi():
    """ Returns the ooi-word-counting sample script - uses AJAX call opens 
        file passes back JSON
    """
    try:
        file = open(DBM_DIRECTORY+"Examples/OOIWordCounting","r")
        src = file.read()
        return jsonify(src=Markup(src))
    except:
        return handle_404_json_error(404)

@app.route("/sample-scripts/scheduled-task-protocol")
def task():
    """ Returns the scheduled-task-protocol sample script - uses AJAX call opens 
        file passes back JSON
    """
    try:
        file = open(DBM_DIRECTORY+"Examples/ScheduledTaskProtocol","r")
        src = file.read()
        return jsonify(src=Markup(src))
    except:
        return handle_404_json_error(404)

@app.route("/sample-scripts/smtp-client")
def smtp():
    """ Returns the smtp sample script - uses AJAX call opens 
        file passes back JSON
    """
    try:
        file = open(DBM_DIRECTORY+"Examples/SMTPClient","r")
        src = file.read()
        return jsonify(src=Markup(src))
    except:
        return handle_404_json_error(404)

@app.route("/article")
def article():
    """ Returns the timed automata article returns PDF to browser
    """
    try:
        return send_file("static/files/article.pdf")
    except:
        return handle_404_error(404)

@app.route("/share",methods=['POST', 'GET'])
def share():
    """ Logic for the share URL routing grabs the editor content, generates
        an id using function. Adds to JSON file. If no JSON file create one
        else get JSON data append this to it and write back to file. Redirect
        to parameratized share url route.
    """
    if request.method == 'POST':
        id = create_id()
        gen_session = Markup(request.form['script2'])

        start = []
        payload = {'id': id, 'session': gen_session}
        if not os.path.isfile(JSON_DIRECTORY+'sessions.json'):
            start.append(payload)
            with open(JSON_DIRECTORY+'sessions.json','w') as outfile:
                outfile.write(json.dumps(start))
        else:
            with open(JSON_DIRECTORY+'sessions.json') as outfile:
                data = json.load(outfile)
            data.append(payload)
            with open(JSON_DIRECTORY+'sessions.json','w') as outfile:
                outfile.write(json.dumps(data))
        return redirect("/share/"+str(id))
    else:
        return render_template("index.html", pageName="Home")

@app.route("/share/<int:id>",methods=['GET'])
def get_share(id):
    """ Parameratized share URL route gets the ID supplied searches for data to
        display if not found through a 404 resources not found error.
    """
    try:
        data = json.loads(open(JSON_DIRECTORY+'sessions.json','r').read())
        dict = next(item for item in data if item["id"] == id)
        sessions = dict.get('session')
        return render_template("index.html", pageName="home", sessions=sessions 
        ,id=id)
    except:
        return handle_404_error(404)


def create_id():
    """ Check whether id already exists in file. If file doesn't exist it doesn't.
    Else search the file and check call yourself again if id found
    """
    id = random.getrandbits(32)
    if not os.path.isfile(JSON_DIRECTORY+'sessions.json'):
        return id
    else:
        data = json.loads(open(JSON_DIRECTORY+'sessions.json','r').read())
        for item in data:
            if item["id"] == id:
                return create_id()
            else:
                return id

"""For the flask_swagger_ui implementation """
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "CTA_REFINEMENT"
    }
)
"""Register the Swagger blueprint"""
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
app.register_blueprint(get_blueprint())



@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error as html page"""
    return render_template('error.html',pageName="Oops",errorNo=400)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error as html page"""
    return render_template('error.html',pageName="Oops",errorNo=404)

@app.errorhandler(404)
def handle_404_json_error(_error):
    """Return a http 404 error as JSON this is for the AJAX calls"""
    return jsonify(src="Oops Resource Not Found. We are working hard to fix this...",
    result="Oops Resource Not Found. We are working hard to fix this...")

@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error as html page"""
    return render_template('error.html',pageName="Oops",errorNo=500)


if __name__ == "__main__":
    app.run(threaded=True)
