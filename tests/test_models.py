from .. import models
import pytest
from storm.locals import *

class TestSource:
    def test_create(self, store, source):
        """Can a source instantiate and commit?"""

        store.add(source)
        store.commit()

    def test_find(self, store, source):
        """Can a source be searched for in the database?"""

        store.add(source)
        found_source = store.find(models.Source, models.Source.name == source.name).one()
        assert found_source is source

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
        store.flush()
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
        print test_source.instructions()
        test_instructions = [(u'goto', (u'http://www.joesfunerals.com',)), 
                             (u'text', (u'#password', u'foo')), 
                             (u'goto', (u'http://www.joesfunerals.com',)), 
                             (u'text', (u'#password', u'bar'))]
 
        assert test_instructions == test_source.instructions()
