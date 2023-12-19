from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from schemas.image import Response
from config.settings import constants
from services.file import get_file_path_from_url
# from services.db import connect_mongo_db, insert_or_update_user_image, get_user_images_by_email
from services.db import DatabaseConnector, insert_or_update_user_image, get_user_images_by_email
from services.auth import get_jwt_token, check_jwt_token, get_user_data_by_jwt
from services.ml_services.background_remove import background_remove_fun
from services.ml_services.self_background_blur import self_background_blur_fun
from services.ml_services.flip_vertically import flip_vertically_fun
from services.ml_services.flip_horizontally import flip_horizontally_fun
from services.ml_services.black_and_white import black_and_white_fun
from services.ml_services.saturation import saturation_fun
from services.ml_services.hue import hue_fun
from services.ml_services.contrast import contrast_fun
from services.ml_services.brightness import brightness_fun
from services.ml_services.sharpness import sharpness_fun
from services.ml_services.background_replace import background_replace_fun
from services.ml_services.painting import painting_fun
from services.ml_services.sketching import sketching_fun
from services.ml_services.cartoonification import cartoonification_fun
from services.ml_services.image_super_resolution import image_super_resolution_fun
from services.file import upload_image
from services.file import generate_presigned_url

router = APIRouter()

# connect_mongo_db()
db_connector = DatabaseConnector()

@router.post("/upload")
async def upload(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        jwt_token = get_jwt_token(request)
        validate_jwt_token = check_jwt_token(jwt_token)
        if validate_jwt_token == 100:
            user_details = get_user_data_by_jwt(jwt_token)
            # print('HELLLLLLLLLLLLLO33333333333333')
            global_url, file_name = upload_image(email = user_details["email"], base_64_string = body["image"])
            insert_or_update_user_image(file_name = file_name, email = user_details["email"], url = global_url)
            # print('HELLLLLLLLLLLLLO444444444444444')
            response = Response()
            response.message = constants.SUCCESSFULLY_PERFORMED
            response.url = global_url
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
        elif validate_jwt_token == 101 or validate_jwt_token == 102:
            response = Response()
            response.message = constants.INVALID_LOGIN
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = Response()
        response.message = constants.ERROR
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))
    

@router.post("/background_remove")
async def background_remove(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        jwt_token = get_jwt_token(request)
        validate_jwt_token = check_jwt_token(jwt_token)
        if validate_jwt_token == 100:
            user_details = get_user_data_by_jwt(jwt_token)
            file_name, system_file_path, global_url, background_url, factor, save, revert = get_file_path_from_url(body)
            bg_remove = background_remove_fun(file_name, global_url, user_details['email'])
            insert_or_update_user_image(file_name = file_name, email = user_details["email"], url = global_url)
            response = Response()
            response.message = constants.SUCCESSFULLY_PERFORMED
            response.url = global_url
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
        elif validate_jwt_token == 101 or validate_jwt_token == 102:
            response = Response()
            response.message = constants.INVALID_LOGIN
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = Response()
        response.message = constants.ERROR
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))

@router.post("/background_blur")
async def background_blur(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        jwt_token = get_jwt_token(request)
        validate_jwt_token = check_jwt_token(jwt_token)
        print(validate_jwt_token)
        if validate_jwt_token == 100:
            user_details = get_user_data_by_jwt(jwt_token)
            file_name, system_file_path, global_url, background_url, factor, save, revert = get_file_path_from_url(body)
            bg_remove_and_blur = self_background_blur_fun(file_name, global_url, user_details['email'])
            insert_or_update_user_image(file_name = file_name, email = user_details["email"], url = global_url)
            response = Response()
            response.message = constants.SUCCESSFULLY_PERFORMED
            response.url = global_url
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
        elif validate_jwt_token == 101 or validate_jwt_token == 102:
            response = Response()
            response.message = constants.INVALID_LOGIN
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = Response()
        response.message = constants.ERROR
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))

