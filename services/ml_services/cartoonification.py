import cv2
import numpy as np
import os

import tensorflow.compat.v1  as tf1
tf1.disable_eager_execution()

import services.ml_services.network as network
import services.ml_services.guided_filter as guided_filter


from services.file import save_to_final_folder, save_to_sub_folder, create_copy_image, check_copy_file_exist, delete_copy_file, revert_operation, fetch_image_from_url, generate_presigned_url
from config.settings import file_structure

input_photo = tf1.placeholder(tf1.float32, [1, None, None, 3])
network_out = network.unet_generator(input_photo)
final_out = guided_filter.guided_filter(input_photo, network_out, r=1, eps=5e-3)
all_vars = tf1.trainable_variables()
gene_vars = [var for var in all_vars if 'generator' in var.name]
saver = tf1.train.Saver(var_list=gene_vars)
config = tf1.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf1.Session(config=config)
sess.run(tf1.global_variables_initializer())
saver.restore(sess, tf1.train.latest_checkpoint(file_structure.CARTOONIFICATION_MODEL))

def resize_crop(image):
    h, w, c = np.shape(image)
    if min(h, w) > 720:
        if h > w:
            h, w = int(720*h/w), 720
        else:
            h, w = 720, int(720*w/h)
    image = cv2.resize(image, (w, h),
                       interpolation=cv2.INTER_AREA)
    h, w = (h//8)*8, (w//8)*8
    image = image[:h, :w, :]
    return image

def cartoonification_fun(file_name: str, system_file_path: str, factor: int, save: int, revert: int, email:str) -> str:
    cartoonification_path = file_structure.USER_DATA + email + file_structure.CARTOONNIFICATION_PATH + system_file_path.split("/")[-1]
    operation_file_path = check_copy_file_exist(original_path = system_file_path, sub_path = cartoonification_path, file_name = file_name)
    operation_file_url = generate_presigned_url(operation_file_path)
    image = fetch_image_from_url(operation_file_url)
    image = resize_crop(image)
    batch_image = image.astype(np.float32)/127.5 - 1
    batch_image = np.expand_dims(batch_image, axis=0)
    output = sess.run(final_out, feed_dict={input_photo: batch_image})
    output = (np.squeeze(output)+1)*127.5
    cartoonification_output = np.clip(output, 0, 255).astype(np.uint8)
    if operation_file_path == system_file_path:
        create_copy_image(from_path = system_file_path, to_path = cartoonification_path, file_name = file_name)
    save_to_sub_folder(cartoonification_path, cartoonification_output)
    save_to_final_folder(system_file_path, cartoonification_output)
    if save == 1:
        delete_copy_file(sub_path = cartoonification_path, file_name = file_name)
    if revert == 1:
        revert_operation(original_path = system_file_path, sub_path = cartoonification_path, file_name = file_name)
    return system_file_path