from cerberus import Validator
person_schema = {
    'first_name': {
        'type': 'string', 
        'minlength': 2, 
        'maxlength': 50, 
        'required': True
    },
    'middle_name': {
        'type': 'string', 
        'minlength': 0, 
        'maxlength': 50, 
        'required': True
    },
    'last_name': {
        'type': 'string', 
        'minlength': 2, 
        'maxlength': 50, 
        'required': True
    },
    'name': {
        'type': 'string', 
        'minlength': 2, 
        'maxlength': 50, 
        'required': True
    },
    'address': {
        'type': 'dict',
        'schema': {
            'street': {'type': 'string', 'maxlength': 100, 'required': True},
            'city': {'type': 'string', 'maxlength': 50, 'required': True},
            'state': {'type': 'string', 'maxlength': 50, 'required': True},
            'postal_code': {'type': 'string', 'maxlength': 10, 'required': True},
            'country': {'type': 'string', 'maxlength': 50, 'required': True}
        }
    },
    'email': {
        'type': 'string', 
        'regex': r'^[^@]+@[^@]+\.[^@]+$', 
        'required': True
    },
    'phone': {
        'type': 'string', 
        'regex': r'^\+?[1-9]\d{1,14}$',
        'required': True
    },
    'date_of_birth': {
        'type': 'string', 
        'regex': r'^\d{4}-\d{2}-\d{2}$', 
        'required': True
    },
    'gender': {
        'type': 'string', 
        'allowed': ['Male', 'Female', 'Non-Binary', 'Other'],
        'required': False
    },
    'nationality': {
        'type': 'string', 
        'maxlength': 50,
        'required': False
    }
}