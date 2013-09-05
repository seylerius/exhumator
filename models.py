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

