from storm.locals import *
import re

models = []
actions = [u"goto", u"click", u"select", u"text", u"frame", u"dump"]
actions_with_values = [u"select", u"text"]
url_regex = re.compile(r"^(http(?:s)?\:\/\/[a-zA-Z0-9\-]+(?:\.[a-zA-Z0-9\-]+)*\.[a-zA-Z]{2,6}(?:\/?|(?:\/[\w\-]+)*)(?:\/?|\/\w+\.[a-zA-Z]{2,4}(?:\?[\w]+\=[\w\-]+)?)?(?:\&[\w]+\=[\w\-]+)*)$")

def listify(x):
    if not isinstance(x, list):
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
        global actions
        global actions_with_values
        global url_regex

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
        global actions_with_values
        if self.action in actions_with_values:
            return (self.action, self.target, self.values.split("|"))
        else:
            return (self.action, self.target)

class SourceStep(object):
    __storm_table__ = "source_step"
    source_id = Int(primary=True)
    step_id = Int(primary=True)
    sequence = Int()

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
