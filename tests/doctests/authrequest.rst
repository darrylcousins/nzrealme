Authentication Request
======================

This class is used by the :class:`nzrealme.serviceprovider.ServiceProvider``
class to generate a SAML2 AuthnRequest message and send it to the NZ RealMe
Login service IdP (Identity Provider) using the HTTP-Redirect binding.

This class is not intended to be used directly and is created with the
``new_request`` method of the :class:`nzrealme.serviceprovider.ServiceProvider`::

    >>> sp = ServiceProvider(os.path.join(test_dir, 'conf'), 'login')
    >>> req= sp.new_request()
    >>> req
    <nzrealme.authrequest.AuthRequest object at 0x...>

The ``LogonStrength`` object::

    >>> req.auth_strength
    <nzrealme.logonstrength.LogonStrength object at 0x...>
    >>> req.auth_strength.urn
    'urn:nzl:govt:ict:stds:authn:deployment:GLS:SAML:2.0:ac:classes:LowStrength'
    >>> req.auth_strength.score
    10