@router.post("/background_replace")
async def background_replace(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        jwt_token = get_jwt_token(request)
        validate_jwt_token = check_jwt_token(jwt_token)
        print(validate_jwt_token)
        if validate_jwt_token == 100:
            user_details = get_user_data_by_jwt(jwt_token)
            file_name, system_file_path, global_url, background_path, factor, save, revert = get_file_path_from_url(body, user_details['email'])
            bg_replace = background_replace_fun(file_name, global_url, background_path, user_details['email'])
            insert_or_update_user_image(file_name = file_name, email = user_details["email"], url = global_url)
            response = Response()
            response.message = constants.SUCCESSFULLY_PERFORMED
            response.url = global_url
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
        elif validate_jwt_token == 101 or validate_jwt_token == 102:
            response = Response()
            response.message = constants.INVALID_LOGIN
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = Response()
        response.message = constants.ERROR
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))

@router.post("/flip_vertically")
async def flip_vertically(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        jwt_token = get_jwt_token(request)
        validate_jwt_token = check_jwt_token(jwt_token)
        print(validate_jwt_token)
        if validate_jwt_token == 100:
            user_details = get_user_data_by_jwt(jwt_token)
            file_name, system_file_path, global_url, background_path, factor, save, revert = get_file_path_from_url(body, email=user_details['email'])
            fliped_image = flip_vertically_fun(file_name = file_name, system_file_path = system_file_path)
            insert_or_update_user_image(file_name = file_name, email = user_details["email"], url = global_url)
            response = Response()
            response.message = constants.SUCCESSFULLY_PERFORMED
            response.url = global_url
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
        elif validate_jwt_token == 101 or validate_jwt_token == 102:
            response = Response()
            response.message = constants.INVALID_LOGIN
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = Response()
        response.message = constants.ERROR
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))

@router.post("/flip_horizontally")
async def flip_horizontally(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        jwt_token = get_jwt_token(request)
        validate_jwt_token = check_jwt_token(jwt_token)
        print(validate_jwt_token)
        if validate_jwt_token == 100:
            user_details = get_user_data_by_jwt(jwt_token)
            file_name, system_file_path, global_url, background_path, factor, save, revert = get_file_path_from_url(body, email=user_details['email'])
            fliped_image = flip_horizontally_fun(file_name = file_name, system_file_path = system_file_path)
            insert_or_update_user_image(file_name = file_name, email = user_details["email"], url = global_url)
            response = Response()
            response.message = constants.SUCCESSFULLY_PERFORMED
            response.url = global_url
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
        elif validate_jwt_token == 101 or validate_jwt_token == 102:
            response = Response()
            response.message = constants.INVALID_LOGIN
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = Response()
        response.message = constants.ERROR
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))

@router.post("/black_and_white")
async def black_and_white(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        jwt_token = get_jwt_token(request)
        validate_jwt_token = check_jwt_token(jwt_token)
        print(validate_jwt_token)
        if validate_jwt_token == 100:
            user_details = get_user_data_by_jwt(jwt_token)
            file_name, system_file_path, global_url, background_path, factor, save, revert = get_file_path_from_url(body, email=user_details['email'])
            fliped_image = black_and_white_fun(file_name = file_name, system_file_path = system_file_path, save = save, revert = revert, email=user_details['email'])
            insert_or_update_user_image(file_name = file_name, email = user_details["email"], url = global_url)
            response = Response()
            response.message = constants.SUCCESSFULLY_PERFORMED
            response.url = global_url
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
        elif validate_jwt_token == 101 or validate_jwt_token == 102:
            response = Response()
            response.message = constants.INVALID_LOGIN
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = Response()
        response.message = constants.ERROR
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))

@router.post("/saturation")
async def saturation(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        jwt_token = get_jwt_token(request)
        validate_jwt_token = check_jwt_token(jwt_token)
        print(validate_jwt_token)
        if validate_jwt_token == 100:
            user_details = get_user_data_by_jwt(jwt_token)
            file_name, system_file_path, global_url, background_path, factor, save, revert = get_file_path_from_url(body, email=user_details['email'])
            saturated_image = saturation_fun(file_name = file_name, system_file_path = system_file_path, factor = factor, save = save, revert = revert, email=user_details['email'])
            insert_or_update_user_image(file_name = file_name, email = user_details["email"], url = global_url)
            response = Response()
            response.message = constants.SUCCESSFULLY_PERFORMED
            response.url = global_url
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
        elif validate_jwt_token == 101 or validate_jwt_token == 102:
            response = Response()
            response.message = constants.INVALID_LOGIN
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = Response()
        response.message = constants.ERROR
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))

