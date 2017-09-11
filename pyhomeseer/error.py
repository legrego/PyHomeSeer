"""
Errors to be used by PyHomeSeer.
"""


class PyHomeSeerError(Exception):
    """ Base error for PyHomeSeer. """
    pass


class PyHomeSeerAuthenticationError(PyHomeSeerError):
    """ Error Authenticating to HomeSeer """
    pass
