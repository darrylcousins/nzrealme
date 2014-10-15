=============
Configuration
=============

This package is configuration-driven - when making an API call, you specify the
path to the config directory and the module picks up everything it needs to
talk to the RealMe login service IdP (Identity Provider) from metadata files
and certificate/key-pair files used for signing/encryption.

Config Files Overview
=====================

The files in the config directory use the following naming convention so you
just need to point the module at the right directory.  The filenames are:


metadata-login-sp.xml
---------------------

This file contains config parameters for the 'Service Provider' - your end of
the authentication dialog - which will talk to the login service.  Once you
have generated the SP metadata file (see: L</Generating Config Files>) you will
need to provide it to the RealMe logon service to install at their end.  You
will need to generate separate metadata files for each of your development,
staging and production environments.

metadata-login-idp.xml
----------------------

The login service IdP or Identity Provider metadata file will be provided to
you by RealMe/DIA.  You will simply need to copy it to the config directory and
give it the correct name.

metadata-assertion-sp.xml
-------------------------

This file is only required if you are using the assertion service and can be
omitted if you are only using the login service.

This file contains config parameters for the 'Service Provider' - your end of
the authentication dialog - which will talk to the assertion service.  Once you
have generated the SP metadata file (see: L</Generating Config Files>) you will
need to provide it to the RealMe logon service to install at their end.  You
will need to generate separate metadata files for each of your development,
staging and production environments.

metadata-assertion-idp.xml
--------------------------

This file is only required if you are using the assertion service and can be
omitted if you are only using the login service.

The assertion service IdP or Identity Provider metadata file will be provided
to you by RealMe/DIA.  You will simply need to copy it to the config directory
and give it the correct name.

metadata-icms.wsdl
------------------

This file is only required if you are both using the assertion service and need
to resolve the opaque token into an FLT.  It can be omitted if you are only
using the login service or do not need the user's FLT.

The WSDL file will be provided to you by RealMe/DIA.  You will simply need to
copy it to the config directory and give it the correct name.

sp-sign-crt.pem
---------------

This certificate file is used for generating digital signatures for the SP
metadata file and SAML authentication requests.  For your initial integration
with the RealMe login service development IdP ('MTS'), certificate key-pair
files will be provided to you.  For staging (ITE) and production, you will need
to generate your own and provide the certificate files (not the private key
files) to the RealMe login service.

sp-sign-key.pem
---------------

This private key is paired with the **sp-sign-crt.pem** certificate.

sp-ssl-crt.pem
--------------

This certificate is used for negotiating an SSL connection on the backchannel
to the IdP artifact resolution service.

sp-ssl-key.pem
--------------

This private key is paired with the **sp-ssl-crt.pem** certificate.


