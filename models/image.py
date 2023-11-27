from mongoengine import Document, StringField, DateTimeField, EmailField
import datetime
# import pytz

class Image(Document):
    email = EmailField(required=True)
    filename = StringField(required=True)
    url = StringField(required=True)
    created_at = DateTimeField(default = datetime.datetime.now(datetime.timezone.utc))
    updated_at = DateTimeField(default =  datetime.datetime.now(datetime.timezone.utc))

