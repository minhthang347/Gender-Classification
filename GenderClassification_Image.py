import numpy as np
import cv2
import cvlib as cv
import joblib
import argparse
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from extract_features import model as model_vgg

# model path
model_path = "C:/Users/ThangHuynh/Desktop/GenderDetection (vgg16 + svm)/train_model.pkl"

# load model
model = joblib.load(model_path)

# read input image
image = cv2.imread("sample_input.jpg")

if image is None:
    print("Could not read input image")
    exit()

# detect faces in the image
face, confidence = cv.detect_face(image)

classes = ['man', 'woman']

# loop through detected faces
for idx, f in enumerate(face):
    # get corner points of face rectangle
    (startX, startY) = f[0], f[1]
    (endX, endY) = f[2], f[3]

    # draw rectangle over face
    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)

    # crop the detected face region
    face_crop = np.copy(image[startY:endY, startX:endX])

    # preprocessing for gender detection model
    face_crop = cv2.resize(face_crop, (224, 224))
    face_crop = face_crop.astype("float") / 255.0
    face_crop = img_to_array(face_crop)
    face_crop = np.expand_dims(face_crop, axis=0)
    face_crop = model_vgg.predict(face_crop)

    # apply gender detection on face
    conf = model.predict(face_crop)
    print(conf)

    # get label with max accuracy
    idx = int(conf)
    label = classes[idx]

    #label = "{}: {:.2f}%".format(label, conf[idx] * 100)

    Y = startY - 10 if startY - 10 > 10 else startY + 10

    # write label and confidence above face rectangle
    cv2.putText(image, label, (startX, Y), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 2)

# display output
cv2.imshow("gender detection", image)

# press any key to close window
cv2.waitKey()

# save output
cv2.imwrite("gender_detection.jpg", image)

# release resources
cv2.destroyAllWindows()
