""" Module provides unit testing functionality for REST API endpoints
    requires module pytest.
    To run at command line enter: pytest apiTests.py
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

    """Test get all CTAs in session endpoint
    """
def test_index(app, client):
    res = client.get('/api/cta')
    assert res.status_code == 200

    """Test get the grammar rules API endpoint
    """
def test_grammar(app, client):
    res = client.get('/api/grammar')
    assert "Command" in res.data 
    assert res.status_code == 200

    """Test get a specific sample script endpoint
    """
def test_specific_sample(app, client):
    res = client.get('/api/sample-scripts/ATM')
    assert "Bank" in res.data 
    assert res.status_code == 200

    """Test getting list of available sample scripts
    """
def test_samples(app,client):
    res = client.get('/api/sample-scripts')
    assert "ATM" in res.data 
    assert res.status_code == 200