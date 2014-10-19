# -*- coding: utf-8 -*-
"""Manipulate NZ RealMe Login service AuthnContextClassRef values"""


__all__ = (
    'LogonStrength',
    )


URN_PREFIX = 'urn:nzl:govt:ict:stds:authn:deployment:GLS:SAML:2.0:ac:classes:'

STRENGTH_LOW = URN_PREFIX + 'LowStrength'
STRENGTH_MODERATE = URN_PREFIX + 'ModStrength'
STRENGTH_MODERATE_SID = URN_PREFIX + 'ModStrength::OTP:Token:SID'
STRENGTH_MODERATE_SMS = URN_PREFIX + 'ModStrength::OTP:Token:SMS'

WORD_TO_URN = {
    'low': STRENGTH_LOW,
    'mod': STRENGTH_MODERATE,
    'moderate': STRENGTH_MODERATE,
    }

STRENGTH_SCORE = {
    STRENGTH_LOW: 10,
    STRENGTH_MODERATE: 20,
    STRENGTH_MODERATE_SID: 20,
    STRENGTH_MODERATE_SMS: 20,
    }

class LogonStrength(object):
    """
    The NZ RealMe Login service supports the notion of logon strength.  For example
    a user session authenticated with a username and password is a 'low strength'
    logon.  Whereas authenticating with a user, password and SecurID token will
    result in a moderate strength logon.  The different logon strengths are
    represented by URNs which will be present in the initial SAML AuthnRequest
    message as well as the assertion in the resulting ArtifactResponse.

    This class is used to encapsulate the URNs and to provide methods for comparing
    the strength of one URN to another.

    Attributes:
        urn (str): Default to 'urn:nzl:govt:ict:stds:authn:deployment:GLS:SAML:2.0:ac:classes:LowStrength'
    """
    urn = STRENGTH_LOW

    def __init__(self, strength='low'):
        try:
            self.urn = WORD_TO_URN[strength]
        except KeyError:
            raise ValueError(
                '{0} is not a valid stength expecting {1}'.format(
                    strength, ' or '.join(WORD_TO_URN.keys())))

    @property
    def score(self):
        """
        Returns the strength score (currently either 10 or 20) which is used when
        comparing strengths using the 'minimum' match type.

        Returns:
            Int: Numerical strength score.
        """
        return STRENGTH_SCORE[self.urn]

    def assert_match(self, required='low', match='minimum'):
        """
        This method returns if the provided logon strength matches the required
        strength, or dies if the strength does not meet the specified requirement.

        The **required** strength will default to 'low' if not provided.

        The **match** parameter must be 'exact' or 'minimum' (default
        'minimum').  When comparing different logon strengths, the rules outlined in
        the RealMe Login service SAML v2.0 Messaging Specification are used.

        Args:
            required (str): Defaults to 'low'
            match (str): Defaults to 'minimum'

        Returns:
            Bool:
        """
        pass

