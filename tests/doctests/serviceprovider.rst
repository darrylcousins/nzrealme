Service Provider
================


The ``ServiceProvider`` is used to represent the local SAML2 SP (Service Provider) which
will be used to access the NZ RealMe Login service IdP (Identity Provider) or
the NZ RealMe Assertion service IdP.  In normal use, an object of this class is
initialised with the file ``metadata-sp.xml`` in the configuration directory.

The constructor must be passed a configuration directory::

    >>> sp = ServiceProvider('/path/to/confdir')
    Traceback (most recent call last):
    ...
    ValueError: Directory /path/to/confdir does not exist

The ``service_type`` must be valid::

    >>> sp = ServiceProvider(os.path.join(test_dir, 'conf'), 'wrong')
    Traceback (most recent call last):
    ...
    ValueError: Service type wrong is not a valid type, expected login or assertion

Initialize the Service Provider
-------------------------------

::

    >>> sp = ServiceProvider(os.path.join(test_dir, 'conf'), 'login')

    >>> len(sp.generate_saml_id())
    40

The time of our request in iso format::

    >>> sp.now_as_iso()
    '20...-...-...T...:...:...Z'

    >>> sp.nameid_format()
    'urn:oasis:names:tc:SAML:2.0:nameid-format:persistent'

Valid until date comes from 'sp-sign-crt.pem' as an iso formated utc date time::

    >>> sp.valid_until_datetime()
    '2014-08-15T06:22:16Z'
