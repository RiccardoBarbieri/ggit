class ProcessException(Exception):
    """
    Custom exception raised when there are problems related to execution
    of a process.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message