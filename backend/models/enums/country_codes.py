from enum import Enum

class CountryCode(str, Enum):
    US = "US"
    GB = "GB"
    DE = "DE"
    FR = "FR"
    JP = "JP"
    # Add more country codes as needed