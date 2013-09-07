from storm.locals import *

models = []
actions = ["goto", "click", "select", "text", "frame", "dump"]
actions_with_values = ["select", "text"]

def listify(x):
    if not isinstance(x, list):
        x = [x]
    return x

def expanded_calls(step):
    args = step[1:]
    listified_args = [listify(x) for x in args]
    for args_combo in itertools.product(*listified_args):
        yield step[0], args_combo

class Source(object):
    __storm_table__ = "source"
    id = Int(primary=True)
    name = Unicode()
    url = Unicode()

    def __init__(self, name=u"", url=u"", id=None):
        self.name = name
        self.url = url

    def __repr__(self):
        return u"Source(name=\"{self.name}\", url=\"{self.url}\", id={self.id})".format(self=self)
