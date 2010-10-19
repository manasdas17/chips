class StreamsConstructionError(Exception):
    """Error in definition of streams system"""

    def __init__(self, message, filename, lineno):
        self.message = message + "\nfile : {0}, line : {1}".format(filename, lineno)

class StreamsProcessError(Exception):
    """Error in definition of process instructions"""

    def __init__(self, message, filename, lineno):
        self.message = message + "\nfile : {0}, line : {1}".format(filename, lineno)
