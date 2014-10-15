Logon Strength
==============

The NZ RealMe Login service supports the notion of logon strength.  For example
a user session authenticated with a username and password is a 'low strength'
logon.  Whereas authenticating with a user, password and SecurID token will
result in a moderate strength logon.  The different logon strengths are
represented by URNs which will be present in the initial SAML AuthnRequest
message as well as the assertion in the resulting ArtifactResponse.

This class is used to encapsulate the URNs and to provide methods for comparing
the strength of one URN to another.

The string passed must be valid::

    >>> ls = LogonStrength('none')
    Traceback (most recent call last):
    ...
    ValueError: none is not a valid stength expecting moderate or low or mod

    >>> ls = LogonStrength('low')
    >>> ls.urn
    'urn:nzl:govt:ict:stds:authn:deployment:GLS:SAML:2.0:ac:classes:LowStrength'
    >>> ls.score
    10

    >>> ls = LogonStrength('moderate')
    >>> ls.urn
    'urn:nzl:govt:ict:stds:authn:deployment:GLS:SAML:2.0:ac:classes:ModStrength'
    >>> ls.score
    20
