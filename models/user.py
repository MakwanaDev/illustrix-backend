from mongoengine import Document, StringField, DateTimeField, EmailField
import datetime
# import pytz

class User(Document):
    first_name = StringField(required = True, max_length = 100)
    last_name = StringField(required = True, max_length = 100)
    email = EmailField(required = True, unique = True)
    password = StringField(required = True, max_length = 100)
    created_at = DateTimeField(default = datetime.datetime.now(datetime.timezone.utc))
    updated_at = DateTimeField(default =  datetime.datetime.now(datetime.timezone.utc))

    # meta = {'collection': 'Users'} 
# class User:
#     def __init__(self, db) -> None:
#         self.collection = db['Users']

    