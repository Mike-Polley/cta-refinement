from flask import Flask, render_template, request, url_for, redirect, send_file, Markup,jsonify
import sys
import os
import tempfile
from settings import DBMDIRECTORY, JSONDIRECTORY
sys.path.append(DBMDIRECTORY)
from CtaWebFunctions import *
import random
import json
from time import sleep

app = Flask(__name__)


@app.route("/",methods=["POST","GET"])
def home():
    return render_template("index.html", pageName="Home")

@app.route("/share/output",methods=["POST","GET"])
@app.route("/output",methods=["POST","GET"])
def output():
    a = request.args.get('a', 0, type=str)
    format = str(request.args.get('b', 0, type=str))
    tf = tempfile.NamedTemporaryFile().name
    scriptResponse = webScriptRefinementChecker(str(a),tf,format)
    tf = "files/imagetemp" + tf + "." + format
    return jsonify(result=Markup(scriptResponse),image=url_for('static',filename=tf))

@app.route("/grammar")
def grammar():
    f = open(DBMDIRECTORY+"grammar","r")
    src = f.readlines()
    return render_template("grammar.html",src=src,len=len(src),pageName="Grammar Rules")

@app.route("/sample-scripts/atm")
def atm():
    f = open(DBMDIRECTORY+"Examples/ATM","r")
    src = f.read()
    return jsonify(src=Markup(src))

@app.route("/sample-scripts/fisher-mutual-exclusion")
def fisher():
    f = open(DBMDIRECTORY+"Examples/FisherMutualExclusion","r")
    src = f.read()
    return jsonify(src=Markup(src))

@app.route("/sample-scripts/ford-credit-portal")
def ford():
    f = open(DBMDIRECTORY+"Examples/FordCreditWebPortal","r")
    src = f.read()
    return jsonify(src=Markup(src))

@app.route("/sample-scripts/ooi-word-counting")
def ooi():
    f = open(DBMDIRECTORY+"Examples/OOIWordCounting","r")
    src = f.read()
    return jsonify(src=Markup(src))

@app.route("/sample-scripts/scheduled-task-protocol")
def task():
    f = open(DBMDIRECTORY+"Examples/ScheduledTaskProtocol","r")
    src = f.read()
    return jsonify(src=Markup(src))

@app.route("/sample-scripts/smtp-client")
def smtp():
    f = open(DBMDIRECTORY+"Examples/SMTPClient","r")
    src = f.read()
    return jsonify(src=Markup(src))

@app.route("/article")
def article():
    return send_file("static/files/article.pdf")

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
    data = json.loads(open(JSONDIRECTORY+'sessions.json','r').read())
    dict = next(item for item in data if item["id"] == id)
    session = dict.get('session')
    return render_template("index.html", pageName="home", session=session, id=id)

""" Check whether id already exists in file. If file doesn't exist it doesn't.
    else search the file and check call yourself again if id found
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


if __name__ == "__main__":
    app.run(threaded=True)
