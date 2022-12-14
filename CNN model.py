import os
import cv2 as cv
import numpy as np
import tensorflow as tf
from keras.utils import to_categorical
from tensorflow import keras
from keras.layers.convolutional import Conv2D
from keras.layers import Dense
from keras.layers.convolutional import MaxPooling2D
from keras.layers import Flatten

# Loading Train Data
print("Train Data Loading ...")
img_train_path = r'Train'
train_data = []
train_label_names = []
for directory in os.listdir(img_train_path):
    for file in os.listdir(os.path.join(img_train_path, directory)):
        image_path = os.path.join(img_train_path, directory, file)
        image = cv.imread(image_path, 0)
        image = np.array(image)
        image = image.astype('float32')
        image /= 255  # Normalization
        train_data.append(image)
        train_label_names.append(directory)

target_dict = {k: v for v, k in enumerate(np.unique(train_label_names))}
train_label = [target_dict[train_label_names[i]] for i in range(len(train_label_names))]

row = len(train_data)
height = len(train_data[0])
width = len(train_data[1])
print(f'Images:{row}, height:{height}, width:{width}')
print("training data shape:", np.shape(train_data))

train_label = to_categorical(train_label)
print(f'training label shape :{np.shape(train_label)}')

# Loading Test Data
print("\nTest Data Loading ...")
img_test_path = r'Test'
test_data = []
test_label_names = []
for directory in os.listdir(img_test_path):
    for file in os.listdir(os.path.join(img_test_path, directory)):
        image_path = os.path.join(img_test_path, directory, file)
        image = cv.imread(image_path, 0)
        image = np.array(image)
        image = image.astype('float32')  # Convert dataType into float because later we will with values between [0-1]
        image /= 255  # Normalization
        test_data.append(image)
        test_label_names.append(directory)


target_dict = {k: v for v, k in enumerate(np.unique(test_label_names))}
test_label = [target_dict[test_label_names[i]] for i in range(len(test_label_names))]
row = len(test_data)
height = len(test_data[0])
width = len(test_data[1])
print(f'Images:{row}, height:{height}, width:{width}')
print("Shape of a list:", np.shape(test_data))


test_label = to_categorical(test_label)
print(f'training label shape :{np.shape(test_label)}')

# Expanding the dimension
print("\nExpanding data ...")
# Reshape training images in 3 dimensions (height = 32px, width = 32p , chanel =(GrayScale))
train_data = np.reshape(train_data, [-1, 32, 32, 1])
print("training data shape after Expanding the dimension:", np.shape(train_data))
# Reshape testing images in 3 dimensions (height = 32px, width = 32p , chanel =(GrayScale))
test_data = np.reshape(test_data, [-1, 32, 32, 1])
print("test data shape after Expanding the dimension:", np.shape(test_data))

# Creating model
print("\nCreating a model ...")

model = keras.Sequential([
    Conv2D(32, 3, padding="same", activation="relu", input_shape=(32, 32, 1)),
    MaxPooling2D(2, 2),
    Conv2D(64, 3, padding="same", activation="relu"),
    MaxPooling2D(2, 2),
    Conv2D(128, 3, padding="same", activation="relu"),
    MaxPooling2D(2, 2),
    Conv2D(64, 3, padding="same", activation="relu"),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(256, activation="relu"),
    Dense(28, activation="softmax")
])

print(model.summary())
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(train_data, train_label, epochs=30, validation_data=(test_data, test_label))
# save the weights
print("\nSaving the model...")
model.save('Models/first_model.h5')