"""Top-level exception classes
"""   
from pysnmp import error

class SnmpApplicationError(error.PySnmpError): pass
