from functools import reduce, singledispatch
from collections.abc import Hashable, Sequence, Generator


def coroutine(obj):
    """Ensure start of generator."""
    # if isinstance(obj, Generator): # needs more general solution
    #     return obj
    def _start(*args, **kwds):
        cr = obj(*args, **kwds)
        cr.send(None)
        return cr
    return _start

def send_to(target, break_on=None):
    def source(src):
        def captured(*args, **kwds):
            for elt in iter(src(*args,**kwds), break_on):
                target.send(elt)
        return captured
    return source

def start_gen(gen):
    g = gen()
    next(g)
    return g


def pipethrough(elt, gens): # has to handle piplines also
    """Send 'elt' through given generators."""
    # gens = list(map(start_gen, gens)) # have to encapsulate coroutine ensurement
    return reduce(lambda elt, gen: gen.send(elt), gens, elt)

def consume(gen):
    for _ in gen: pass
    return None


# there is need to implement some 'compose' that could handle 
# wrapped functions/gen expressions as partials and also 
# coprocedures
@singledispatch # *gens or gens? how to handle both?
def compose(*gens):
    """Create pipeline from sequence of generators."""
    # gens = list(map(coroutine, gens))
    def _composition(src):
        yield from map(lambda elt: pipethrough(elt, gens), src)
    return _composition
        # this functional implementation is a little bit slower than...
        # for elt in src:
        #     for gen in gens:
        #         elt = gen().send(elt)
        #     yield elt

@compose.register
def starcompose(gens: Sequence):
    yield from compose(*gens)


# some kind of branching/teeing
# yield from (gen().send(elt) for elt in src for gen in gens)


