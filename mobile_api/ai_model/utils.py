from tensorflow.keras.metrics import top_k_categorical_accuracy
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow import keras
from main.settings import BASE_DIR
import numpy as np
import os


def accuracy(y_true, y_pred, *args, **kwargs):
    return top_k_categorical_accuracy(y_true, y_pred, k=2)


model = load_model(os.path.join(BASE_DIR, "mobile_api/ai_model/Final_Model_final.keras"), custom_objects={"accuracy": accuracy})


def predict_cancer_disease(image_path):
    class_names = {
        0: "Actinic keratoses",
        1: "Basal cell carcinoma",
        2: "Benign keratosis-like lesions",
        3: "Dermatofibroma",
        4: "Melanocytic nevi",
        5: "Vascular lesions",
        6: "Melanoma",
    }
    
    # load image & preprocessing the image
    img = image.load_img(image_path, target_size=(28,28))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    
    
    predication = model.predict(img_array)
    predicated_class_index = np.argmax(predication)
    predicated_class_name = class_names.get(predicated_class_index)
    
    return predicated_class_name

