from flask import Flask, render_template, request, url_for, redirect, send_file, Markup
import sys
import tempfile
sys.path.append('/var/www/cta_refinement/cta_refinement/dbmModules')
from CtaWebFunctions import *

app = Flask(__name__)

@app.route("/",methods=["POST","GET"])
def home():
    if request.method == "POST":
        scriptInput = request.form["script"]
        tf = tempfile.NamedTemporaryFile().name
        response = webScriptRefinementChecker(str(scriptInput),tf)
        tf = "files/imagetemp" + tf + ".png"
        sepResponse = ""
        for char in response:
           if char == ".":
              sepResponse = sepResponse + ".<br>"
           else:
              sepResponse = sepResponse + char
        return render_template("output.html",response = Markup(sepResponse),image=tf,pageName="Home")
    else:
        return render_template("index.html",pageName="Home")

@app.route("/grammar")
def grammar():
    f = open("dbmModules/grammar","r")
    src = f.readlines()
    return render_template("grammar.html",src=src,len=len(src),pageName="Grammar Rules")

@app.route("/sample-scripts/atm")
def atm():
    f = open("/var/www/cta_refinement/cta_refinement/dbmModules/Examples/ATM","r")
    src = f.readlines()
    return render_template("examples.html", src=src, len=len(src),pageName="ATM")

@app.route("/sample-scripts/fisher-mutual-exclusion")
def fisher():
    f = open("/var/www/cta_refinement/cta_refinement/dbmModules/Examples/FisherMutualExclusion","r")
    src = f.readlines()
    return render_template("examples.html", src=src, len=len(src),pageName="Fisher Mutual Exclusion")

@app.route("/sample-scripts/ford-credit-portal")
def ford():
    f = open("/var/www/cta_refinement/cta_refinement/dbmModules/Examples/FordCreditWebPortal","r")
    src = f.readlines()
    return render_template("examples.html", src=src, len=len(src),pageName="Ford Credit Portal")

@app.route("/sample-scripts/ooi-word-counting")
def ooi():
    f = open("/var/www/cta_refinement/cta_refinement/dbmModules/Examples/OOIWordCounting","r")
    src = f.readlines()
    return render_template("examples.html", src=src, len=len(src),pageName="OOI Word Counting")

@app.route("/sample-scripts/scheduled-task-protocol")
def task():
    f = open("/var/www/cta_refinement/cta_refinement/dbmModules/Examples/ScheduledTaskProtocol","r")
    src = f.readlines()
    return render_template("examples.html", src=src, len=len(src),pageName="Scheduled Task Protocol")

@app.route("/sample-scripts/smtp-client")
def smtp():
    f = open("/var/www/cta_refinement/cta_refinement/dbmModules/Examples/SMTPClient","r")
    src = f.readlines()
    return render_template("examples.html", src=src, len=len(src),pageName="SMTP Client")

@app.route("/article")
def article():
    return send_file("static/files/article.pdf")


if __name__ == "__main__":
    app.run(threaded=True)
