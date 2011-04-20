"""Common exceptions"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

class ChipsSyntaxError(Exception):
    """Error in definition of streams system"""

    def __str__(self):
        message = self.args["message"]
        filename = self.args["filename"]
        lineno = self.args["lineno"]
        return message + "\nfile : {0}, line : {1}".format(filename, line)

class ChipsProcessError(Exception):
    """Error in definition of process instructions"""

    def __str__(self):
        message = self.args["message"]
        filename = self.args["filename"]
        lineno = self.args["lineno"]
        return message + "\nfile : {0}, line : {1}".format(filename, line)

class ChipsSimulationError(Exception):
    """Error in definition of process instructions"""

    def __str__(self):
        message = self.args["message"]
        filename = self.args["filename"]
        lineno = self.args["lineno"]
        return message + "\nfile : {0}, line : {1}".format(filename, line)
