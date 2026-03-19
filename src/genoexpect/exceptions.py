"""Custom exceptions for genoexpect."""


class GenoExpectError(Exception):
    """Base package exception."""


class StudyNotFoundError(GenoExpectError):
    """Raised when a study id is missing from config."""


class InvalidConfigError(GenoExpectError):
    """Raised when study config is malformed."""
