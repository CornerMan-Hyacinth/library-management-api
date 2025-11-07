from enum import Enum

class Gender(str, Enum):
    male = "male"
    female = "female"

class ResponseStatus(str, Enum):
    """Allowed values for the `status` field."""
    SUCCESS = "success"
    ERROR = "error"