# import cv2
# TODO: Change to Opencv
from PIL import Image, ImageEnhance
import numpy as np
import cv2

from services.file import save_to_final_folder, save_to_sub_folder, create_copy_image, check_copy_file_exist, delete_copy_file, revert_operation, generate_presigned_url, fetch_image_from_url
from config.settings import file_structure

def contrast_fun(file_name: str, system_file_path: str, factor: int, save: int, revert: int, email:str) -> str:
    contrast_path = file_structure.USER_DATA + email + file_structure.CONTRAST_PATH + system_file_path.split("/")[-1]
    operation_file_path = check_copy_file_exist(original_path = system_file_path, sub_path = contrast_path, file_name = file_name)
    operation_file_url = generate_presigned_url(operation_file_path)
    image = fetch_image_from_url(operation_file_url, pillow=True)
    enhancer = ImageEnhance.Contrast(image)
    contrasted_image = enhancer.enhance(factor)
    contrasted_image = np.array(contrasted_image)
    contrasted_image = cv2.cvtColor(contrasted_image, cv2.COLOR_BGR2RGB)
    if operation_file_path == system_file_path:
        create_copy_image(from_path = system_file_path, to_path = contrast_path, file_name = file_name)
    save_to_sub_folder(contrast_path, contrasted_image)
    save_to_final_folder(system_file_path, contrasted_image)
    if save == 1:
        delete_copy_file(sub_path = contrast_path, file_name = file_name)
    if revert == 1:
        revert_operation(original_path = system_file_path, sub_path = contrast_path, file_name = file_name)
    return system_file_path