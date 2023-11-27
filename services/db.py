# from mongoengine import connect
from datetime import datetime
from pymongo import MongoClient
from config.settings import db_settings
from models.user import User
from models.image import Image
# from router.user import db_connector


class DatabaseConnector:
    def __init__(self):
        # print('\n\n\n\n\======================Connecting to Mongo DB=============\n\n\n\n')
        self.db_client = MongoClient(db_settings.client_uri)
        self.db = self.db_client[db_settings.db_name]
        self.user_collection = self.db['Users']
        self.image_collection = self.db['Images']

db_connector = DatabaseConnector()

def insert_one_user(Object : User):
    """Insert One Record in Database

    Args:
        Object (User): Object of the User
    """
    # print('Type of User : ******', type(User) )
    # print('\n\nObject : ', Object.to_mongo().to_dict())
    user_data = Object.to_mongo().to_dict()
    db_connector.user_collection.insert_one(user_data)
    # print('******')
    # Object.save()

def search_by_email(email : str) -> User:
    """Search Record By Email

    Args:
        email (str): Email ID of the User

    Returns:
        User: Object of the data
    """
    # user_data = User.objects(email = email)
    # print('******')
    user_data = db_connector.user_collection.find_one({'email': email})
    # print('------\n\n User Data : ', user_data)
    # print('\n\nType : ', type(user_data))
    return user_data

def check_user_data(email: str, password: str) -> int:
    """Check User is valid or Not

    Args:
        email (str): User Emial ID
        password (str): User Password

    Returns:
        Code: 100 = User is Valid.
              102 = User is not Valid. 
    """
    # user_data = User.objects(email = email)
    user_data = db_connector.user_collection.find_one({'email': email})
    if user_data['email'] == email and user_data['password'] == password:
        return 100
    else:
        return 102

def insert_one_user_image(Object: Image) -> None:
    Object.save()

def insert_or_update_user_image(file_name: str, email: str, url: str) -> None:
    query = {'email': email, 'filename': file_name}
    image_list = db_connector.image_collection.count_documents(query)
    # print('\n\n\nImages Data 1111111111: ', image_list)
    if image_list > 0:
        db_connector.image_collection.update_one(query, {'$set': {'updated_at': datetime.utcnow()}})
    else:
        Object =Image(email=email, filename=file_name, url=url)
        image_data = Object.to_mongo().to_dict()
        db_connector.image_collection.insert_one(image_data)
    
    # images_list = Image.objects(email = email, filename = file_name)
    # if images_list:
    #     images_list.update(updated_at = datetime.utcnow())
    # else:
    #     image_object = Image(email = email, filename = file_name, url = url)
    #     image_object.validate()
    #     image_object.save()

def get_user_images_by_email(email: str) -> list:
    # user_data = Image.objects(email = email)
    user_data = db_connector.image_collection.find({'email':email})
    # print('\n\n\nImages Data : ', user_data)
    user_images = []
    for doc in user_data:
        # print(doc)
        user_images.append(doc['url'])
    return user_images

def update_user_detailsby_email(body: dict) -> None:
    User.objects(email = body["email"]).update_one(set__first_name = body["first_name"], set__last_name = body["last_name"], set__password = body["password"])