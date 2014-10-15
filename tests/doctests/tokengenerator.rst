Token Generator
===============

This class is responsible for generating random ID tokens such as::

    rdgxl31xjc55f7tl94hes5q0w52bnmw9z9h593qt

The preferred way to use this class
is via the ServiceProvider::

    service_provider.generate_saml_id()

Get a token::

    >>> tg = TokenGenerator()
    >>> len(tg.saml_id())
    40
