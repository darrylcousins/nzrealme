# -*- coding: utf-8 -*-
"""
Digital signature generation/verification

Query String Signing
--------------------

Get key and cert::

    >>> key = open(os.path.join(test_dir, 'conf', 'sp-sign-key.pem')).read()
    >>> cert = open(os.path.join(test_dir, 'conf', 'sp-sign-crt.pem')).read()

Create the query string::

    >>> init_qs = {'Data': 'anything will do',
    ...     'SigAlg': 'http://www.w3.org/2000/09/xmldsig#rsa-sha1'}
    >>> init_qs = urllib.urlencode(init_qs)
    >>> signature = sign_binary(init_qs, key)
    >>> len(signature)
    344
    >>> q = {'Signature':  signature}
    >>> qs = '{0}&{1}'.format(init_qs, urllib.urlencode(q))

Verify the query string::

    >>> data = urlparse.parse_qs(qs)
    >>> signature = data.pop('Signature')[0]

    >>> verify_binary(init_qs, base64.b64decode(signature), cert)
    True

Expecting failure::

    >>> verify_binary('this should fail', base64.b64decode(signature), cert)
    False

"""
import base64

import dm.xmlsec.binding as xmlsec


__all__ = (
    'sign_binary',
    'verify_binary',
    )


def sign_binary(string, key):
    """
    Sign a string and return it

    :param string: The string to sign
    :type string: string

    :param key: The private key
    :type key: string

    """
    xmlsec.initialize()

    dsig_ctx = xmlsec.DSigCtx()
    dsig_ctx.signKey = xmlsec.Key.loadMemory(key, xmlsec.KeyDataFormatPem, None)

    signature = dsig_ctx.signBinary(string, xmlsec.TransformRsaSha1)
    return base64.b64encode(signature)

def verify_binary(string, signature, cert):
    """
    Validates a signed query string

    :param string: The string to validate
    :type string:

    :param signature: The signature
    :type string:

    :param cert: The pubic cert
    :type string:
    """
    xmlsec.initialize()

    dsig_ctx = xmlsec.DSigCtx()
    dsig_ctx.signKey = xmlsec.Key.loadMemory(cert, xmlsec.KeyDataFormatCertPem, None)

    try:
        dsig_ctx.verifyBinary(string, xmlsec.TransformRsaSha1, signature)
    except xmlsec.VerificationError:
        return False

    return True

