class BaseValidator:
    """
    Base class for all validators.
    Accepts a configuration dictionary during initialization.
    """
    def __init__(self, config):
        self.column_name = config.get("column_name")
        self.params = config.get("params", {})

    def validate(self, data, valid_pins):
        """
        Validate data and return a list of invalid cell references.
        Must be implemented by each subclass.
        """
        raise NotImplementedError("Each validator must implement the 'validate' method.")
