import os
from config.settings import file_structure, s3_credentials
import cv2
import numpy as np
import base64
import random
import string
import shutil
import boto3
from botocore.exceptions import NoCredentialsError
from io import BytesIO
from PIL import Image
import requests


def generate_presigned_url(object_name, s3_path=True, expiration=3600):
    """
    Generate a pre-signed URL for uploading an object to an S3 bucket.

    :param bucket_name: The name of the S3 bucket.
    :param object_name: The key (path) of the object within the bucket.
    :param expiration: The expiration time for the pre-signed URL in seconds (default is 1 hour).
    :return: A pre-signed URL for uploading the object to S3.
    """
    s3 = boto3.client('s3', aws_access_key_id='AKIARGPTIVBM3RH6CTDV',
                      aws_secret_access_key='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')

    try:
        response = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': s3_credentials.bucket_nm, 'Key': object_name},
            ExpiresIn=expiration
        )
        if s3_path:
            # print(response)
            return response.split('?')[0]
        return response
    
    except NoCredentialsError:
        return None


# import requests

# def upload_image_data_with_presigned_url(presigned_url, image_data):
#     """
#     Upload image data to Amazon S3 using a pre-signed URL.

#     :param presigned_url: The pre-signed URL generated for the S3 upload.
#     :param image_data: The binary image data you want to upload.
#     :return: True if the upload was successful, False otherwise.
#     """
#     try:
#         response = requests.put(presigned_url, data=image_data)
#         if response.status_code == 200:
#             return True
#         else:
#             return False
#     except Exception as e:
#         print(f"Upload error: {e}")
#         return False



def upload_image_to_s3(image, file_path):

    if not isinstance(image, bytes):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(image, mode='RGB')
        out_img = BytesIO()
        img.save(out_img, format='png')
        out_img.seek(0)  
    else:
        out_img = BytesIO(image)

    print(type(image))
    s3 = boto3.client('s3', aws_access_key_id=s3_credentials.aws_access_keyid,
                      aws_secret_access_key=s3_credentials.aws_secret_accesskey)

    bucket = s3_credentials.bucket_nm
    
    try:
        s3.upload_fileobj(out_img, bucket, file_path)

        print(f"Image data uploaded to S3: s3://{bucket}/{file_path}")
    except Exception as e:
        print(f"Upload error: {e}")

def fetch_image_from_url(image_url: str, pillow: bool = False) -> Image:
    try:
        # Send an HTTP GET request to the URL to fetch the image
        response = requests.get(image_url)
        if response.status_code == 200:
            # Read the content (image data) from the response
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            if pillow:
                return image
            image = np.array(image)
            if image.shape[2] == 3:  # Check if it's an RGB image
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            else:
                image = image[:, :, :3]
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            return image
        else:
            # Handle the case when the request was not successful
            print(f"Failed to fetch image from URL: {image_url}")
            return None
    except Exception as e:
        # Handle any exceptions that might occur during the process
        print(f"An error occurred: {str(e)}")
        return None

def create_base_structure(email: str) -> None:
    # Initialize the S3 client
    s3 = boto3.client('s3', aws_access_key_id='AKIARGPTIVBM3RH6CTDV', aws_secret_access_key='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')

    # Define the S3 bucket name
    bucket_name = s3_credentials.bucket_nm

    base_folder = file_structure.USER_DATA + email
    
    try:
        # Check if the base folder exists in S3
        response = s3.head_object(Bucket=bucket_name, Key=base_folder)
    except Exception as e:
        # If the base folder doesn't exist, create it
        s3.put_object(Bucket=bucket_name, Key=base_folder)
        # Create subfolders in S3
        for sub_folder in file_structure.BASE_STRUCTURE:
            sub_folder_path = base_folder + sub_folder
            s3.put_object(Bucket=bucket_name, Key=sub_folder_path)

def get_file_path_from_url(body: dict, email : str = '') -> str:
    global_url = body["image_url"]
    file_name = body["image_url"].split("/")[-1]
    system_path = file_structure.USER_DATA + email + file_structure.FINAL_IMAGE_PATH + body['image_url'].split("/")[-1]
    background_image = ""
    factor = 0
    save = 1
    revert = 0
    if "background_url" in body:
        background_image = file_structure.USER_DATA + email + file_structure.FINAL_IMAGE_PATH + body['background_url'].split("/")[-1]
    if "factor" in body:
        factor = body["factor"]
    if "save" in body:
        save = body["save"]
    if "revert" in body:
        revert = body["revert"]
    return file_name, system_path, global_url, background_image, factor, save, revert

