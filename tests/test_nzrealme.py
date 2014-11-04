# -*- coding: utf-8 -*-
import doctest
import sys
import os
import json
from base64 import b64decode
from zlib import decompress


def get_all_available(paths):
    """
    Get the methods and classes from the paths defined. Requires that the
    module has an ``__all__`` attribute to use.
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
    're',
    ]

# and again for the modules used, NB this depends on ``__all`` being defined in
# module
MODULES = [
    'nzrealme.authn_request',
    'nzrealme.utils',
    ]


def loadSettings(f='settings1.json'):
    filename = os.path.join(os.path.dirname(__file__), 'saml', f)
    if os.path.exists(filename):
        stream = open(filename, 'r')
        settings = json.load(stream)
        stream.close()
        return settings
    else:
        raise Exception('Settings json file does not exist')


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

    from onelogin.saml2.settings import OneLogin_Saml2_Settings
    from onelogin.saml2.utils import OneLogin_Saml2_Utils
    test.globs['OneLogin_Saml2_Settings'] = OneLogin_Saml2_Settings
    test.globs['OneLogin_Saml2_Utils'] = OneLogin_Saml2_Utils
    test.globs['loadSettings'] = loadSettings
    test.globs['b64decode'] = b64decode
    test.globs['decompress'] = decompress


def tearDown(test):
    pass


DOCFILES = [
    'doctests/authn_request.rst',
    ]


DOCTESTS = [
    'nzrealme.settings',
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
