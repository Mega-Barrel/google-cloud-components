import logging
import os

class Logger:
    """
    A class to create and manage a logger for an application.

    Logs messages to both a specified file and the console.
    It supports different log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """

    def __init__(self, name: str, log_file: str, log_level=logging.INFO):
        """
        Initializes the Logger instance.

        Args:
            name (str): The name of the logger, typically the module or application name.
            log_file (str): The path to the log file where messages will be saved.
            log_level (int): The minimum logging level to output. Defaults to logging.INFO.
        """
        # Create a custom logger with the specified name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Check if handlers already exist to prevent duplicate log entries
        if not self.logger.handlers:
            # Create a file handler to save logs to a file
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)

            # Define the log format
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

    def get_logger(self):
        """
        Returns the configured logger object.

        Returns:
            logging.Logger: The configured logger instance.
        """
        return self.logger

if __name__ == "__main__":
    # Define the log file path
    LOG_FILE_PATH = "log"

    # Create the directory if it doesn't exist
    os.makedirs(LOG_FILE_PATH, exist_ok=True)

    # Create a logger instance for the main application
    my_logger = Logger(
        "google_cloud_components",
        log_file=os.path.join(LOG_FILE_PATH, 'google_cloud_components.log'),
        log_level=logging.DEBUG
    )

    # Get the logger object and log some messages
    logger = my_logger.get_logger()

    logger.debug("This is a debug message.")
    logger.info("This is an informational message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")

    print(f"Logs have also been saved to the '{LOG_FILE_PATH}' file.")
