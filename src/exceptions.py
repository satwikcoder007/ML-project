import sys   # Provides methods to communicate with  Python runtime environment
import os
from src.logger import logger  # Import the custom logger


class CustomException(Exception): ## extend the base Exception class
    """
    Custom exception class that captures error details such as
    filename, line number, and function where the error occurred.
    """

    def __init__(self, message: str, original_exception: Exception = None): ## constructor

        super().__init__(message) ## calling the base class constructor

        self.message = message
        self.original_exception = original_exception
        self.filename = None
        self.lineno = None
        self.function_name = None

        # Capture traceback info (if available)
        _, _, exc_traceback = sys.exc_info()
        if exc_traceback:
            # Go to the deepest traceback where the error occurred
            while exc_traceback.tb_next:
                exc_traceback = exc_traceback.tb_next

            frame = exc_traceback.tb_frame
            self.filename = os.path.basename(frame.f_code.co_filename)
            self.lineno = frame.f_lineno
            self.function_name = frame.f_code.co_name

    def __str__(self) -> str:
        """
        this __str__ method allows you to decide what to print if someone print the object so its lke overloading
        """
        details = f"Error: {self.message}"
        if self.filename and self.lineno and self.function_name:
            details += f"\n  At {self.filename}:{self.lineno} in {self.function_name}()"
        if self.original_exception:
            details += f"\n  Caused by: {type(self.original_exception).__name__}: {self.original_exception}"

        return details

    def log(self):
        """
        Log the error details using the configured logger.
        """
        details = f"Error: {self.message}"
        if self.filename and self.lineno and self.function_name:
            details += f"\n  At {self.filename}:{self.lineno} in {self.function_name}()"
        if self.original_exception:
            details += f"\n  Caused by: {type(self.original_exception).__name__}: {self.original_exception}"

        logger.error(details)
