from flask import Flask, render_template, request, url_for, redirect, send_file, Markup,jsonify
import sys
import tempfile
from settings import DBMDIRECTORY
sys.path.append(DBMDIRECTORY)
from CtaWebFunctions import *

app = Flask(__name__)


@app.route("/",methods=["POST","GET"])
def home():
    return render_template("index.html", pageName="Home")

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


if __name__ == "__main__":
    app.run(threaded=True)
