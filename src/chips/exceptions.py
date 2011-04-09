"""Common exceptions"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

class StreamsConstructionError(Exception):
    """Error in definition of streams system"""

    def __init__(self, message, filename, lineno):
        self.message = message + "\nfile : {0}, line : {1}".format(filename, lineno)

class StreamsProcessError(Exception):
    """Error in definition of process instructions"""

    def __init__(self, message, filename, lineno):
        self.message = message + "\nfile : {0}, line : {1}".format(filename, lineno)

class SimulationError(Exception):
    """Error in definition of process instructions"""

    def __init__(self, message, filename, lineno):
        self.message = message + "\nfile : {0}, line : {1}".format(filename, lineno)
