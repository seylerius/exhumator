from .. import models
import pytest
from storm.locals import *

@pytest.fixture()
def store(scope='module'):
    database = create_database('sqlite:')
    store = Store(database)
    store.execute("CREATE TABLE source "
                  "(id INTEGER PRIMARY KEY, name VARCHAR, url VARCHAR)")
    return store

class TestSource:
    def test_create(self, store):
        test_source = models.Source()
        test_source.name = "Joe's Funerals.com"
        test_source.url = "http://www.joesfunerals.com"
        store(test_source)
        store.flush()
        assert "{source!r}".format(source=test_source) == "Source(name=\"Joe's Funerals.com\", url=\"http://www.joesfunerals.com\", id=1)"

    def test_find(self, store):
        test_source = store.find(models.Source, models.Source.name == "Joe's Funerals.com").one()
        assert "{source!r}".format(source=test_source) == "Source(name=\"Joe's Funerals.com\", url=\"http://www.joesfunerals.com\", id=1)"
