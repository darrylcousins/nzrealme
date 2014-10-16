# -*- coding: utf-8 -*-
"""Class representing the NZ RealMe Login SAML IdP"""
import os
from lxml import etree

__all__ = (
    'IdentityProvider',
    )

SOAP_BINDING = 'urn:oasis:names:tc:SAML:2.0:bindings:SOAP';

NSMAP = {
    'md': 'urn:oasis:names:tc:SAML:2.0:metadata',
    'ds': 'http://www.w3.org/2000/09/xmldsig#'
    }

METADATA_CACHE = {}

class IdentityProvider(object):
    """
    This class is used to represent the SAML IdP (Identity Provider) which
    implements the RealMe Login service.  An object of this class is initialised
    from the ``metadata-login-idp.xml`` in the configuration directory.
    """

    def __init__(self, conf_dir, service_type='login'):
        """
        Constructor.  Should not be called directly.  Instead, call the ``get_idp`` method
        on the service provider object.

        The ``conf_dir`` parameter **must** be provided.  It specifies the full pathname
        of the directory containing the IdP metadata file.
        """
        self.conf_dir = conf_dir
        self.service_type = service_type
        self._load_metadata()

    def _load_metadata(self):
        """
        Load metadata from file, save in simple dictionary cache and set as class attributes
        """
        cache_key = self.get_cache_key()
        if METADATA_CACHE.get(cache_key, None):
            params = METADATA_CACHE[cache_key]
        else:
            params = self._read_metadata_from_file()
        self.__dict__.update(params)

    def _read_metadata_from_file(self):
        """
        Gather data from the metadata file.
        """
        metadata = {}
        tree = etree.parse(self._metadata_pathname())

        entity_id = tree.xpath('/md:EntityDescriptor/@entityID', namespaces=NSMAP)[0]
        assert entity_id
        metadata['entity_id'] = entity_id

        single_signon_location = tree.xpath(
            '/md:EntityDescriptor/md:IDPSSODescriptor/md:SingleSignOnService/@Location',
            namespaces=NSMAP)[0]
        assert single_signon_location
        metadata['single_signon_location'] = single_signon_location

        signing_cert_pem_data = tree.xpath(
            '/md:EntityDescriptor/md:IDPSSODescriptor/md:KeyDescriptor[@use="signing"]/ds:KeyInfo/ds:X509Data/ds:X509Certificate',
            namespaces=NSMAP)[0].text
        assert signing_cert_pem_data
        signing_cert_pem_data = "-----BEGIN CERTIFICATE-----\n{0}\n-----END CERTIFICATE-----\n".format(
            signing_cert_pem_data.strip())
        metadata['signing_cert_pem_data'] = signing_cert_pem_data

        resolution_services = []

        for node in tree.xpath(
            '/md:EntityDescriptor/md:IDPSSODescriptor/md:ArtifactResolutionService',
            namespaces=NSMAP):
            index = node.xpath('./@index')[0]
            try:
                assert index
            except AssertionError:
                raise ValueError(
                    'No Index for ArtifactResolutionService: {0}'.format(
                        node.tag))

            location = node.xpath('./@Location')[0]
            try:
                assert location
            except AssertionError:
                raise ValueError(
                    'No Location for ArtifactResolutionService: {0}'.format(
                        node.tag))

            resolution_services.insert(int(index), location)

            binding = node.xpath('./@Binding')[0]
            try:
                assert binding
            except AssertionError:
                raise ValueError(
                    'No Binding for ArtifactResolutionService: {0}'.format(
                        node.tag))
            try:
                assert binding == SOAP_BINDING
            except AssertionError:
                raise ValueError(
                    'No Binding for ArtifactResolutionService: {0}'.format(
                        node.tag))

        metadata['resolution_services'] = resolution_services

        METADATA_CACHE[self.get_cache_key()] = metadata

        return metadata

    def _metadata_pathname(self):
        """Assert the existence of the metadata file"""
        if not self.conf_dir:
            raise ValueError('Configuration directory has not been defined')
        metadata_file = os.path.join(
            self.conf_dir, 'metadata-{0}-idp.xml'.format(self.service_type))
        if not os.path.exists(metadata_file):
            raise ValueError('Metadata file not found: {0}'.format(metadata_file))
        return metadata_file

    def get_cache_key(self):
        """Simple method to create the cache key"""
        return '{0}-{1}'.format(self.conf_dir, self.service_type)

    def entity_id(self):
        """
        Accessor for the ``ID`` parameter in the Identity Provider metadata file.
        """
        pass

    def single_signon_location(self):
        """
        Accessor for the ``SingleSignOnService`` parameter in the Service Provider
        metadata file.
        """
        pass

    def signing_cert_pem_data(self):
        """
        Accessor for the signing certificate (X509 format) text from the metadata file.
        If supplied with a service type, it will return the certificate appropriate to
        that type.
        """
        pass

    def login_cert_pem_data(self):
        """
        Accessor for the signing certificate (X509 format) text from the metadata file
        of the login service.  This is used when resolving the opaque token from the
        identity assertion through the iCMS service.
        """
        pass

    def artifact_resolution_location(self, idx):
        """
        Accessor for the ``ArtifactResolutionService`` parameter in the Service Provider
        metadata file.  When calling this method, you must provide an index number
        (from the artifact).
        """
        pass

    def verify_signature(self, doc):
        """
        Takes an XML document signed by the Identity provider and returns true if the
        signature is valid.
        """
        pass

    def validate_source_id(self, src_id):
        """
        Takes a source ID string from an artifact to be resolved and confirms that it
        was generated by this Identity Provider.  Returns true on successs, dies on
        error.
        """
        pass



