class UserError(Exception):
    """base class for all expected user induced errors
    (mainly used to exit program without printing stacktrace for better readability)"""