@router.post("/hue")
async def hue(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        jwt_token = get_jwt_token(request)
        validate_jwt_token = check_jwt_token(jwt_token)
        print(validate_jwt_token)
        if validate_jwt_token == 100:
            user_details = get_user_data_by_jwt(jwt_token)
            file_name, system_file_path, global_url, background_path, factor, save, revert = get_file_path_from_url(body, email=user_details['email'])
            hue_image = hue_fun(file_name = file_name, system_file_path = system_file_path, factor = factor, save = save, revert = revert, email=user_details['email'])
            insert_or_update_user_image(file_name = file_name, email = user_details["email"], url = global_url)
            response = Response()
            response.message = constants.SUCCESSFULLY_PERFORMED
            response.url = global_url
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
        elif validate_jwt_token == 101 or validate_jwt_token == 102:
            response = Response()
            response.message = constants.INVALID_LOGIN
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = Response()
        response.message = constants.ERROR
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))

@router.post("/contrast")
async def contrast(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        jwt_token = get_jwt_token(request)
        validate_jwt_token = check_jwt_token(jwt_token)
        print(validate_jwt_token)
        if validate_jwt_token == 100:
            user_details = get_user_data_by_jwt(jwt_token)
            file_name, system_file_path, global_url, background_path, factor, save, revert = get_file_path_from_url(body, email=user_details['email'])
            contrasted_image = contrast_fun(file_name = file_name, system_file_path = system_file_path, factor = factor, save = save, revert = revert, email=user_details['email'])
            insert_or_update_user_image(file_name = file_name, email = user_details["email"], url = global_url)
            response = Response()
            response.message = constants.SUCCESSFULLY_PERFORMED
            response.url = global_url
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
        elif validate_jwt_token == 101 or validate_jwt_token == 102:
            response = Response()
            response.message = constants.INVALID_LOGIN
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = Response()
        response.message = constants.ERROR
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))

@router.post("/brightness")
async def brightness(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        jwt_token = get_jwt_token(request)
        validate_jwt_token = check_jwt_token(jwt_token)
        print(validate_jwt_token)
        if validate_jwt_token == 100:
            user_details = get_user_data_by_jwt(jwt_token)
            file_name, system_file_path, global_url, background_path, factor, save, revert = get_file_path_from_url(body, email=user_details['email'])
            brightness_image = brightness_fun(file_name = file_name, system_file_path = system_file_path, factor = factor, save = save, revert = revert, email=user_details['email'])
            insert_or_update_user_image(file_name = file_name, email = user_details["email"], url = global_url)
            response = Response()
            response.message = constants.SUCCESSFULLY_PERFORMED
            response.url = global_url
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
        elif validate_jwt_token == 101 or validate_jwt_token == 102:
            response = Response()
            response.message = constants.INVALID_LOGIN
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = Response()
        response.message = constants.ERROR
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))

@router.post("/sharpness")
async def sharpness(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        jwt_token = get_jwt_token(request)
        validate_jwt_token = check_jwt_token(jwt_token)
        print(validate_jwt_token)
        if validate_jwt_token == 100:
            user_details = get_user_data_by_jwt(jwt_token)
            file_name, system_file_path, global_url, background_path, factor, save, revert = get_file_path_from_url(body, email=user_details['email'])
            sharpness_image = sharpness_fun(file_name = file_name, system_file_path = system_file_path, factor = factor, save = save, revert = revert, email= user_details['email'])
            insert_or_update_user_image(file_name = file_name, email = user_details["email"], url = global_url)
            response = Response()
            response.message = constants.SUCCESSFULLY_PERFORMED
            response.url = global_url
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
        elif validate_jwt_token == 101 or validate_jwt_token == 102:
            response = Response()
            response.message = constants.INVALID_LOGIN
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = Response()
        response.message = constants.ERROR
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))

