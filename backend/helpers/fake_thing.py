from faker import Faker
fake = Faker()

class Thing:

    data = []
    def get_data(rec_type = 'Thing'
                 , name = 'Thing'
            ):   
             
        data = {
            'name' : name
            , 'alternate_name'   : ''
            , 'additional_types' : 'Renters, Subscribers, ...'
            , 'image': ''
            , 'description' : ''
            , 'disambiguating_description': ''
            , 'about' : 'str'
            , 'category': 'str'
            , 'knows_about' : 'str'
            , 'mentions': 'str'
            , 'produces': 'str'
            , 'replaces': 'str'
            , 'replacer': 'str'
            , 'services': 'str'  
        }

        return data