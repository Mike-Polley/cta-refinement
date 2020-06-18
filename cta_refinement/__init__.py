from flask import Flask, render_template, request, url_for, redirect
import sys
sys.path.append('/var/www/cta_refinement/cta_refinement/dbmModules')
from CtaWebFunctions import *

app = Flask(__name__)

@app.route("/",methods=["POST","GET"])
def home():
    if request.method == "POST":
        scriptInput = request.form["script"]
        response = webScriptRefinementChecker(str(scriptInput))
        return render_template("output.html",script = response)
    else:
        return render_template("index.html")


@app.route("/sample-scripts/ATM")
def atm():
    return render_template("ATM.html")

if __name__ == "__main__":
    app.run(threaded=True)
