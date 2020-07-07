""" Module provides unit testing functionality for url routes for web interface
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
    res = client.get('/')
    assert res.status_code == 200
    assert "Cta" in res.data

def test_grammar(app,client):
    res = client.get('/grammar')
    assert res.status_code == 200
    assert "Command" in res.data

def test_ouput_failure(app,client):
    res = client.get('/output')
    assert res.status_code == 200
    assert "Failed" in res.data

def test_atm(app,client):
    res = client.get('/sample-scripts/atm')
    assert res.status_code == 200
    assert "User" in res.data

def test_fisher(app,client):
    res = client.get('/sample-scripts/fisher-mutual-exclusion')
    assert res.status_code == 200
    assert "Producer" in res.data

def test_ford(app,client):
    res = client.get('/sample-scripts/ford-credit-portal')
    assert res.status_code == 200
    assert "logged" in res.data

def test_ooi(app,client):
    res = client.get('/sample-scripts/ooi-word-counting')
    assert res.status_code == 200
    assert "M2" in res.data

def test_sched(app,client):
    res = client.get('/sample-scripts/scheduled-task-protocol')
    assert res.status_code == 200
    assert "U3" in res.data

def test_smtp(app,client):
    res = client.get('/sample-scripts/smtp-client')
    assert res.status_code == 200
    assert "Client" in res.data

def test_article(app,client):
    res = client.get('/article')
    assert res.status_code == 200
    assert "PDF" in res.data