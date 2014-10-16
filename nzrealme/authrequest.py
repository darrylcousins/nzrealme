# -*- coding: utf-8 -*-
"""Generate a SAML2 Authentication Request message"""
from lxml import etree

from .logonstrength import LogonStrength

__all__ = (
    'AuthRequest',
    )

NSMAP = {
    'saml': 'urn:oasis:names:tc:SAML:2.0:assertion',
    'samlp': 'urn:oasis:names:tc:SAML:2.0:protocol',
    }

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

        self.xml = self._generate_auth_request_doc(service_provider)
        # self.query_string = sign_query_string(self._raw_query_string)

    def _generate_auth_request_doc(self, sp):
        """
        Generate the authentication xml request document.

        sp (object): ServiceProvider instance

        my $x = XML::Generator->new(#':pretty',
            namespace => [ @$ns_saml, @$ns_samlp ],
        );
        $self->{x} = $x;

        $self->{saml_request} = $x->AuthnRequest($ns_samlp,
            {
                Version                       => '2.0',
                ID                            => $self->request_id(),
                IssueInstant                  => $self->request_time(),
                Destination                   => $self->destination_url(),
                $self->service_type eq 'login'
                    ? (ForceAuthn             => $self->force_auth() )
                    : (),
                AssertionConsumerServiceIndex => '0',
            },
            $self->_issuer(),
            $self->_nameid_policy(),
            $self->service_type eq 'login'
                ? $self->_authen_context()
                : (),
        ) . '';  # ensure result is stringified

xml_found_node_ok($xml, q{/nssamlp:AuthnRequest});
xml_node_content_is($xml, q{/nssamlp:AuthnRequest/@Version} => '2.0');
xml_node_content_is($xml, q{/nssamlp:AuthnRequest/@AssertionConsumerServiceIndex} => '0');
xml_node_content_is($xml, q{/nssamlp:AuthnRequest/@ForceAuthn} => 'true');
xml_node_content_is($xml, q{/nssamlp:AuthnRequest/@ID} => $req_id);
xml_node_content_is($xml, q{/nssamlp:AuthnRequest/@IssueInstant} => $req->request_time);
xml_node_content_is($xml, q{/nssamlp:AuthnRequest/@Destination} => $sp->idp->single_signon_location);
xml_node_content_is($xml, q{/nssamlp:AuthnRequest/nssaml:Issuer} => $sp->entity_id);
xml_node_content_is($xml, q{/nssamlp:AuthnRequest/nssamlp:NameIDPolicy/@AllowCreate} => 'false');
xml_node_content_is($xml, q{/nssamlp:AuthnRequest/nssamlp:NameIDPolicy/@Format}
    => 'urn:oasis:names:tc:SAML:2.0:nameid-format:persistent');
xml_node_content_is($xml, q{/nssamlp:AuthnRequest/nssamlp:RequestedAuthnContext/nssaml:AuthnContextClassRef}
    => 'urn:nzl:govt:ict:stds:authn:deployment:GLS:SAML:2.0:ac:classes:LowStrength');
        """

        xml = etree.Element(
                'AuthnRequest',
                nsmap={None: NSMAP['samlp'], 'saml': NSMAP['saml']})
        xml.set('Version', '2.0')
        xml.set('ID', sp.generate_saml_id())
        xml.set('IssueInstant', sp.now_as_iso())
        xml.set('Destination', sp.identity_provider.single_signon_location)
        xml.set('AssertionConsumerServiceIndex', '0')

        nidp = etree.SubElement(xml, 'NameIDPolicy')
        nidp.set('Format', sp.nameid_format())

        if sp.service_type == 'login':
            xml.set('ForceAuthn', 'true' if self.force_auth else 'false')
            nidp.set('AllowCreate', 'true' if self.allow_create else 'false')

            rac = etree.SubElement(xml, 'RequestedAuthnContext')
            accr = etree.SubElement(rac,
                '{{{0}}}AuthnContextClassRef'.format(NSMAP['saml']),
                nsmap={'saml': NSMAP['saml']})
            accr.text = self.auth_strength.urn

        iss = etree.SubElement(xml,
            '{{{0}}}Issuer'.format(NSMAP['saml']),
            nsmap={'saml': NSMAP['saml']})
        iss.text = sp.identity_provider.entity_id

        return xml

