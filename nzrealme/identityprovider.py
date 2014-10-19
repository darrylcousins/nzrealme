# -*- coding: utf-8 -*-
"""Class representing the NZ RealMe Login SAML IdP"""
import os
from lxml import etree

__all__ = (
    'IdentityProvider',
    )

SOAP_BINDING = 'urn:oasis:names:tc:SAML:2.0:bindings:SOAP'

NSMAP = {
    'md': 'urn:oasis:names:tc:SAML:2.0:metadata',
    'ds': 'http://www.w3.org/2000/09/xmldsig#'
    }

METADATA_CACHE = {}


class IdentityProvider(object):
    """
    This class is used to represent the SAML IdP (Identity Provider) which
    implements the RealMe Login service.  An object of this class is
    initialised from the ``metadata-login-idp.xml`` in the configuration
    directory.

    Attributes:
        conf_dir (path): the path to key and certificate files.
        service_type (string): the service type 'login' or 'assert'
    """

    def __init__(self, conf_dir, service_type='login'):
        """
        Constructor.  Should not be called directly.  Instead, call the
        ``get_idp`` method on the service provider object. Loads metadata on
        init.

        Args:
            conf_dir (path): the path to key and certificate files.
            service_type (string): the service type 'login' or 'assert'.
                Defaults to 'login'

        The ``conf_dir`` parameter **must** be provided.  It specifies the full
        pathname of the directory containing the IdP metadata file.
        """
        self.conf_dir = conf_dir
        self.service_type = service_type
        self.load_metadata()

    def load_metadata(self):
        """
        Load metadata from file, save in simple dictionary cache and set as
        class attributes
        """
        cache_key = self.get_cache_key()
        if METADATA_CACHE.get(cache_key, None):
            params = METADATA_CACHE[cache_key]
        else:
            params = self.read_metadata_from_file()
        self.__dict__.update(params)

    def read_metadata_from_file(self):
        """
        Gather data from the metadata file.

        Returns:
            params (dict): Dictionary of read values:
                * entity_id (string):
                    The ``ID`` parameter in the Identity Provider metadata
                    file.
                * single_signon_location (url):
                    The ``SingleSignOnService`` parameter in the Service
                    Provider metadata file.
                * signing_cert_pem_data (string)
                    The signing certificate (X509 format) text from the
                    metadata file.  If supplied with a service type, it will
                    return the certificate appropriate to that type.
                * resolution_services (list):
                    The ``ArtifactResolutionService`` parameter in the Service
                    Provider metadata file, indexed by the indexes in the
                    metadata file.

        """
        metadata = {}
        tree = etree.parse(self.metadata_pathname())

        entity_id = tree.xpath(
            '/md:EntityDescriptor/@entityID',
            namespaces=NSMAP)[0]
        assert entity_id
        metadata['entity_id'] = entity_id

        single_signon_location = tree.xpath(
            '/md:EntityDescriptor/md:IDPSSODescriptor/md:SingleSignOnService/@Location',  # nopep8
            namespaces=NSMAP)[0]
        assert single_signon_location
        metadata['single_signon_location'] = single_signon_location

        signing_cert_pem_data = tree.xpath(
            '/md:EntityDescriptor/md:IDPSSODescriptor/md:KeyDescriptor[@use="signing"]/ds:KeyInfo/ds:X509Data/ds:X509Certificate',  # nopep8
            namespaces=NSMAP)[0].text
        assert signing_cert_pem_data
        signing_cert_pem_data = "-----BEGIN CERTIFICATE-----\n{0}\n-----END CERTIFICATE-----\n".format(  # nopep8
            signing_cert_pem_data.strip())
        metadata['signing_cert_pem_data'] = signing_cert_pem_data

        resolution_services = []

        for node in tree.xpath(
            '/md:EntityDescriptor/md:IDPSSODescriptor/md:ArtifactResolutionService',  # nopep8
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

    def metadata_pathname(self):
        """Assert the existence of the metadata file"""
        if not self.conf_dir:
            raise ValueError('Configuration directory has not been defined')
        metadata_file = os.path.join(
            self.conf_dir, 'metadata-{0}-idp.xml'.format(self.service_type))
        if not os.path.exists(metadata_file):
            raise ValueError(
                'Metadata file not found: {0}'.format(metadata_file))
        return metadata_file

    def get_cache_key(self):
        """Simple method to create the cache key

        Returns:
            cache_key (string)
        """
        return '{0}-{1}'.format(self.conf_dir, self.service_type)

    def get_signing_cert_pem_data(self, service_type='login'):
        """
        The signing certificate (X509 format) text from the metadata file. If
        supplied with a service type, it will return the certificate
        appropriate to that type.

        Args:
            service_type (string): 'login' or 'assert', default to 'login'

        Returns:
            String: The signing pem data.
        """
        pass

    def get_login_cert_pem_data(self):
        """
        The signing certificate (X509 format) text from the metadata file of
        the login service.  This is used when resolving the opaque token from
        the identity assertion through the iCMS service.

        Returns:
            String: The signing pem data.
        """
        pass

    def artifact_resolution_location(self, idx):
        """
        Accessor for the ``ArtifactResolutionService`` parameter in the Service
        Provider metadata file.  When calling this method, you must provide an
        index number (from the artifact).

        Args:
            idx (int): the index for looking up the artifact from list

        Returns:
            String:
        """
        pass

    def verify_signature(self, doc):
        """
        Takes an XML document signed by the Identity provider and returns true
        if the signature is valid.

        Args:
            doc (xml): the xml document from idp.

        Returns:
            Bool:
        """
        pass

    def validate_source_id(self, src_id):
        """
        Takes a source ID string from an artifact to be resolved and confirms
        that it was generated by this Identity Provider.  Returns true on
        successs, dies on error.

        Args:
            src_id (str): the identifying id.

        Returns:
            Bool: True, otherwise will raise.
        """
        pass
