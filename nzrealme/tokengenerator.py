# -*- coding: utf-8 -*-
"""Generate SAML ID strings"""
import random


__all__ = (
    'TokenGenerator',
    )


class TokenGenerator(object):
    """
    This class is responsible for generating random ID tokens such as:

        e5111f121b7b5f8533d18d98e1ec8ade294c62cc3

    Although the methods are described below, the preferred way to use this
    class is via the ServiceProvider:

        service_provider.generate_saml_id()

    """

    def saml_id(self):
        """
        Generates and returns a hex-encoded random token (guaranteed to start
        with a letter) using strong_token if possible and weak_token otherwise.

        Returns:
            string: hex-encoded random token (with alphabetical first char)
        """
        token = self.strong_token()
        while token[0] in [str(i) for i in range(10)]:
            token = self.strong_token()
        return token

    def strong_token(self):
        """
        This method will read 20 bytes from the random device and return a
        hex-encoded representation of those bytes.

        The default length of 12 with the a-z, A-Z, 0-9 character set returns
        a 71-bit value. log_2((26+26+10)^12) =~ 71 bits

        Credit to the django project for this code: django.utils.crypto

        Returns:
            string: hex-encoded random token
        """
        length = 40
        allowed_chars = 'abcdefghijklmnopqrstuvwxyz0123456789'

        try:
            rand = random.SystemRandom()
        except NotImplementedError:
            import warnings
            warnings.warn('A secure pseudo-random number generator is not '
                          'available on your system.')

        return ''.join(rand.choice(allowed_chars) for i in range(length))
