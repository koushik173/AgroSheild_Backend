from fastapi import FastAPI, File, UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

MODEL = tf.keras.models.load_model("../Working_CNN/models/1")
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

origins = [
    "http://localhost:3000",  # Replace with your React app's URL
    # Add more origins as needed
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/ping")
async def ping():
    return "Hello, I am alive too "

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
    
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = round(100*np.max(predictions[0]), 2)
    # print(predicted_class, confidence)
    
    return {
        "class": predicted_class, 
        "confidence": confidence
        }


if __name__== "__main__":
    uvicorn.run(app, host='localhost', port=8000)