from .. import models
import pytest
from storm.locals import *

@pytest.fixture(scope='module')
def store():
    database = create_database('sqlite:')
    store = Store(database)
    # Create table for models.Source
    store.execute("CREATE TABLE source "
                  "(id INTEGER PRIMARY KEY, name VARCHAR, url VARCHAR)")
    # Create tables for models.Step and models.SourceStep
    store.execute("CREATE TABLE step "
                  "(id INTEGER PRIMARY KEY, action VARCHAR, target VARCHAR, \"values\" VARCHAR)")
    store.execute("CREATE TABLE source_step "
                  "(source_id INTEGER, step_id INTEGER, sequence INTEGER, PRIMARY KEY (source_id, step_id))")
    return store

class TestSource:
    def test_create(self, store):
        test_source = models.Source()
        test_source.name = u"Joe's Funerals.com"
        test_source.url = u"http://www.joesfunerals.com"
        store.add(test_source)
        store.commit()
        assert u"{source!r}".format(source=test_source) == u"Source(name=\"Joe's Funerals.com\", url=\"http://www.joesfunerals.com\", id=1)"

    def test_find(self, store):
        test_source_name = u"Joe's Funerals.com"
        test_source_url = u"http://www.joesfunerals.com"
        test_source_id = 1
        found_source = store.find(models.Source, models.Source.name == test_source_name).one()
        assert u"Source(name=\"{name}\", url=\"{url}\", id={id})".format(name=test_source_name, url=test_source_url, id=test_source_id) == found_source.__repr__()

class TestStep:
    def test_create(self, store):
        test_step = models.Step(u"goto", u"http://www.joesfunerals.com")
        store.add(test_step)
        store.commit()
        assert test_step == store.get(models.Step, 1)

    def test_add(self, store):
        test_step = store.get(models.Step, 1)
        test_source = store.get(models.Source, 1)
        test_step2 = models.Step(u"text", u"#password", u"foo|bar")
        test_source.steps.add(test_step)
        test_source.steps.add(test_step2)
        store.commit()

    def test_invalid_action(self, store):
        with pytest.raises(ValueError):
            invalid_step = models.Step(u"florp", u"http://www.florp.com")

    def test_invalid_url(self, store):
        with pytest.raises(ValueError):
            invalid_step = models.Step(u"goto", u"foo-bar-bork")

    def test_find(self, store):
        test_source = store.get(models.Source, 1)
        test_step1 = store.get(models.Step, 1)
        test_step2 = store.get(models.Step, 2)
        assert test_step1 in test_source.steps
        assert test_step2 in test_source.steps

    def test_mangle(self, store):
        test_source = store.get(models.Source, 1)
        test_instructions = [(u"goto", u"http://www.joesfunerals.com"), 
                             (u"text", u"#password", u"foo"),
                             (u"goto", u"http://www.joesfunerals.com"), 
                             (u"text", u"#password", u"bar")]
        assert test_instructions == test_source.instructions()
