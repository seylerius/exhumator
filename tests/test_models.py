from .. import models
import pytest
from storm.locals import *

class TestSource:
    def test_create(self, store, source):
        store.add(source)
        store.commit()

    def test_find(self, store, source):
        store.add(source)
        found_source = store.find(models.Source, models.Source.name == source.name).one()
        assert found_source is source

class TestStep:
    def test_create(self, store, step):
        store.add(step)
        store.commit()
        assert step is store.get(models.Step, step.id)

    def test_invalid_action(self):
        with pytest.raises(ValueError):
            invalid_step = models.Step(u"florp", u"http://www.florp.com")

    def test_invalid_url(self):
        with pytest.raises(ValueError):
            invalid_step = models.Step(u"goto", u"foo-bar-bork")

    def test_find(self, store, source, steps):
        """Do steps associate properly with a source?"""
        store.add(source)
        for step in steps:
            store.add(step)
        store.flush()
        for step in steps:
            source.steps.add(step)
        store.flush()
        for step in steps:
            assert step in source.steps

    def test_mangle(self, store, source, steps):
        """Do source scraping instructions format properly?"""
        store.add(source)
        for step in steps:
            store.add(step)
        store.flush()
        for step in steps:
            source.steps.add(step)
            store.flush()
        test_instructions = [(u'goto', (u'http://www.joesfunerals.com',)), 
                             (u'text', (u'#password', u'foo')), 
                             (u'dump', (u'test dump',)),
                             (u'goto', (u'http://www.joesfunerals.com',)), 
                             (u'text', (u'#password', u'bar')),
                             (u'dump', (u'test dump',))]
 
        assert test_instructions == source.instructions()

class TestDump:
    def test_create(self, store, dump):
        """Can a dump be instantiated?"""
        store.add(dump)
        store.flush()
        assert dump is store.get(models.Dump, dump.id)

    def test_find(self, store, source, dump):
        """Can a dump be found based on source_id and title?"""
        store.add(source)
        store.add(dump)
        store.flush()
        source.dumps.add(dump)
        store.flush()
        assert dump is store.find(models.Dump, models.Dump.source_id == source.id, models.Dump.title == dump.title).one()

    def test_unmined(self, store, dumps):
        """Find unmined dumps."""
        for dump in dumps:
            store.add(dump)
        store.flush()
        unmined_dumps = store.find(models.Dump, models.Dump.mined == False)
        for dump in unmined_dumps:
            assert dump in dumps

class TestFuneralHome:
    def test_create(self, store, home):
        store.add(home)
        store.flush()
        assert home is store.get(models.Home, home.id)

    def test_find(self, store, source, home):
        store.add(source)
        store.add(home)
        store.flush()
        home.source = source
        store.flush()
        assert home in source.homes
