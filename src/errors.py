class Error(Exception):
    """Base class for exceptions"""
    pass

class VirusTotalApiError(Error):
    """
    Custom-defined exception for error messages returned by the API.
    
    """
    def __init__(self, message):
        self.message = message