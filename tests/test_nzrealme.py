# -*- coding: utf-8 -*-
import doctest
import sys
import os


def get_all_available(paths):
    """
    Get the methods and classes from the paths defined. Requires that the module
    has an ``__all__`` attribute to use.
    """
    for path in paths:
        fromlist = path.split('.')
        mod = __import__(path, fromlist=fromlist[:-1])
        for name in mod.__all__:
            yield getattr(mod, name)


# models used in the tests defined here and imported instead of peppering docs
BUILTINS = [
    'os',
    'lxml',
    'urllib',
    'urlparse',
    'base64',
    'pprint',
    ]

# and again for the modules used, NB this depends on ``__all`` being defined in
# module
MODULES = [
    'nzrealme.serviceprovider',
    'nzrealme.authrequest',
    'nzrealme.logonstrength',
    'nzrealme.tokengenerator',
    'nzrealme.identityprovider',
    'nzrealme.encoder',
    'nzrealme.signer',
    ]

def setUp(test):
    test.globs['test_dir'] = os.path.dirname(__file__)
    for klass in get_all_available(MODULES):
        test.globs[klass.__name__] = klass
    # builtins
    for module in BUILTINS:
        try:
            name = module.split('.')[-1]
        except IndexError:
            name = module
        test.globs[name] = sys.modules[module]


def tearDown(test):
    pass


DOCFILES = [
    'doctests/nzrealme.rst',
    'doctests/serviceprovider.rst',
    'doctests/authrequest.rst',
    'doctests/logonstrength.rst',
    'doctests/tokengenerator.rst',
    'doctests/identityprovider.rst',
    ]


DOCTESTS = [
    'nzrealme.encoder',
    'nzrealme.signer',
    ]


def load_tests(loader, tests, ignore):

    list_of_docfiles = DOCFILES
    for p in list_of_docfiles:
        tests.addTest(doctest.DocFileSuite(
            p, setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
        ))

    list_of_doctests = DOCTESTS
    for m in list_of_doctests:
        tests.addTest(doctest.DocTestSuite(
            __import__(m, globals(), locals(), fromlist=["*"]),
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
        ))

    return tests
