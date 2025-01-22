import sys


class NetworkSecurityException(Exception):
    """
    Custom Exception to handle Network Security Errors.
    """

    def __init__(self, error_message: str, error_details: sys):
        """
        Initialize the custom exception with error message and details.
        """
        super().__init__(error_message)
        self.error_message = error_message
        self.error_details = error_details

        # Extract exception traceback information
        _, _, exc_tb = error_details.exc_info()
        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        """
        Return a formatted string of the exception details.
        """
        return (
            f"Error occurred in file: {self.filename} at line number: {self.lineno} "
            f"with error message: {self.error_message}"
        )
