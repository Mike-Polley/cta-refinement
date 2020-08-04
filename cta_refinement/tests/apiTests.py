""" Module provides unit testing functionality for REST API endpoints
    requires module pytest.
    To run at command line enter: pytest routeTests.py
"""
import pytest
import sys
sys.path.append("/var/www/cta_refinement")
from cta_refinement import app as flaskApp
import json

@pytest.fixture
def app():
    yield flaskApp

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(app, client):
    res = client.get('/api/cta')
    assert res.status_code == 200