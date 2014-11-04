============
Installation
============

At the command line::

    $ easy_install nzrealme

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv nzrealme
    $ pip install nzrealme

From your ``virtualenv`` root directory clone the repository::

  $ git clone https://bitbucket.org/darrylcousins/nzrealme

Initialize and activate the ``virtualenv``::

  $ pyenv virtualenv 2.7.6 onlymarlborough
  $ cd onlymarlborough
  $ pyenv activate onlymarlborough

Pip install the requirements for development::

  $ pip install -r requirements.txt

Run tests::

  $ make test

Check pep8 with flake8::

  $ make lint

Check coverage::

  $ make coverage

Potential problems
==================

Installation of xml bindings ``lxml`` and ``dm.xmsec.binding`` `https://github.com/onelogin/python-saml/issues/30`.

