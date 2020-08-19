""" Module provides unit testing functionality for url routes for web interface
    requires module pytest.
    To run at command line enter: pytest route_test.py
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

    """Test the homepage of web client
    """
def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200
    assert "Cta" in res.data

    """Test the grammar page of the web client
    """
def test_grammar(app,client):
    res = client.get('/grammar')
    assert res.status_code == 200
    assert "Command" in res.data

    """Test that output will fail with no input
    """
def test_output_failure(app,client):
    res = client.get('/output')
    assert res.status_code == 200
    assert "Failed" in res.data

    """Test the ATM sample script ajax
    """
def test_atm(app,client):
    res = client.get('/sample-scripts/atm')
    assert res.status_code == 200
    assert "User" in res.data

    """Test the fisher mutual exclusion sample ajax
    """
def test_fisher(app,client):
    res = client.get('/sample-scripts/fisher-mutual-exclusion')
    assert res.status_code == 200
    assert "Producer" in res.data

    """Test the ford credit portal sample ajax
    """
def test_ford(app,client):
    res = client.get('/sample-scripts/ford-credit-portal')
    assert res.status_code == 200
    assert "logged" in res.data

    """Test the OOI word counting sample ajax
    """
def test_ooi(app,client):
    res = client.get('/sample-scripts/ooi-word-counting')
    assert res.status_code == 200
    assert "M2" in res.data

    """Test the scheduled task protocol sample ajax
    """
def test_sched(app,client):
    res = client.get('/sample-scripts/scheduled-task-protocol')
    assert res.status_code == 200
    assert "U3" in res.data

    """Test the smtp client sample ajax
    """
def test_smtp(app,client):
    res = client.get('/sample-scripts/smtp-client')
    assert res.status_code == 200
    assert "Client" in res.data

    """Test the downloading copy of article ajax
    """
def test_article(app,client):
    res = client.get('/article')
    assert res.status_code == 200
    assert "PDF" in res.data
