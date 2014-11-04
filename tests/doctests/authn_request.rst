======================
NZRealMe Authn Request
======================

The default :class:`onelogin.saml2.authn_request.OneLogin_Saml2_Authn_Request`
object uses an xml template not quite what is required for NZRealMe_.

So it has been subclassed for use in this package.

Create Request
==============

Load the json setting file and create the ``authn_request`` object::

    >>> saml_settings = loadSettings()
    >>> settings = OneLogin_Saml2_Settings(saml_settings)
    >>> authn_request = NZRealMe_Authn_Request(settings)

Check Encoded Request
---------------------

The ``authn_request`` returned is encoded::

    >>> authn_request_encoded = authn_request.get_request()
    >>> decoded = b64decode(authn_request_encoded)
    >>> inflated = decompress(decoded, -15)
    >>> print(inflated)
    <samlp:AuthnRequest
      xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
      ID="NZREALME_..."
      Version="2.0"
      ProviderName="SP test"
      IssueInstant="20...T...Z"
      Destination="http://idp.example.com/SSOService.php"
      ProtocolBinding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
      AssertionConsumerServiceURL="http://stuff.com/endpoints/endpoints/acs.php"
      ForceAuthn="true">
      <saml:Issuer>http://stuff.com/endpoints/metadata.php</saml:Issuer>
      <samlp:NameIDPolicy
        Format="urn:oasis:names:tc:SAML:2.0:nameid-format:persistent"
        AllowCreate="false" />
      <samlp:RequestedAuthnContext Comparison="exact">
        <saml:AuthnContextClassRef>urn:nzl:govt:ict:stds:authn:deployment:GLS:SAML:2.0:ac:classes:LowStrength</saml:AuthnContextClassRef>
      </samlp:RequestedAuthnContext>
    </samlp:AuthnRequest>

The Encoded Query String
------------------------

The query string of the url is encoded::

    >>> parameters = {
    ...     'SAMLRequest': authn_request.get_request()
    ... }
    >>> auth_url = NZRealMe_Utils.redirect(
    ...     'http://idp.example.com/SSOService.php',
    ...     parameters=parameters,
    ...     request_data={})
    >>> exploded = urlparse.urlparse(auth_url)
    >>> exploded = urlparse.parse_qs(exploded[4])
    >>> 'SAMLRequest' in exploded
    True
    >>> payload = exploded['SAMLRequest'][0]
    >>> decoded = b64decode(payload)
    >>> inflated = decompress(decoded, -15)
    >>> print(inflated)
    <samlp:AuthnRequest
      xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
      ID="NZREALME_..."
    ...
    </samlp:AuthnRequest>

Same result as for above.

.. _NZRealMe: https://www.realme.govt.nz/
