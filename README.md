This project builds on the a tool implemented to check refinements between commmunicating
asynchronous timed automated. We provide a web based user interface for interacting with the
tool this can be found when connecting to University of Kent VPN at 129.12.44.117. 
Our web interface provides syntax highlighting, validation of CTA form, generation of graphical
representation within the browser, conversion to GOLang (through the inclusion of another tool which we did not develop)
upload of scripts, download of outputs, sharing of scripts. All sample scripts can be used.

We also provide a REST API which can be used to integrate this tool into further applications
the end points of this can be found at /swagger/.


The Web implementation has many dependecies and is currently only compatible with Python2.
The settings file includes directories where we would expect files to be located within a Linux
environment - these can be altered should you wish to change locations.

(1) Installation instructions (Ubuntu only)
-------------------------------------------

(a) Install the python DBM binding, following the instructions 
in http://people.cs.aau.dk/~adavid/UDBM/python.html. 

Tips:
When installing the required Uppaal DBM Library (https://github.com/airbornemihir/uppaal-dbm), call: 
AR=ar ./configure
instead of ./configure.
For 64 bit architectures only, add the flag -fPIC to 
export CFLAGS :=  -DBOOST_DISABLE_THREADS in the makefile.

(b) Install Parglare version 0.10.0 (https://github.com/igordejanovic/parglare):
pip install parglare==0.10.0

(c) Install Graphviz (https://www.graphviz.org/):
sudo apt-get install graphviz

(d) Install graphviz (http://graphviz.readthedocs.io/en/stable/index.html):
pip install graphviz

(e) Install Flask (https://flask.palletsprojects.com/en/1.1.x/):
pip install flask

(f) Install flask_swagger_ui  (https://pypi.org/project/flask-swagger-ui/):
pip install flask-swagger-ui

(f) Install pytest  (https://docs.pytest.org/en/stable/getting-started.html#install-pytest):
pip install -U pytest

(2) Running the tool
--------------------

To start the web server and view in browser run python2 __ini__.py

The tool can still be run on command line and can  be run with command: ./run.py <script_name>.
Directory 'Examples' contains tests scripts described in the paper.

(3) Scripting language
----------------------

The tool allows CTA creation, drawing and refinement checking
through a simple scripting language.
CTA are created, for instance:

```
Cta U = {
Init u0;
u0 UW!task(x < 10,{x}) u1;
u1 AU?result(x <= 200) u2; 
};
```

U is the CTA name,
Init u0 marks u0 as the initial state.
The remaining lines defines edges.
States are automatically inferred.
Guards can be omitted when True. Similarly,
an omitted reset sets is interpreted as the empty reset set.

CTAs can be drawed with:

```
Show(U);
```

Refinement checking is performed with:

```
U1 refines? U2;
```

----------------------

The full grammar of the language is on the page 'grammar'.

Relevant and helpful links:

Original Tool - https://github.com/cta-refinement/cta-refinement

Swagger file and API - https://app.swaggerhub.com/apis/CO884CTAProj/cta_refinement_api/1.0.0

Guide to creating .wsgi - https://flask.palletsprojects.com/en/master/deploying/mod_wsgi/#creating-a-wsgi-file


