from functools import partial
import re


def lines_from(path, mode='rb'):
    with open(path, mode) as fh:
        yield from fh

def chuncks_from(path, buffsize=8192, mode='rb'):
    with open(path, mode, buffsize) as fh:
        yield from iter(partial(fh.read, buffsize), b'')

def records_from(path, sep=b'\n'):
    rest = ''
    for chunk in chuncks_from(path):
        fields = re.split(sep, b''.join((chunk, rest)))
        rest = fields.pop()
        yield from fields
    yield rest

def trunc_comments():
    ...


