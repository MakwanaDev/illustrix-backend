# import cv2
# TODO: Change to Opencv
import cv2 
import numpy as np

from services.file import save_to_final_folder, save_to_sub_folder, create_copy_image, check_copy_file_exist, delete_copy_file, revert_operation, generate_presigned_url, fetch_image_from_url
from config.settings import file_structure, ml_constants

def painting_fun(file_name: str, system_file_path: str, factor: int, save: int, revert: int, email:str) -> str:
    try:
        painting_path = file_structure.USER_DATA + email + file_structure.PAINTING_PATH + system_file_path.split("/")[-1]
        operation_file_path = check_copy_file_exist(original_path = system_file_path, sub_path = painting_path, file_name = file_name)
        operation_file_url = generate_presigned_url(operation_file_path)
        image = fetch_image_from_url(operation_file_url)
        image_clear = cv2.medianBlur(image, factor)
        image_clear = cv2.medianBlur(image_clear, factor)
        image_clear = cv2.medianBlur(image_clear, factor)
        image_clear = cv2.edgePreservingFilter(image_clear, sigma_s=10)
        image_filter = cv2.bilateralFilter(image_clear, 3, 10, 5)
        for _ in range(2):
            image_filter = cv2.bilateralFilter(image_clear, 3, 20, 10)
        for _ in range(3):
            image_filter = cv2.bilateralFilter(image_clear, 5, 30, 10)
        for _ in range(3):
            image_filter = cv2.bilateralFilter(image_clear, 5, 40, 10)
        gaussian_mask = cv2.GaussianBlur(image_filter, (9,9), 3)
        painted_image = cv2.addWeighted(image_filter, 1.5, gaussian_mask, -0.5, 0)
        painted_image = cv2.addWeighted(painted_image, ml_constants.SHAPRNESS_FACTOR, gaussian_mask, -(ml_constants.SHAPRNESS_FACTOR-1), 10)
        if operation_file_path == system_file_path:
            create_copy_image(from_path = system_file_path, to_path = painting_path, file_name = file_name)
        save_to_sub_folder(painting_path, painted_image)
        save_to_final_folder(system_file_path, painted_image)
        if save == 1:
            delete_copy_file(sub_path = painting_path, file_name = file_name)
        if revert == 1:
            revert_operation(original_path = system_file_path, sub_path = painting_path, file_name = file_name)
        return system_file_path
    except Exception as e:
        print(e)
        print(e.__traceback__.tb_lineno)