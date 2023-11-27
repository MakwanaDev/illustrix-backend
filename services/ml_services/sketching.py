import cv2

from services.file import save_to_final_folder, save_to_sub_folder, create_copy_image, check_copy_file_exist, delete_copy_file, revert_operation, generate_presigned_url, fetch_image_from_url
from config.settings import file_structure

def dodgeV2(x, y):
    return cv2.divide(x, 255-y, scale=250)

def sketching_fun(file_name: str, system_file_path: str, factor: int, save: int, revert: int, email: str) -> str:
    sketching_path = file_structure.USER_DATA + email + file_structure.SKETCHING_PATH + system_file_path.split("/")[-1]
    operation_file_path = check_copy_file_exist(original_path = system_file_path, sub_path = sketching_path, file_name = file_name)
    operation_file_url = generate_presigned_url(operation_file_path)
    print('\n\nSystem file path : ', system_file_path)
    image = fetch_image_from_url(operation_file_url)
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_invert = cv2.bitwise_not(img_gray)
    img_smoothing = cv2.GaussianBlur(img_invert, (21,21), sigmaX=0, sigmaY=0)
    sketched_img = dodgeV2(img_gray, img_smoothing)
    if operation_file_path == system_file_path:
        create_copy_image(from_path = system_file_path, to_path = sketching_path, file_name = file_name)
    save_to_sub_folder(sketching_path, sketched_img)
    save_to_final_folder(system_file_path, sketched_img)
    if save == 1:
        delete_copy_file(sub_path = sketching_path, file_name = file_name)
    if revert == 1:
        revert_operation(original_path = system_file_path, sub_path = sketching_path, file_name = file_name)
    return system_file_path