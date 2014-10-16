============
Installation
============

At the command line::

    $ easy_install nzrealme

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv nzrealme
    $ pip install nzrealme

libxml2 and xmldsig
===================

This package uses `xmldsig <https://github.com/AntagonistHQ/xmldsig>`_ to
create the xml signatures, ``xmldsig`` requires ``xmlsec`` and ``libxml2``.

The package also uses ``lxml`` for reading and writing xml documents.

This means that both ``libxml2`` and ``lxml`` are requirements of this package.

``lxml`` and ``xmlsec`` are included in ``requirements.txt`` and are easily
installed with ``pip``. However I've found that ``libxml2`` can be problematic
to install. These notes are made with ``osx`` in mind but hopefully will be
useful for other architectures. Quite likely system packages will answer the
requirements but I use ``virtualenv`` so these notes are made with that in
mind.

As I understand it ``libxml2`` is not available for a ``pip`` install. These
are the steps I followed to install ``libxml2`` into my virtualenv.::

    $ cd myenv
    $ pyenv active myenv
    $ wget ftp://xmlsoft.org/libxml2/libxml2-sources-2.9.1.tar.gz
    $ tar zxvf libxml2-sources-2.9.1.tar.gz
    $ cd libxml2-2.9.1/python

Now you will need to know where your ``libxml2`` include files are and to use
that path to those includes::

    $ CFLAGS=-I/usr/local/Cellar/libxml2/2.9.1/include python setup.py build
    $ CFLAGS=-I/usr/local/Cellar/libxml2/2.9.1/include python setup.py install

That was it! Now I could do ``pip install xmldsig`` without any trouble.



