# import cv2
# TODO: Change to Opencv
from PIL import Image
import pilgram
import numpy as np
import cv2

from services.file import save_to_final_folder, save_to_sub_folder, create_copy_image, check_copy_file_exist, delete_copy_file, revert_operation, generate_presigned_url, fetch_image_from_url
from config.settings import file_structure

def hue_fun(file_name: str, system_file_path: str, factor: int, save: int, revert: int, email:str) -> str:
    hue_path = file_structure.USER_DATA + email + file_structure.HUE_PATH + system_file_path.split("/")[-1]
    operation_file_path = check_copy_file_exist(original_path = system_file_path, sub_path = hue_path, file_name = file_name)
    operation_file_url = generate_presigned_url(operation_file_path)
    image = fetch_image_from_url(operation_file_url, pillow=True)
    hue_image = pilgram.css.hue_rotate(image, factor)
    hue_image = np.array(hue_image)
    hue_image = cv2.cvtColor(hue_image, cv2.COLOR_BGR2RGB)
    if operation_file_path == system_file_path:
        create_copy_image(from_path = system_file_path, to_path = hue_path, file_name = file_name)
    save_to_sub_folder(hue_path, hue_image)
    save_to_final_folder(system_file_path, hue_image)
    if save == 1:
        delete_copy_file(sub_path = hue_path, file_name = file_name)
    if revert == 1:
        revert_operation(original_path = system_file_path, sub_path = hue_path, file_name = file_name)
    return system_file_path