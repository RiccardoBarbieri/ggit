class ConfigException(Exception):
    """
    Custom exception raised when there are problems related to the
    configuration settings of the database.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message