# -*- coding: utf-8 -*-
"""
NZRealMe_Utils class

A subclass of OneLogin_Saml2_Utils
"""

from hashlib import sha1
from uuid import uuid4

from onelogin.saml2.utils import OneLogin_Saml2_Utils

__all__ = (
    'NZRealMe_Utils',
    )


class NZRealMe_Utils(OneLogin_Saml2_Utils):
    """
    A subclass of :class:`onelogin.saml2.OneLogin_Saml2_Utils`.

    Auxiliary class that contains several utility methods to parse time,
    urls, add sign, encrypt, decrypt, sign validation, handle xml ...

    """

    @staticmethod
    def generate_unique_id():
        """
        Generates an unique string (used for example as ID for assertions).

        :return: A unique string
        :rtype: string
        """
        return 'NZREALME_%s' % sha1(uuid4().hex).hexdigest()
