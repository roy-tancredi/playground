from collections.abc import Hashable, Mapping
from operator import concat

from generics import consume


def flatten(sequence, ignore_types=(Hashable,)): # adding 'depth' to consider
    for elt in sequence:
        if isinstance(elt, ignore_types):
            yield elt
        else: 
            yield from flatten(elt, ignore_types)



def path_nested(sequence, ignore_types=(Hashable,)):
    def _path_nested(tree, current_branch=[]):
        iterator = tree.items() if isinstance(tree, Mapping) else enumerate(tree)
        for i, elt in iterator:
            path = concat(current_branch, [i,]) # optimal solution?
            if isinstance(elt, ignore_types):
                yield (tuple(path), elt)
            else:
                yield from _path_nested(elt, path)
    yield from _path_nested(sequence)


def nest_pathed(sequence): # to be cleaned up and generalized for dicts on output also
    tree = []
    def _nest_pathed(seq, node, depth=0):
        subseq, subnode = [], []
        for path, elt in seq:
            # path_match_depth = len(path) == depth+1
            if len(path) == depth+1 and not subseq:
                node.append(elt)
            elif not subseq: 
                subseq.append((path, elt))
                node.append(subnode)
            elif path[depth] == subseq[0][0][depth]:
                subseq.append((path, elt))
            else:
                yield from _nest_pathed(subseq, subnode, depth+1)
                subseq, subnode = [], []
                if len(path) == depth+1:
                    node.append(elt)
                else:
                    subseq.append((path, elt))
                    node.append(subnode)
        if subseq:
            yield from _nest_pathed(subseq, subnode, depth+1)
    consume(_nest_pathed(sequence, tree))
    return tree




