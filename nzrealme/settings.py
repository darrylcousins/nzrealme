# -*- coding: utf-8 -*-
"""
NZRealMe_Settings class

A subclass of OneLogin_Saml2_Settings
"""

from onelogin.saml2.settings import OneLogin_Saml2_Settings

__all__ = (
    'NZRealMe_Settings',
    )


class NZRealMe_Settings(OneLogin_Saml2_Settings):
    """
    XXX NOT USED, but left here just in case during development.

    A subclass of :class:`onelogin.saml2.OneLogin_Saml2_Settings`.

    Handles the settings, by subclassing and allowing extra attributes as
    required by nzrealme.

        >>> saml_settings = loadSettings()
        >>> settings = NZRealMe_Settings(saml_settings)

    """
    pass
