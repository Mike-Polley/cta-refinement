This tool implements the theory of "Compositional asynchronous timed refinement".

(1) Installation instructions (Ubuntu only)
-------------------------------------------

(a) Install the python DBM binding, following the instructions 
in http://people.cs.aau.dk/~adavid/UDBM/python.html. 

Tips:
When installing the required Uppaal DBM Library (http://people.cs.aau.dk/~adavid/UDBM/), call: 
AR=ar ./configure
instead of ./configure.
For 64 bit architectures only, add the flag -fPIC to 
export CFLAGS :=  -DBOOST_DISABLE_THREADS in the makefile.

(b) Install Parglare (https://github.com/igordejanovic/parglare):
pip install parglare

(c) Install Graphviz (https://www.graphviz.org/):
sudo apt-get install graphviz

(d) Install graphviz (http://graphviz.readthedocs.io/en/stable/index.html):
pip install graphviz


(2) Running the tool
--------------------

The tool can be run with command: ./run.py <script_name>.
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

The full grammar of the language is in file 'grammar'.

(4) Benchmarking
----------------

We provide a small utility for generating arbitrarily large CTAs. It can be run with command: ./TestGen.py <number_of_states> <number_of_clocks>.
The output will be in file "test" and can be given in input to run.py.
# cta-refinement
