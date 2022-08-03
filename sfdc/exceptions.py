
class SalesforceException(Exception):
	"""Base class for Salesforce API exceptions"""

class TokenNotCreated(SalesforceException):
	"""Fail to generate token"""