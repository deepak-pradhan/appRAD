import random
from typing import Literal, Sequence
from faker import Faker
fake = Faker()


class File:
    """
    faker.providers.file
        file_extension()
        file_name()
        mime_type()
    """
    def __init__(self
            , depth: int = 1
            , category: str = 'image'
            , extension: str | Sequence[str] | None = None
            , absolute: bool | None = True
            , file_system_rule: Literal['linux', 'windows'] = 'linux') -> str:
        
        self.generated = set()
        self.category = category
        self.depth = depth

        VALID_CATEGORIES = ['audio', 'image', 'office', 'text', 'video']
        self.generated = {
            'file_extension' : fake.file_extension(
                                    category=self.category
                                )
            , 'file_name' : fake.file_name(
                                category=self.category
                                , extension='png'
                            )
            , 'file_path' : fake.file_path(
                                depth=1
                                , category=self.category
                                , extension='png'
                                , absolute=False
                                ,file_system_rule='linux'
                            )
        }
        
    def generate_file_name(self):
        return self.generated