def save_to_final_folder(path: str, image: np.ndarray) -> None:

    upload_image_to_s3(image, path)

def save_to_sub_folder(path: str, image: np.ndarray) -> None:
    upload_image_to_s3(image, path)

def generate_random_string() -> str:
    random_string = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return random_string

def upload_image(email: str, base_64_string: str) -> str:
    image = base64.b64decode(base_64_string, validate=True)
    upload_path = file_structure.USER_DATA + email + file_structure.UPLOAD_PATH
    file_name = generate_random_string() + ".png"
    file_path = upload_path + file_name
    final_file_path = file_structure.USER_DATA + email + file_structure.FINAL_IMAGE_PATH + file_name
    upload_image_to_s3(image, file_path=final_file_path)
    upload_image_to_s3(image, file_path=file_path)
    global_path = generate_presigned_url(object_name=final_file_path)

    print(global_path)
    return global_path, file_name

def create_copy_image(from_path: str, to_path: str, file_name: str) -> str:
    last_slash_index = to_path.rfind("/")
    copy_path = to_path[:last_slash_index + 1] + file_name.split(".")[0] + file_structure.COPY_FILE_SUFFIX + "." + file_name.split(".")[-1]
    s3 = boto3.client('s3')
    source_bucket = s3_credentials.bucket_nm
    source_key = from_path
    destination_key = copy_path

    try:
        # Use the copy_object method to copy the file
        s3.copy_object(CopySource={'Bucket': source_bucket, 'Key': source_key}, Bucket=source_bucket, Key=destination_key)
        print(f"File copied from {source_key} to {destination_key} within the bucket {source_bucket}.")
    except Exception as e:
        print(f"File copy failed: {str(e)}")

def check_copy_file_exist(original_path: str,sub_path: str, file_name: str) -> str:

    # Initialize the S3 client
    s3 = boto3.client('s3')

    # Define the S3 bucket and file/key you want to check
    bucket_name = s3_credentials.bucket_nm
    file = file_name.split(".")[0]
    copy_path = sub_path.replace(file, file + file_structure.COPY_FILE_SUFFIX)
    file_key = copy_path

    try:
        # Use the head_object method to check if the file exists
        print(f"File {file_key} exists in the bucket {bucket_name}.\n\n")
        s3.head_object(Bucket=bucket_name, Key=file_key)
        print(f"File {file_key} exists in the bucket {bucket_name}.\n\n")
        return copy_path
    # except NoCredentialsError:
    #     print("AWS credentials are not available, or the bucket does not exist.")
    except Exception as e:
        print(f"File {file_key} does not exist in the bucket {bucket_name}.\n\n")
        return original_path

def delete_copy_file(sub_path: str, file_name: str) -> None:

    s3 = boto3.client('s3')
    bucket_name = s3_credentials.bucket_nm
    file = file_name.split(".")[0]
    delete_path = sub_path.replace(file, file + file_structure.COPY_FILE_SUFFIX)
    object_key = delete_path

    try:
        # Use the delete_object method to delete the object
        s3.delete_object(Bucket=bucket_name, Key=object_key)
        print(f"Object '{object_key}' deleted from '{bucket_name}'.")
    except Exception as e:
        print(f"Object deletion failed: {str(e)}")

def revert_operation(original_path: str, sub_path: str, file_name: str) -> None:

    file = file_name.split(".")[0]
    copy_path = sub_path.replace(file, file + file_structure.COPY_FILE_SUFFIX)

    s3 = boto3.client('s3')
    # Specify the source file and the destination path within the same bucket
    source_bucket = s3_credentials.bucket_nm
    source_key = copy_path
    destination_key_1 = original_path
    destination_key_2 = sub_path

    try:
        # Use the copy_object method to copy the file
        s3.copy_object(CopySource={'Bucket': source_bucket, 'Key': source_key}, Bucket=source_bucket, Key=destination_key_1)
        print(f"File copied from {source_key} to {destination_key_1} within the bucket {source_bucket}.")
    except Exception as e:
        print(f"File copy failed: {str(e)}")
    
    try:
        # Use the copy_object method to copy the file
        s3.copy_object(CopySource={'Bucket': source_bucket, 'Key': source_key}, Bucket=source_bucket, Key=destination_key_2)
        print(f"File copied from {source_key} to {destination_key_2} within the bucket {source_bucket}.")
    except Exception as e:
        print(f"File copy failed: {str(e)}")