""" Module provides unit testing functionality for REST API endpoints
    requires module pytest.
    To run at command line enter: pytest api_test.py
"""
import pytest
import sys
sys.path.append("/var/www/cta_refinement")
from cta_refinement import app as flaskApp

@pytest.fixture
def app():
    yield flaskApp

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def session(app, client):
    cta1 = {"name" : "cta1", "CTA" : "{Init q0; q0 UM!card q1; q1 MU?pinrequest({x}) q2; q2 UM!pin(x <= 30) q3; q3 MU?menu q4;}"}
    cta2 = {"name" : "cta2", "CTA" : "{Init q0; q0 UM!card(x == 0) q1; q1 MU?pinrequest({x}) q2; q2 UM!pin(x == 0) q3; q3 MU?menu q4;}"}
    client.post(path='/api/cta/cta1', method="POST", json=cta1)
    return client.post(path='/api/cta/cta2', method="POST", json=cta2)

def test_index(app, client, session):

    """Test get all CTAs in session endpoint
    """
    res = client.get('/api/cta')
    assert res.status_code == 200

def test_get_specific_cta(app, client, session):
    """Test get specific CTA in session endpoint
    """
    res = client.get('/api/cta/cta2')
    assert res.status_code == 200

def test_delete_cta(app, client, session):

    """Test delete specific CTA enpoint
    """
    res = client.delete('/api/cta/cta1')
    assert res.status_code == 200

def test_post_cta(app, client):

    """Test post a new CTA endpoint
    """
    cta = {"name" : "cta3", "CTA" : "{Init u0; u0 UW!task(x < 10,{x}) u1; u1 AU?result(x <= 200) u2;}"}
    res = client.post(path='/api/cta/cta3', method="POST", json=cta)
    assert res.status_code == 200

def test_put_cta(app, client, session):

    """Test update a specific CTA endpoint
    """
    cta = {"name" : "cta1", "CTA" : "{Init u0; u0 UW!task(x == 0,{x}) u1; u1 AU?result(x <= 200 & x >= 199) u2;}"}
    res = client.put(path='/api/cta/cta1', method="PUT", json=cta)
    assert res.status_code == 200

def test_refines(app, client, session):

    """Test refinement between two CTAs
    """
    res = client.get('/api/cta/cta1/refines/cta2')
    assert res.status_code == 200

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


