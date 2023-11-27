import cv2

from services.ml_services.background_remove import background_remove_fun
from services.ml_services.background_blur import background_blur_fun
from services.ml_services.merge_two_images import merge_two_images_fun
from services.file import save_to_final_folder, fetch_image_from_url, generate_presigned_url
from config.settings import file_structure

def self_background_blur_fun(file_name: str, system_file_path: str, email: str) -> str:
    blurred_bg_path = background_blur_fun(file_name = file_name, image_url= system_file_path, email=email)
    blurred_bg_url = generate_presigned_url(blurred_bg_path)
    bg_remove_path = background_remove_fun(file_name = file_name, image_url= system_file_path, email=email)
    bg_remove_url = generate_presigned_url(bg_remove_path)
    combined_image_path = merge_two_images_fun(foregrond_image_url = bg_remove_url, background_image_url = blurred_bg_url, image_url= system_file_path, email=email)
    combined_image_url = generate_presigned_url(combined_image_path)
    combined_image = fetch_image_from_url(combined_image_url)
    final_folder_path = file_structure.USER_DATA + email + file_structure.FINAL_IMAGE_PATH + system_file_path.split("/")[-1]
    save_to_final_folder(final_folder_path, combined_image)
    return system_file_path