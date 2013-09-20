import pytest
from storm.locals import *
from .. import models
from datetime import datetime, timedelta

lorem_ipsum = u"""<html>
    <body>
        <ul>
           <li>Lorem ipsum dolor sit amet, consectetuer adipiscing elit.</li>
           <li>Aliquam tincidunt mauris eu risus.</li>
           <li>Vestibulum auctor dapibus neque.</li>
        </ul>
    </body>
</html>"""

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
    store.execute("CREATE TABLE dump "
                  "(id INTEGER PRIMARY KEY, source_id INTEGER, title VARCHAR, mined INT, locked VARCHAR, dump MEDIUMTEXT)")
    store.execute("CREATE TABLE funeral_home "
                  "(id INTEGER PRIMARY KEY, name VARCHAR, city VARCHAR, state VARCHAR, source_id INTEGER)")
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

@pytest.fixture()
def step():
    """Create a test step."""
    step = models.Step(action=u"goto", target=u"http://www.joesfunerals.com")
    return step

@pytest.fixture()
def steps(step):
    """Create three test steps."""
    step2 = models.Step(action=u"text", target=u"#password", values="foo|bar")
    step3 = models.Step(action=u"dump", target=u"test dump")
    return (step, step2, step3)

@pytest.fixture()
def dump():
    """Create a test dump."""
    dump = models.Dump(title=u"test dump", data=lorem_ipsum)
    return dump

@pytest.fixture()
def dumps(dump):
    """Create three test dumps."""
    dump2 = models.Dump(title=u"test2 dump", data=lorem_ipsum)
    dump3 = models.Dump(title=u"test dump", data=lorem_ipsum)
    return (dump, dump2, dump3)

@pytest.fixture()
def home():
    home = models.FuneralHome(name=u"Joe's Funerals")
    return home

@pytest.fixture()
def homes(home):
    home2 = models.FuneralHome(name=u"Bob's Funerals")
    home3 = models.FuneralHome(name=u"Jim's Funerals")
    return (home, home2, home3)

@pytest.fixture()
def death():
    death = models.Death(name="James Jameson", date_death=datetime(2013, 6, 5), date_service=datetime(2013, 6, 10), 
            date_burial=datetime(2013, 6, 13), city="Jameston", state="VA")
    return death
