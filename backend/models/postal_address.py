import re
from enum import Enum
# @TODO:
# from i18naddress import InvalidAddressError, normalize_address
# https://pypi.org/project/google-i18n-address/
from backend.models.bases.bmodel import BModel
from sqlmodel import Field
from backend.models.enums.country_codes import CountryCode

class PostalAddress1(BModel, table=False):
    __tablename__ = "postal_address"

    # Core properties
    country_code: CountryCode | None = Field(default=None, description="e.g., US, GB, DE")
    state: str | None = Field(default=None, description="State or Province")
    city: str | None = Field(default=None, description="City or Town Name")
    locality: str | None = Field(default=None, description="District or City Area")
    region: str | None = Field(default=None, description="Region within the country")
    postal_code: str | None = Field(default=None, description="Postal or Zip code")
    street_address: str | None = Field(default=None, description="Street address (e.g., 1600 Amphitheatre Pkwy)")
    street_landmark: str | None = Field(default=None, description="Nearby landmark (e.g., near Corner Store)")

    # Additional properties
    address_type: str | None = Field(default=None, description="Type of address (e.g., residential, business)")
    country_name: str | None = Field(default=None, description="Full name of the country")
    sublocality: str | None = Field(default=None, description="Neighborhood within District or City Area")
    contact_type: str | None = Field(default=None, description="Purpose of contact (e.g., sales, PR)")
    telephone: str | None = Field(default=None, description="Telephone number")
    email: str | None = Field(default=None, description="Email address")


    def validate(self) -> None:
        super().validate()
        # Add any specific pre-validation logic for PostalAddress here
        self.validate_postal_code(self.country_code,self.postal_code)
        # Validate at create/update: use Google/Postal Office API


    def validate_postal_code(self, country_code, postal_code):
        """Validates Postal code by Country."""

        match country_code:
            case "US": # USA
                pattern = r"^\d{5}(?:-\d{4})?$"
            case "CN": # Canada
                pattern = r"^[A-Z]\d[A-Z] \d[A-Z]\d$"
            case "FR": # France
                pattern = r"^\d{5}$"
            case "JP": # Japan
                pattern = r"^\d{3}-\d{4}$"
            case "UK": # UK
                pattern = r"^[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}$"
            case _:
                ValueError(f"Cannot validate {postal_code} for case : {country_code}")

        return bool(re.match(pattern, postal_code))  


    def __repr__(self):
        return f"<PostalAddress1(id={self.id}, country='{self.country}', locality='{self.locality}')>"