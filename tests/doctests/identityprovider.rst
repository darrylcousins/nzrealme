Identity Provider
=================

This class is used to represent the SAML IdP (Identity Provider) which
implements the RealMe Login service.  An object of this class is initialised
from the ``metadata-login-idp.xml`` in the configuration directory.

This class is not intended to be used directly and is created with the
``init`` method of the :class:`nzrealme.serviceprovider.ServiceProvider`::

    >>> sp = ServiceProvider(os.path.join(test_dir, 'conf'), 'login')
    >>> idp = sp.identity_provider
    >>> idp
    <nzrealme.identityprovider.IdentityProvider object at 0x...>

On creation the IdentityProvider loads metadata from the file::

    >>> idp._metadata_pathname()
    '/.../nzrealme/nzrealme/tests/conf/metadata-login-idp.xml'

And the important tokens are stored in class attributes::

    >>> idp.resolution_services
    ['https://as.test.fakeme.govt.nz/sso/ArtifactResolver/metaAlias/logon/logonidp']

    >>> idp.entity_id
    'https://test.fakeme.govt.nz/saml2'

The destination url::

    >>> idp.single_signon_location
    'https://test.fakeme.govt.nz/logon-test/testEntryPoint'

    >>> print(idp.signing_cert_pem_data)
    -----BEGIN CERTIFICATE-----
    MIIDLzCCAhegAwIBAgIJAJys5okjA3N3MA0GCSqGSIb3DQEBBQUAMC4xLDAqBgNV
    BAMMI3Rlc3Quc2lnbmluZy5hY2NvdW50LmZha2VtZS5nb3Z0Lm56MB4XDTE0MDUz
    MDAwNTkwMFoXDTE0MDYyOTAwNTkwMFowLjEsMCoGA1UEAwwjdGVzdC5zaWduaW5n
    LmFjY291bnQuZmFrZW1lLmdvdnQubnowggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAw
    ggEKAoIBAQDNQWtXKquqhfJt/X8C8Gyg9+2LrhcCvQdyXnTVAITItV1kTk+l2tze
    QNo7yU0Z9i692Gn+UBobPoRwmHgCXu6ZyKxH1qOBqwnqyhhezYSQNm8ReBaSPlP1
    yYswDvY+/N9MBAcZvCt8BSNz4Tsv+gP7WrHOx5U0zrSkVcEGhaCcLFsdo3R2SMFP
    xvVpRmIqRPKzyANZqyoMtoRnIhxyuppaO1fSKvy1TG0SK7dLDVWIn2NPMZMpvZsG
    9JorBAeit5nO/eE8GSxe/i8lvjIuZS/Rc57+71RmeemFz+MbIGZ4tU+YqY0SupXz
    24E0dIsMzSl3rXEU/VD9L4etaxz0pz4ZAgMBAAGjUDBOMB0GA1UdDgQWBBQfsK+Y
    Bi2/Vk+Fvyc22UEvhx1QQTAfBgNVHSMEGDAWgBQfsK+YBi2/Vk+Fvyc22UEvhx1Q
    QTAMBgNVHRMEBTADAQH/MA0GCSqGSIb3DQEBBQUAA4IBAQBXgE/zv3lWxf7e3nGc
    Xpl6JBPv2cB7nwDjeoDxRwx2oThuRoFLtrFmjonrUZIMUWapUBGA+/WjMlq9GuB2
    a1UUx4izOPX9QDHzPTewuDO4tiyI+vTXrXno+8CW7wOi9OwOVaiY8X677nPhJUIP
    LBcBdweYxC7nLdhNLKEXMyRXlg/mD5ACDQAAiUbs/yx3Br4K3YQyM7oZOCAfJR4+
    whCR4OTRYNM1bH7LQNM88N6EPyRnkP3mJpu0HH2wNFOc1hfF2hq9Icwu3VhsQLnm
    nv8TV6OwdEoqMNCPozBegc27rf6AixerOnOJk1hMVLq4GM3Dy0O1qPC3tniFbzUv
    gCNF
    -----END CERTIFICATE-----
