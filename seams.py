from itertools import chain, zip_longest


def roundrobin(*gens, ignore=None):
    yield from (elt for chunk in zip_longest(*gens, fillvalue=ignore) 
                        for elt in chunk if elt is not ignore)
