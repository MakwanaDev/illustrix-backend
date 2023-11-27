import cv2
import tensorflow as tf
from tensorflow.keras.models import Model
from PIL import Image
from fastapi import FastAPI, File, UploadFile
import uvicorn
from fastapi.responses import JSONResponse
import numpy as np
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return 'Hello world.'

@app.post("/predicts")
async def predict(
        file: UploadFile = File(...)
):
    contents = await file.read()
    print(f"Received data: {contents[:50]}")
    nparr = np.frombuffer(contents, np.uint8)
    print('Hello world..')
    try:
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    except Exception as e:
        return {'error': f'Error decoding image : {str(e)}'}
    print('\n\n\n\nImage Type : \n\n================\n\n\n')
    print(type(image))

    print('\n\n\n\n================\n\n\n')
    print(image.shape)
    graph = tf.Graph()
    with graph.as_default():
        model = tf.keras.models.load_model('services/ml_services/models/unet_july_19.h5', compile=False)
        original_image = image
        h, w, _ = image.shape
        image = cv2.resize(image, (256, 256))
        image = image/255.0
        image = image.astype(np.float32)
        image = np.expand_dims(image, axis=0)
        pred_mask = model.predict(image)[0]
        pred_mask = cv2.resize(pred_mask, (w, h))
        pred_mask = np.expand_dims(pred_mask, axis=-1)
        pred_mask = pred_mask > 0.5
        background_mask = np.abs(1 - pred_mask)
        masked_image = original_image * pred_mask
        background_mask = np.concatenate(
            [background_mask, background_mask, background_mask], axis=-1)
        background_mask = background_mask * [0, 0, 0]
        #masked_image = masked_image + background_mask

        gray_image = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY)
        b, g, r = cv2.split(masked_image)
        rgba = [b, g, r, alpha]
        transperant_image = cv2.merge(rgba, 4)

        # Convert NumPy array to a list (JSON serializable)
        img_list = transperant_image.tolist()

        # Convert the list to a JSON-formatted string
        img_str = json.dumps(img_list)

        # with open('Img.txt', 'w') as tx:
        #     tx.write(img_str)

        response_data = {"image_data": img_str}
        return JSONResponse(content=response_data)


if __name__ == "__main__":  
    uvicorn.run(app, host='0.0.0.0', port=8100)
