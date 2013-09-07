from .. import models
import pytest
from storm.locals import *

@pytest.fixture()
def store(scope='session'):
    database = create_database('sqlite:')
    store = Store(database)
    store.execute("CREATE TABLE source "
                  "(id INTEGER PRIMARY KEY, name VARCHAR, url VARCHAR)")
    return store

class TestSource:
    def test_create(self, store):
        test_source = models.Source()
        test_source.name = u"Joe's Funerals.com"
        test_source.url = u"http://www.joesfunerals.com"
        store.add(test_source)
        store.flush()
        store.commit()
        assert u"{source!r}".format(source=test_source) == u"Source(name=\"Joe's Funerals.com\", url=\"http://www.joesfunerals.com\", id=1)"

    def test_find(self, store):
        found_source = store.get(models.Source, 1)
        assert found_source
