from enum import Enum
"""
The Sort and Direction Enums each enumerate the different options supported for sortBy and direction
"""

class Sort(Enum):
    id = 1
    reads = 2
    likes = 3
    popularity = 4

class Direction(Enum):
    desc = 1
    asc = 2

