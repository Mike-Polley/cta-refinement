#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/cta-refinement/")
path = "/usr/local/lib/python2.7/site-packages/"
if path not in sys.path:
	sys.path.append(path)


from FlaskApp import app as application
application.secret_key = 'Add your secret key'
