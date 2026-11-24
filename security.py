"""Shared API error. Telegram validation is introduced in Issue #3."""
class ApiError(Exception):

    def __init__(self, status, code, message, details=None):
        (self.status, self.code, self.message, self.details) = (status, code, message, details)
