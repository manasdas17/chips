"""Common exceptions"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1.1"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

class ChipsSyntaxError(Exception):
    """Error in definition of streams system"""

    def __init__(self, message, filename, lineno):
        message =  "\n    " + message
        message += "\n"
        message += "        "
        message += "File {0}, line {1}".format(filename, lineno)
        Exception.__init__(self, message) 

class ChipsProcessError(Exception):
    """Error in definition of process instructions"""

    def __init__(self, message, filename, lineno):
        message =  "\n    " + message
        message += "\n"
        message += "        "
        message += "File {0}, line {1}".format(filename, lineno)
        Exception.__init__(self, message) 

class ChipsSimulationError(Exception):
    """Error in definition of process instructions"""

    def __init__(self, message, filename, lineno):
        message =  "\n    " + message
        message += "\n"
        message += "        "
        message += "File {0}, line {1}".format(filename, lineno)
        Exception.__init__(self, message) 
