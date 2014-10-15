# -*- coding: utf-8 -*-
"""Generate a SAML2 Authentication Request message"""

from .logonstrength import LogonStrength

__all__ = (
    'AuthRequest',
    )

class AuthRequest(object):
    """
    This class is used by the
    :class:`nzrealme.serviceprovider.ServiceProvider`` class to generate a
    SAML2 AuthnRequest message and send it to the NZ RealMe Login service IdP
    (Identity Provider) using the HTTP-Redirect binding.

    This class is not intended to be used directly and is created with the
    ``new_request`` method of the
    :class:`nzrealme.serviceprovider.ServiceProvider`

    The constructor does not **require** any arguments, but accepts the
    following optional keyword arguments:

    allow_create (bool): False
        Controls whether the user should be allowed to create a new account on the
        "login" service IdP.  Not used when talking to the "assertion service".

    force_auth (bool): True
        Controls whether the user will be forced to log in, rather than allowing the
        reuse of an existing logon session on the IdP.  Not useful, as the login
        service ignores this option anyway.

    auth_strength (str): 'low'
        The logon strength required.  May be supplied as a URN, or as keyword ('low',
        'mod', 'sms', etc).  See :class:`nzrealme.logonstrenght.LogonStrength` for constants.

    relay_state (str): ''
        User-supplied string value that will be returned as a URL parameter to the
        assertion consumer service.

    """
    service_provider = None
    auth_strength = None
    allow_create = False
    force_auth = True
    relay_state = ''

    def __init__(self, service_provider, **kwargs):
        self.allow_create = kwargs.get('allow_create', False)
        self.force_auth = kwargs.get('force_auth', True)
        self.relay_state = kwargs.get('relay_state', '')
        auth_strength = kwargs.get('auth_strength', 'low')
        self.auth_strength = LogonStrength(auth_strength)

        self.service_provider = service_provider
        self.request_id = service_provider.generate_saml_id()

        # self.destination_url = idp.single_signon_location()  # XXX
        # self.request_time = now_as_iso()  # XXX
        # self.nameid_format = nameid_format()  # XXX
        # self.xml = self.generate_auth_request_doc()
        # self.query_string = sign_query_string(self._raw_query_string)

