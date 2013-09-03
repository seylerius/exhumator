from minimongo import Model, Index, configure

configure(host=u'paulo.mongohq.com', port=10067, username=u"emhs", password=u'dea84638ime', database='Exhumator')

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

class Source(Model):
    class Meta:
        collection="sources"

    def __init__(self, name):
        super(Source, self)
        
        # Can't use self.attr until instantiated
        self.__setitem__("name", name)
        self.__setitem__("company", None)
        self.__setitem__("steps", [])
        self.__setitem__("funeral_homes", [])

#    def add_step(self, action, target, value=None):
#        if action not in actions:
#            raise TypeError("Not a valid action")
#        elif action in actions_with_values:
#            if value is None:
#                raise TypeError("Action \"{action}\" requires a value".format(action=action))
#            elif if not isinstance(value, list):
#                raise TypeError("Values must be expressed as a list")
#        else:

models.append(Source)