@router.post("/painting")
async def painting(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        jwt_token = get_jwt_token(request)
        validate_jwt_token = check_jwt_token(jwt_token)
        print(validate_jwt_token)
        if validate_jwt_token == 100:
            user_details = get_user_data_by_jwt(jwt_token)
            file_name, system_file_path, global_url, background_path, factor, save, revert = get_file_path_from_url(body, email=user_details['email'])
            painting_image = painting_fun(file_name = file_name, system_file_path = system_file_path, factor = factor, save = save, revert = revert, email=user_details['email'])
            insert_or_update_user_image(file_name = file_name, email = user_details["email"], url = global_url)
            response = Response()
            response.message = constants.SUCCESSFULLY_PERFORMED
            response.url = global_url
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
        elif validate_jwt_token == 101 or validate_jwt_token == 102:
            response = Response()
            response.message = constants.INVALID_LOGIN
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = Response()
        response.message = constants.ERROR
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))

@router.post("/sketching")
async def sketching(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        jwt_token = get_jwt_token(request)
        validate_jwt_token = check_jwt_token(jwt_token)
        print(validate_jwt_token)
        if validate_jwt_token == 100:
            user_details = get_user_data_by_jwt(jwt_token)
            file_name, system_file_path, global_url, background_path, factor, save, revert = get_file_path_from_url(body, email=user_details['email'])
            sketching_image = sketching_fun(file_name = file_name, system_file_path = system_file_path, factor = factor, save = save, revert = revert, email=user_details['email'])
            insert_or_update_user_image(file_name = file_name, email = user_details["email"], url = global_url)
            response = Response()
            response.message = constants.SUCCESSFULLY_PERFORMED
            response.url = global_url
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
        elif validate_jwt_token == 101 or validate_jwt_token == 102:
            response = Response()
            response.message = constants.INVALID_LOGIN
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = Response()
        response.message = constants.ERROR
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))

@router.post("/cartoonification")
async def cartoonification(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        jwt_token = get_jwt_token(request)
        validate_jwt_token = check_jwt_token(jwt_token)
        print(validate_jwt_token)
        if validate_jwt_token == 100:
            user_details = get_user_data_by_jwt(jwt_token)
            file_name, system_file_path, global_url, background_path, factor, save, revert = get_file_path_from_url(body, email=user_details['email'])
            cartoonification_image = cartoonification_fun(file_name = file_name, system_file_path = system_file_path, factor = factor, save = save, revert = revert, email = user_details['email'])
            insert_or_update_user_image(file_name = file_name, email = user_details["email"], url = global_url)
            response = Response()
            response.message = constants.SUCCESSFULLY_PERFORMED
            response.url = global_url
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
        elif validate_jwt_token == 101 or validate_jwt_token == 102:
            response = Response()
            response.message = constants.INVALID_LOGIN
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = Response()
        response.message = constants.ERROR
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))

@router.post("/image_super_resolution")
async def image_super_resolution(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        jwt_token = get_jwt_token(request)
        validate_jwt_token = check_jwt_token(jwt_token)
        print(validate_jwt_token)
        if validate_jwt_token == 100:
            user_details = get_user_data_by_jwt(jwt_token)
            file_name, system_file_path, global_url, background_path, factor, save, revert = get_file_path_from_url(body, email=user_details['email'])
            super_resolution_image = image_super_resolution_fun(file_name = file_name, system_file_path=system_file_path, email= user_details['email'])
            insert_or_update_user_image(file_name = file_name, email = user_details["email"], url = global_url)
            response = Response()
            response.message = constants.SUCCESSFULLY_PERFORMED
            response.url = global_url
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
        elif validate_jwt_token == 101 or validate_jwt_token == 102:
            response = Response()
            response.message = constants.INVALID_LOGIN
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = Response()
        response.message = constants.ERROR
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))

@router.get("/get_user_images")
async def get_user_images(request: Request) -> JSONResponse:
    try:
        jwt_token = get_jwt_token(request)
        validate_jwt_token = check_jwt_token(jwt_token)
        print(validate_jwt_token)
        if validate_jwt_token == 100:
            user_details = get_user_data_by_jwt(jwt_token)
            global_url = get_user_images_by_email(email = user_details["email"])
            response = Response()
            response.message = constants.SUCCESSFULLY_PERFORMED
            response.url = global_url
            return JSONResponse(status_code=status.HTTP_200_OK, content=response.dict(exclude_none=True))
        elif validate_jwt_token == 101 or validate_jwt_token == 102:
            response = Response()
            response.message = constants.INVALID_LOGIN
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.dict(exclude_none=True))
    except Exception as e:
        print(e)
        response = Response()
        response.message = constants.ERROR
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.dict(exclude_none=True))