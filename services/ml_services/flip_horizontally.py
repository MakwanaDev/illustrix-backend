import cv2

from services.file import save_to_final_folder, save_to_sub_folder, generate_presigned_url, fetch_image_from_url
from config.settings import file_structure

def flip_horizontally_fun(file_name: str, system_file_path: str) -> str:
    operation_file_url = generate_presigned_url(system_file_path)
    image = fetch_image_from_url(operation_file_url)
    flipped_image = cv2.flip(image, 1)
    flipped_horizontally_path = file_structure.USER_DATA + system_file_path.split("/")[3] + file_structure.FLIP_HORIZONTAL_PATH + system_file_path.split("/")[-1]
    save_to_sub_folder(flipped_horizontally_path, flipped_image)
    save_to_final_folder(system_file_path, flipped_image)
    return system_file_path