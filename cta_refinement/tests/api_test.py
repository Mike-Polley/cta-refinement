""" Module provides unit testing functionality for REST API endpoints
    requires module pytest.
    To run at command line enter: pytest api_test.py
"""
import pytest
import sys
sys.path.append("/var/www/cta_refinement")
from cta_refinement import app as flaskApp
from werkzeug.test import EnvironBuilder
import json

@pytest.fixture
def app():
    yield flaskApp

@pytest.fixture
def client(app):
    return app.test_client()

    """Test get all CTAs in session endpoint
    """
def test_index(app, client):

    """Test get all CTAs in session endpoint
    """
    res = client.get('/api/cta')
    assert res.status_code == 200

def test_get_specific_cta(app, client):
    cta = { "name" : "cta1", "CTA" : "{Init u0; u0 UW!task(x < 10,{x}) u1; u1 AU?result(x <= 200) u2;}"}
    with app.test_client() as c:
        client.post(path='/api/cta/cta1',json=cta)
        res = client.get('/api/cta/cta1')
        assert request.args['name'] == "cta1"
        #assert res.status_code == 200

#def test_delete_cta(app, client):
#    client.post()
#    res = client.delete()
#    res.status_code == 200

def test_post_cta(app, client):
    cta = test_cta()
    res = client.post(path='/api/cta/{cta_name}', method="POST", json=cta)
    res.status_code == 200

#def test_put_cta(app, client):
#    client.post('/api/cta/{cta_name}')
#    res = client.put()
#    res.status_code == 200

def test_grammar(app, client):

    """Test get the grammar rules API endpoint
    """
    res = client.get('/api/grammar')
    assert "Command" in res.data
    assert res.status_code == 200

def test_specific_sample(app, client):

    """Test get a specific sample script endpoint
    """
    res = client.get('/api/sample-scripts/ATM')
    assert "Bank" in res.data
    assert res.status_code == 200

def test_samples(app, client):

    """Test getting list of available sample scripts
    """
    res = client.get('/api/sample-scripts')
    assert "ATM" in res.data
    assert res.status_code == 200

def get_test_environment(method):

    if method == "POST":
        env = EnvironBuilder(method="POST", json={ "name" : "cta1", "CTA" : "{Init u0; u0 UW!task(x < 10,{x}) u1; u1 AU?result(x <= 200) u2;}"})

def example_cta():
    return {"name" : "cta1", "CTA" : "{Init u0; u0 UW!task(x < 10,{x}) u1; u1 AU?result(x <= 200) u2;}"}

