"""Custom exception classes for NATO Exercise application.

This module defines a hierarchy of custom exceptions for better error handling
and more specific error messages in production code.
"""


class NATOExerciseError(Exception):
    """Base exception for all NATO Exercise related errors.
    
    All custom exceptions in this module should inherit from this class.
    This allows catching all application-specific errors with a single except clause.
    
    Example:
        try:
            # Some operation
        except NATOExerciseError as e:
            # Handle any application error
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
    pass


class FileNotFoundError(NATOExerciseError):  # Note: shadows built-in FileNotFoundError
    """Raised when a required file cannot be found.
    
    This wraps the built-in FileNotFoundError to provide more context
    about which file was expected and why it's needed.
    
    Note: This class name shadows Python's built-in FileNotFoundError.
    Consider renaming to NATOFileNotFoundError or wrapping the built-in
    exception instead of shadowing it.
    
    Attributes:
        file_path: Path to the file that was not found
        message: Optional custom error message
    
    Example scenarios:
        - CSV file missing from expected location
        - Configuration file not found
        - Log file directory doesn't exist
    
    TODO: Add file_path attribute and custom message formatting
    """
    pass


class InvalidCSVError(NATOExerciseError):
    """Raised when CSV file is malformed or invalid.
    
    This exception should be raised when:
        - CSV file cannot be parsed
        - CSV has incorrect encoding
        - CSV structure is invalid (wrong delimiter, quotes, etc.)
        - CSV is empty or corrupted
    
    Attributes:
        file_path: Path to the invalid CSV file
        reason: Explanation of why the CSV is invalid
    
    Example scenarios:
        - CSV has wrong delimiter
        - CSV has unclosed quotes
        - CSV encoding is not UTF-8
        - CSV is binary or not text
    
    TODO: Add file_path and reason attributes
    """
    pass


class InvalidInputError(NATOExerciseError):
    """Raised when user input fails validation.
    
    This exception should be raised when:
        - Input contains non-alphabetic characters
        - Input is empty or whitespace only
        - Input contains special characters that cannot be converted
        - Input is None
    
    Attributes:
        input_value: The invalid input that was provided
        reason: Explanation of why the input is invalid
    
    Example scenarios:
        - User enters "123" (contains numbers)
        - User enters "hello!" (contains special characters)
        - User enters empty string
        - User enters None
    
    TODO: Add input_value and reason attributes with validation
    """
    pass


class MissingDataError(NATOExerciseError):
    """Raised when required data is missing from CSV.
    
    This exception should be raised when:
        - CSV is missing required columns (e.g., 'letter' or 'code')
        - CSV has empty rows where data is expected
        - Required mappings are missing (e.g., no entry for letter 'A')
        - CSV structure doesn't match expected format
    
    Attributes:
        missing_field: Name of the missing field/column
        file_path: Path to the CSV file with missing data
        available_fields: List of fields that are present
    
    Example scenarios:
        - CSV missing 'letter' column
        - CSV missing 'code' column
        - CSV has no rows (empty data)
        - Specific letter mapping is missing
    
    TODO: Add missing_field, file_path, and available_fields attributes
    """
    pass


class ConfigurationError(NATOExerciseError):
    """Raised when there are configuration issues.
    
    This exception should be raised when:
        - Configuration file is missing
        - Configuration has invalid values
        - Required environment variables are not set
        - Configuration format is invalid (e.g., invalid JSON/YAML)
    
    Attributes:
        config_key: The configuration key that caused the error
        reason: Explanation of the configuration error
        config_file: Optional path to the configuration file
    
    Example scenarios:
        - Missing CSV_PATH environment variable
        - Invalid log level in config
        - Configuration file has syntax errors
        - Required config section is missing
    
    TODO: Add config_key, reason, and config_file attributes
    """
    pass

