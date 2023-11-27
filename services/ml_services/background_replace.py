import cv2

from services.ml_services.background_remove import background_remove_fun
from services.ml_services.merge_two_images import merge_two_images_fun
from services.file import save_to_final_folder, generate_presigned_url, fetch_image_from_url
from config.settings import file_structure

def background_replace_fun(file_name: str, image_url: str, background_path: str, email:str) -> str:
    background_url = generate_presigned_url(background_path)
    bg_remove = background_remove_fun(file_name = file_name, image_url = image_url, email=email)
    bg_remove_url = generate_presigned_url(bg_remove)
    combined_image_path = merge_two_images_fun(foregrond_image_url= bg_remove_url, background_image_url= background_url, image_url= image_url, email=email)
    combined_image_url = generate_presigned_url(combined_image_path)
    combined_image = fetch_image_from_url(combined_image_url)
    final_folder_path = file_structure.USER_DATA + email + file_structure.FINAL_IMAGE_PATH + image_url.split("/")[-1]
    save_to_final_folder(final_folder_path, combined_image)
    return final_folder_path