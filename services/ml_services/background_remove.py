import numpy as np
import cv2
import requests
import json
import ast
from services.file import save_to_final_folder, save_to_sub_folder, generate_presigned_url
from config.settings import file_structure
import requests
from PIL import Image
from io import BytesIO
import io
from dotenv import load_dotenv
import os

load_dotenv()
class SimilarBufferedReader:
    def __init__(self, bytes_io):
        self.bytes_io = bytes_io

    def read(self, size=-1):
        return self.bytes_io.read(size)


def background_remove_fun(file_name: str, image_url: str, email: str) -> str:
    try:
        import tensorflow as tf
        from tensorflow.keras.models import Model
        graph = tf.Graph()
        with graph.as_default():
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = response.content
                image_buffer = io.BytesIO(image_data)
                buffered_image = SimilarBufferedReader(image_buffer)

            url = os.getenv('BR_API')
            name = image_url.split('/')[-1]
            files1 = {'file': (f'{name}', buffered_image, 'image/png')}
            
            response = requests.post(url, files=files1)
            img_arr = ast.literal_eval(response.json()['image_data'])
            transperant_image = np.array(img_arr, dtype=np.uint8)

            bg_remove_path = file_structure.USER_DATA + email + file_structure.BACKGROUND_REMOVE_PATH + image_url.split("/")[-1]
            removed_bg_path = file_structure.USER_DATA + email + file_structure.USER_BACKGROUND_PATH + image_url.split("/")[-1]
            final_folder_path = file_structure.USER_DATA + email + file_structure.FINAL_IMAGE_PATH + image_url.split("/")[-1]

            original_image = image_data
            save_to_sub_folder(bg_remove_path, transperant_image)
            save_to_sub_folder(removed_bg_path, original_image)
            save_to_final_folder(final_folder_path, transperant_image)
            return final_folder_path
    except Exception as e:
        print(e)
        print(e.__traceback__.tb_lineno)