# -*- coding: utf-8 -*-
"""ServiceProvider: class representing the local SAML2 Service Provider"""
import os

from .authrequest import AuthRequest
from .tokengenerator import TokenGenerator


__all__ = (
    'ServiceProvider',
    )

SERVICE_TYPES = (
    'login',
    'assertion'
    )

class ServiceProvider(object):
    """
    This class is used to represent the local SAML2 SP (Service Provider) which
    will be used to access the NZ RealMe Login service IdP (Identity Provider) or
    the NZ RealMe Assertion service IdP.  In normal use, an object of this class is
    initialised with the file ``metadata-sp.xml`` in the configuration directory.

    conf_dir (str): '/path/to/directory'
        The ``conf_dir`` parameter **must** be provided.  It specifies the full pathname
        of the directory containing SP and IdP metadata files as well as certificate
        and key files for request signing and mutual-SSL.

    service_type (str, 'login'): 'login' or 'assertion'
        Indicate whether you wish to communicate with the ``login`` service or the
        ``assertion`` service (for identity information).
    """
    conf_dir = None
    service_type = None

    def __init__(self, conf_dir, service_type='login'):
        """
        """

        if not os.path.exists(conf_dir):
            raise ValueError(
                'Directory {0} does not exist'.format(conf_dir))
        self.conf_dir = conf_dir

        if service_type not in SERVICE_TYPES:
            raise ValueError(
                'Service type {0} is not a valid type, expected {1}'.format(
                    service_type, ' or '.join(SERVICE_TYPES)))
        self.service_type = service_type

        self.token_generator = TokenGenerator()

    def new_request(self, **kwargs):
        """
        Creates a new :class:`nzrealme.authrequest.AuthRequest` object.  The caller would
        typically use the ``as_url`` method of the request to redirect the client to the
        Identity Provider's single logon service.  The request object's ``request_id``
        method should be used to get the request ID and save it in session state for
        use later during artifact resolution.

        The ``new_request`` method does not **require** any arguments, but accepts the
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
        request = AuthRequest(self, **kwargs)
        return request

    def generate_saml_id(self):
        """
        Used by the request classes to generate a unique identifier for each request.
        It accepts one argument, being a string like 'AuthenRequest' to identify the
        type of request.
        """
        return self.token_generator.saml_id()

