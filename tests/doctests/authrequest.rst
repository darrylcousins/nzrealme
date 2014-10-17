Authentication Request
======================

This class is used by the :class:`nzrealme.serviceprovider.ServiceProvider``
class to generate a SAML2 AuthnRequest message and send it to the NZ RealMe
Login service IdP (Identity Provider) using the HTTP-Redirect binding.

This class is not intended to be used directly and is created with the
``new_request`` method of the :class:`nzrealme.serviceprovider.ServiceProvider`::

    >>> sp = ServiceProvider(os.path.join(test_dir, 'conf'), 'login')


Create the request
------------------

::

    >>> request = sp.new_request()
    >>> request
    <nzrealme.authrequest.AuthRequest object at 0x...>

Verify attributes of the request
--------------------------------

The ``LogonStrength`` object::

    >>> request.auth_strength
    <nzrealme.logonstrength.LogonStrength object at 0x...>
    >>> request.auth_strength.urn
    'urn:nzl:govt:ict:stds:authn:deployment:GLS:SAML:2.0:ac:classes:LowStrength'
    >>> request.auth_strength.score
    10

The xml authentication request::

    >>> print(request.saml_request)
    <AuthnRequest 
        xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
        xmlns="urn:oasis:names:tc:SAML:2.0:protocol"
        Version="2.0"
        ID="..."
        IssueInstant="20...T...Z"
        Destination="https://test.fakeme.govt.nz/logon-test/testEntryPoint"
        AssertionConsumerServiceIndex="0"
        ForceAuthn="true">
      <NameIDPolicy Format="urn:oasis:names:tc:SAML:2.0:nameid-format:persistent" AllowCreate="false"/>
      <RequestedAuthnContext>
        <saml:AuthnContextClassRef>urn:nzl:govt:ict:stds:authn:deployment:GLS:SAML:2.0:ac:classes:LowStrength</saml:AuthnContextClassRef>
      </RequestedAuthnContext>
      <saml:Issuer>https://test.fakeme.govt.nz/saml2</saml:Issuer>
    </AuthnRequest>

The ecoded saml request::

    >>> saml_len = len(request.encoded_saml_request)
    >>> saml_len > 500
    True

The raw query string::

    >>> data = urlparse.parse_qs(request.raw_query_string)
    >>> pprint.pprint(data)
    {'SAMLRequest': ['...']}
    >>> len(data['SAMLRequest'][0]) == saml_len
    True

The full, signed query string::

    >>> data = urlparse.parse_qs(request.signed_query_string)
    >>> pprint.pprint(data)
    {'SAMLRequest': ['...'],
     'SigAlg': ['http://www.w3.org/2000/09/xmldsig#rsa-sha1'],
     'Signature': ['...']}
    >>> len(data['SAMLRequest'][0]) == saml_len
    True

The url to be sent to::

    >>> request.url
    'https://test.fakeme.govt.nz/logon-test/testEntryPoint?SAMLRequest=...'

Verify the query string
-----------------------

Check the query can be verified using :class:`nzrealme.signature.verify_binary`. First construct the original string that was used::

    >>> q = {'SigAlg': 'http://www.w3.org/2000/09/xmldsig#rsa-sha1'}
    >>> init_qs = '{0}&{1}'.format(request.raw_query_string, urllib.urlencode(q))

Get the signature used::

    >>> signature = data.pop('Signature')[0]

Get the public certificate from test configuration directory::

    >>> cert = open(os.path.join(test_dir, 'conf', 'sp-sign-crt.pem')).read()

And verify the signed query string::

    >>> verify_binary(init_qs, base64.b64decode(signature), cert)
    True
