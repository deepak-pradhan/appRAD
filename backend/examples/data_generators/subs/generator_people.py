import random
from cerberus import Validator
from mimesis import Person, Address
from mimesis.enums import Gender
from mimesis.builtins import USASpecProvider
from backend.examples.common.schemas.person.person import person_schema

# Initialize Mimesis providers
person_gen = Person()
address_gen = Address()
validator = Validator(person_schema)

def generate_gender_code():
    """Generate ISO/IEC 5218 gender code
    0 = Not known
    1 = Male 
    2 = Female
    9 = Not applicable
    """
    return random.choice([0, 1, 2, 9])

def generate_person():
    us = USASpecProvider()
    
    # Map ISO gender code to Mimesis Gender enum
    gender_code = generate_gender_code()
    gender_map = {
        0: random.choice([Gender.MALE, Gender.FEMALE]),  # Random for unknown
        1: Gender.MALE,
        2: Gender.FEMALE,
        9: random.choice([Gender.MALE, Gender.FEMALE])   # Random for not applicable
    }
    gender_value = gender_map[gender_code]
    first_name = person_gen.first_name(gender=gender_value)
    
    # Middle name logic: 30% chance of None, 35% chance of single character, 35% chance of first_name
    middle_name = ''
    if random.random() > 0.3:
        middle_name = person_gen.first_name(gender=gender_value)
        if random.random() < 0.5:
            middle_name = middle_name[0]  # Single character (initial)

    last_name = person_gen.last_name()
    gender = "Male" if gender_value == Gender.MALE else "Female"  # Schema-compliant gender value

    return {
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'name': f"{first_name} {middle_name} {last_name}",
        'address': {
            'street': address_gen.street_name(),
            'city': address_gen.city(),
            'state': address_gen.state(), # us.state(),
            'postal_code': address_gen.postal_code(),
            'country': address_gen.country()
        },
        'email': person_gen.email(),
        'phone': person_gen.telephone(),
        'date_of_birth': person_gen.birthdate().isoformat(),
        'gender': gender,
        'nationality': person_gen.nationality(),
    }
def validate_person_data(data):
    """Validate a person record against the Cerberus schema."""
    if validator.validate(data):
        return validator.document  # Return validated data
    else:
        print("Validation error:", validator.errors)
        return None
    
def generate_data(target_size_in_bytes):
    """
    Generate synthetic person data until it reaches the target size.
    Returns a list of validated person records.
    """
    data = []
    size = 0
    while size < target_size_in_bytes:
        raw_data = generate_person()
        # validated_data = validate_person_data(raw_data)
        validated_data = raw_data
        if validated_data:
            data.append(validated_data)
            size += sum(len(str(v)) for v in flatten_dict(validated_data).values()) + len(validated_data)
    return data

# Utility function to flatten nested dictionaries (e.g., flatten the address in person data)
def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

