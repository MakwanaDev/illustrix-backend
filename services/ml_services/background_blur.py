import cv2

from config.settings import file_structure, ml_constants
from services.file import save_to_sub_folder, fetch_image_from_url

def background_blur_fun(file_name: str, image_url: str, email:str) -> str:
    foreground = fetch_image_from_url(image_url)
    bg_path = file_structure.USER_DATA + email + file_structure.USER_BLURRED_BACKGROUND_PATH + image_url.split("/")[-1]
    original_img_path = image_url           
    background = fetch_image_from_url(original_img_path)
    background = cv2.resize(background, (foreground.shape[1], foreground.shape[0]))
    blurred_background = cv2.GaussianBlur(background, (ml_constants.BLUR_FACTOR, ml_constants.BLUR_FACTOR), 0)
    save_to_sub_folder(bg_path, blurred_background)
    return bg_path