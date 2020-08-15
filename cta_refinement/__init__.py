from flask import Flask, render_template, request, url_for, redirect, send_file, Markup, jsonify, make_response, session
import sys
import os
import tempfile
from settings import DBMDIRECTORY, JSONDIRECTORY, GOGENERATOR
sys.path.append(DBMDIRECTORY), sys.path.append(GOGENERATOR)
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
    return render_template("index.html", pageName="Home")

@app.route("/share/output",methods=["POST","GET"])
@app.route("/output",methods=["POST","GET"])
def output():
    if request.args.get('c', 0, type=str) == 'false':
        try:
            a = request.args.get('a', 0, type=str)
            session.update({'currentScript' : str(a)})
            format = str(request.args.get('b', 0, type=str))
            tf = tempfile.NamedTemporaryFile().name
            scriptResponse = webScriptRefinementChecker(str(a),tf,format)
            tf = "files/imagetemp" + tf + "." + format
            return jsonify(result=Markup(scriptResponse),image=url_for('static',filename=tf))
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
    try:
        file = open(DBMDIRECTORY+"grammar","r")
        src = file.readlines()
        return render_template("grammar.html",src=src,len=len(src),pageName="Grammar Rules")
    except:
        return handle_404_error(404)

@app.route("/sample-scripts/atm")
def atm():
    try:
        file = open(DBMDIRECTORY+"Examples/ATM","r")
        src = file.read()
        return jsonify(src=Markup(src))
    except:
        return handle_404_json_error(404)

@app.route("/sample-scripts/fisher-mutual-exclusion")
def fisher():
    try:
        file = open(DBMDIRECTORY+"Examples/FisherMutualExclusion","r")
        src = file.read()
        return jsonify(src=Markup(src))
    except:
        return handle_404_json_error(404)

@app.route("/sample-scripts/ford-credit-portal")
def ford():
    try:
        file = open(DBMDIRECTORY+"Examples/FordCreditWebPortal","r")
        src = file.read()
        return jsonify(src=Markup(src))
    except:
        return handle_404_json_error(404)

@app.route("/sample-scripts/ooi-word-counting")
def ooi():
    try:
        file = open(DBMDIRECTORY+"Examples/OOIWordCounting","r")
        src = file.read()
        return jsonify(src=Markup(src))
    except:
        return handle_404_json_error(404)

@app.route("/sample-scripts/scheduled-task-protocol")
def task():
    try:
        file = open(DBMDIRECTORY+"Examples/ScheduledTaskProtocol","r")
        src = file.read()
        return jsonify(src=Markup(src))
    except:
        return handle_404_json_error(404)

@app.route("/sample-scripts/smtp-client")
def smtp():
    try:
        file = open(DBMDIRECTORY+"Examples/SMTPClient","r")
        src = file.read()
        return jsonify(src=Markup(src))
    except:
        return handle_404_json_error(404)

@app.route("/article")
def article():
    try:
        return send_file("static/files/article.pdf")
    except:
        return handle_404_error(404)

@app.route("/share",methods=['POST', 'GET'])
def share():
    if request.method == 'POST':
        Id = createId()
        genSession = Markup(request.form['script2'])

        start = []
        payload = {'id': Id, 'session': genSession}
        if not os.path.isfile(JSONDIRECTORY+'sessions.json'):
            start.append(payload)
            with open(JSONDIRECTORY+'sessions.json','w') as outfile:
                outfile.write(json.dumps(start))
        else:
            with open(JSONDIRECTORY+'sessions.json') as outfile:
                data = json.load(outfile)

            data.append(payload)
            with open(JSONDIRECTORY+'sessions.json','w') as outfile:
                outfile.write(json.dumps(data))
        return redirect("/share/"+str(Id))
    else:
        return render_template("index.html", pageName="Home")

@app.route("/share/<int:id>",methods=['GET'])
def getShare(id):
    try:
        data = json.loads(open(JSONDIRECTORY+'sessions.json','r').read())
        dict = next(item for item in data if item["id"] == id)
        sessions = dict.get('session')
        return render_template("index.html", pageName="home", sessions=sessions, id=id)
    except:
        return handle_404_error(404)

""" Check whether id already exists in file. If file doesn't exist it doesn't.
    Else search the file and check call yourself again if id found
"""
def createId():
    id = random.getrandbits(32)
    if not os.path.isfile(JSONDIRECTORY+'sessions.json'):
        return id
    else:
        data = json.loads(open(JSONDIRECTORY+'sessions.json','r').read())
        for item in data:
            if item["id"] == id:
                return createId()
            else:
                return id

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "CTA_REFINEMENT"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

### create swagger blueprint ###
app.register_blueprint(get_blueprint())


### add error handlers for api ###
@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return render_template('error.html',pageName="Oops",errorNo=400)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return render_template('error.html',pageName="Oops",errorNo=404)

@app.errorhandler(404)
def handle_404_json_error(_error):
    return jsonify(src="Oops Resource Not Found. We are working hard to fix this...",
    result="Oops Resource Not Found. We are working hard to fix this...")

@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return render_template('error.html',pageName="Oops",errorNo=500)


if __name__ == "__main__":
    app.run(threaded=True)
