from storm.locals import *
import re
import itertools

models = []
actions = [u"goto", u"click", u"select", u"text", u"frame", u"dump"]
actions_with_values = [u"select", u"text"]
url_regex = re.compile(r"^(http(?:s)?\:\/\/[a-zA-Z0-9\-]+(?:\.[a-zA-Z0-9\-]+)*\.[a-zA-Z]{2,6}(?:\/?|(?:\/[\w\-]+)*)(?:\/?|\/\w+\.[a-zA-Z]{2,4}(?:\?[\w]+\=[\w\-]+)?)?(?:\&[\w]+\=[\w\-]+)*)$")

def listify(x):
    if type(x) not in [tuple, list]:
        x = [x]
    return x

def expanded_calls(step):
    args = step[1:]
    listified_args = [listify(x) for x in args]
    for args_combo in itertools.product(*listified_args):
        yield step[0], args_combo

class Step(object):
    __storm_table__ = "step"
    id = Int(primary=True)
    action = Unicode()
    target = Unicode()
    values = Unicode()

    def __init__(self, action, target, values=None):
        if action not in actions:
            raise ValueError(u'"{action}" is not a valid action.'.format(action=action))
        if action in actions_with_values:
            if values is None:
                raise ValueError(u'"{action}" requires a value.'.format(action=action))
            else:
                if type(values) is list:
                    self.values = "|".join(values)
                elif type(values) in [str, unicode]:
                    self.values = unicode(values)
                else:
                    raise ValueError(u'Invalid value type')
        if action == u"goto" and not url_regex.match(target):
            raise ValueError(u'Invalid target URL: {url}'.format(url=target))

        self.action = action
        self.target = target

    def tuple(self):
        if self.action in actions_with_values:
            return (self.action, self.target, self.values.split("|"))
        else:
            return (self.action, self.target)

class SourceStep(object):
    __storm_table__ = "source_step"
    __storm_primary__ = "source_id", "step_id"
    source_id = Int()
    step_id = Int()
    sequence = Int()

    def __storm_pre_flush__(self):
        if self.sequence is None:
            store = Store.of(self)
            steps = [step for step in store.get(Source, self.source_id).steps]
            if len(steps):
                sequence_end = store.get(SourceStep, (self.source_id, steps[-1].id)).sequence
                self.sequence = sequence_end + 1
            else:
                self.sequence = 1

class Source(object):
    __storm_table__ = "source"
    id = Int(primary=True)
    name = Unicode()
    url = Unicode()
    steps = ReferenceSet(id, SourceStep.source_id, SourceStep.step_id, Step.id, SourceStep.sequence)

    def __init__(self, name=u"", url=u"", id=None):
        self.name = name
        self.url = url

    def __repr__(self):
        return u"Source(name=\"{self.name}\", url=\"{self.url}\", id={self.id})".format(self=self)

    def __storm_loaded__(self):
        sequence = 0
        store = Store.of(self)
        for step in self.steps:
            sequence += 1
            store.get(SourceStep, (self.id, step.id)).sequence = sequence
            print sequence

    def instructions(self):
        all_expanded_calls = [expanded_calls(step.tuple()) for step in self.steps]
        sequences = [sequence for sequence in itertools.product(*all_expanded_calls)]
        flat_sequences = []
        for sequence in sequences:
            flat_sequences.extend(sequence)
        return flat_sequences
