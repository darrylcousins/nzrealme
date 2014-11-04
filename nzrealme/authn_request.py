# -*- coding: utf-8 -*-
"""
NZRealMe_Authn_Request class

A subclass of OneLogin_Saml2_Authn_Request
"""

from base64 import b64encode
from zlib import compress

from onelogin.saml2.authn_request import OneLogin_Saml2_Authn_Request
from onelogin.saml2.constants import OneLogin_Saml2_Constants

from nzrealme.utils import NZRealMe_Utils


__all__ = (
    'NZRealMe_Authn_Request',
    )


class NZRealMe_Authn_Request(OneLogin_Saml2_Authn_Request):
    """
    A subclass of :class:`onelogin.saml2.OneLogin_Saml2_Authn_Request`.

    This class handles an AuthNRequest. It builds an
    AuthNRequest object.

    """

    def __init__(self, settings):
        """
        Constructs the AuthnRequest object.

        Args:
            settings (OneLogin_Saml2_Settings): Setting data

        Returns:
            xml: Request string

        """
        self.__settings = settings

        sp_data = self.__settings.get_sp_data()
        idp_data = self.__settings.get_idp_data()
        security = self.__settings.get_security_data()

        uid = NZRealMe_Utils.generate_unique_id()
        self.__id = uid
        issue_instant = NZRealMe_Utils.parse_time_to_SAML(NZRealMe_Utils.now())

        destination = idp_data['singleSignOnService']['url']

        name_id_policy_format = sp_data['NameIDFormat']
        if 'wantNameIdEncrypted' in security and \
                security['wantNameIdEncrypted']:
            name_id_policy_format = OneLogin_Saml2_Constants.NAMEID_ENCRYPTED

        provider_name_str = ''
        organization_data = settings.get_organization()
        if isinstance(organization_data, dict) and organization_data:
            langs = organization_data.keys()
            if 'en-US' in langs:
                lang = 'en-US'
            else:
                lang = langs[0]
            if 'displayname' in organization_data[lang] and \
                    organization_data[lang]['displayname'] is not None:
                provider_name_str = 'ProviderName="{0}"'.format(
                    organization_data[lang]['displayname'])

        request = """<samlp:AuthnRequest
    xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
    xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
    ID="%(id)s"
    Version="2.0"
    %(provider_name)s
    IssueInstant="%(issue_instant)s"
    Destination="%(destination)s"
    ProtocolBinding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
    AssertionConsumerServiceURL="%(assertion_url)s"
    ForceAuthn="true">
    <saml:Issuer>%(entity_id)s</saml:Issuer>
    <samlp:NameIDPolicy
        Format="%(name_id_policy)s"
        AllowCreate="false" />
    <samlp:RequestedAuthnContext Comparison="exact">
        <saml:AuthnContextClassRef>%(authn_context_class)s</saml:AuthnContextClassRef>
    </samlp:RequestedAuthnContext>
</samlp:AuthnRequest>""" % \
            {
                'id': uid,
                'provider_name': provider_name_str,
                'issue_instant': issue_instant,
                'destination': destination,
                'assertion_url': sp_data['assertionConsumerService']['url'],
                'authn_context_class': sp_data['AuthnContextClass'],
                'entity_id': sp_data['entityId'],
                'name_id_policy': name_id_policy_format,
            }

        self.__authn_request = request

    def get_request(self):
        """
        Returns unsigned AuthnRequest.
        :return: Unsigned AuthnRequest
        :rtype: str object
        """
        deflated_request = compress(self.__authn_request)[2:-4]
        return b64encode(deflated_request)

    def get_id(self):
        """
        Returns the AuthNRequest ID.
        :return: AuthNRequest ID
        :rtype: string
        """
        return self.__id
