import pytest
from .. import models

@pytest.fixture()
def store():
    """Build a test database.

    Using an in-memory SQLite database, prepare the data store
    for use. Retain as a session-scoped fixture, so that data 
    built in earlier tests is available for later tests."""

    database = create_database('sqlite:')
    store = Store(database)
    # Create table for models.Source
    store.execute("CREATE TABLE source "
                  "(id INTEGER PRIMARY KEY, name VARCHAR, url VARCHAR)")
    # Create tables for models.Step and models.SourceStep
    store.execute("CREATE TABLE step "
                  "(id INTEGER PRIMARY KEY, action VARCHAR, target VARCHAR, \"values\" VARCHAR)")
    store.execute("CREATE TABLE source_step "
                  "(source_id INTEGER, step_id INTEGER, sequence INTEGER, PRIMARY KEY (source_id, step_id), UNIQUE (source_id, sequence))")
    return store

@pytest.fixture()
def source():
    """Create a test source."""

    source = models.Source(name=u"Joe's Funerals.com", url=u"http://www.joesfunerals.com")
    return source

@pytest.fixture()
def sources(source):
    """Create three test sources."""

    source2 = models.Source(name=u"Bob's Funerals.com", url=u"http://www.bobsfunerals.com")
    source3 = models.Source(name=u"Jim's Funerals.com", url=u"http://www.jimsfunerals.com")
    return (source, source2, source3)
