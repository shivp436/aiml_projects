import base64
import numpy as np
import cv2
import pywt
import joblib
import json


__dir_names = None
__svc = None

def load_artifacts():
    global __svc
    global __dir_names
    
    print("Loading artifacts...")
    if __svc is None:
        __svc = joblib.load('./artifacts/model.pkl')
    
    if __dir_names is None:
        with open("./artifacts/class_dict.json", "r") as f:
            __dir_names = json.load(f)

    print("Artifacts loaded successfully!")

def w2d(img, mode='haar', level=1):
    imArray = img
    #Datatype conversions
    #convert to grayscale
    imArray = cv2.cvtColor(imArray,cv2.COLOR_RGB2GRAY)
    #convert to float and normalize
    imArray = np.float32(imArray)
    imArray /= 255
    # compute coefficients
    coeffs=pywt.wavedec2(imArray, mode, level=level)

    # preprocess coeffs
    coeffs_H=list(coeffs)
    coeffs_H[0] *= 0

    # reconstruction
    imArray_H=pywt.waverec2(coeffs_H, mode);
    imArray_H *= 255;
    imArray_H =  np.uint8(imArray_H)

    return imArray_H

def predict_class(img_path=None, base64_str=None):
    global __svc
    global __dir_names
    # read image
    if img_path:
        img = cv2.imread(img_path)
    elif base64_str:
        # Decode the base64 string into bytes
        decoded_data = base64.b64decode(base64_str)
        # Convert bytes to NumPy array
        np_data = np.frombuffer(decoded_data, np.uint8)
        # Decode the NumPy array into an image
        img = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
    img = cv2.resize(img, (256, 256))

    # wavelet transform
    img_har = w2d(img, 'db1', 5)
    img_har = cv2.resize(img_har, (256, 256))

    # combine image
    combined_img = np.vstack((img.reshape(256*256*3,1),img_har.reshape(256*256,1)))

    # predict class
    if __svc is None:
        load_artifacts()
    prediction = __svc.predict(combined_img.reshape(1,-1))
    print(prediction)
    return __dir_names[prediction[0]]