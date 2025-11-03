from enum import Enum

class Gender(str, Enum):
    male = "male"
    female = "female"
    
class BookAvailable(str, Enum):
    all = "all"
    available = "available"
    borrowed = "borrowed"