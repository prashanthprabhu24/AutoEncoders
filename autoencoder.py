# -*- coding: utf-8 -*-
"""AUTOEncoder.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1V09lXfLz3flqJXEBa2LmHUToZU3BZrQm

Date : 10/03/2022
Project : Autoencoder (Convolutional Autoencoder)
Author : Prashanth N
"""

# !unzip '/content/dataset.zip'

"""Steps : 
1. Get the dataset
2. Preprocess the dataset
3. Create the model
4. Train the model
5. Reconstruct the input data/ Show Output
6. Compare with the actual input
"""

# 1. Get the dataset 
import matplotlib.pyplot as plt
import os
import cv2

folder = '/content/dataset'
for i, image in enumerate(os.listdir(folder)):
  img = cv2.imread(folder+'/'+image,1)
  print('Original Input Image : ',i)
  plt.imshow(img)
  plt.show()
  print()

# 2. Pre-process the data
from keras.preprocessing.image import img_to_array
import numpy as np
import cv2

img_data = []
folder = '/content/dataset'
for i, image in enumerate(os.listdir(folder)):
  img = cv2.imread(folder+'/'+image,1)
  rgb_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
  rgb_img = cv2.resize(rgb_img,(256,256))
  img_data.append(img_to_array(rgb_img))
img_final = np.reshape(img_data,(len(img_data),256,256,3))
img_final = img_final.astype('float32')/255
print('Pre-Processed Input image : ')
for i in img_final:
  plt.imshow(i.reshape(256,256,3))
  plt.show()

# 3. Create the model
from keras.layers import Dense, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Sequential

# model = Sequential()#([inp,vsize], out)
model = Model(inp, out)
# Encoding
model = (Conv2D(64,(3,3), activation = 'relu', padding='same', input_shape=(256,256,3)))(model)
model.add(MaxPooling2D((2,2), padding='same'))
model.add(Conv2D(32, (3,3), activation='relu', padding='same'))
model.add(MaxPooling2D((2,2), padding='same'))
model.add(Conv2D(16, (3,3), activation='relu', padding='same'))
model.add(MaxPooling2D((2,2), padding='same'))

# Decoding
model.add(Conv2D(16, (3,3), activation='relu', padding='same'))
model.add(UpSampling2D((2,2)))
model.add(Conv2D(32, (3,3), activation='relu', padding='same'))
model.add(UpSampling2D((2,2)))
model.add(Conv2D(64, (3,3), activation='relu', padding='same'))
model.add(UpSampling2D((2,2)))
model.add(Conv2D(3, (3,3), activation='relu', padding='same'))

# Compiling
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
model.summary()

# 4. Train the model
import tensorflow as tf
tf.config.run_functions_eagerly(True)
model.fit(img_final, img_final, epochs = 10, shuffle=True)

# 5. Reconstruct the input data/ Show Output

pred = model.predict(img_final)
for i,j in enumerate(range(len(img_final))):
  print('Reconstructed Input Images(Output) : ', i)
  plt.imshow(pred[j].reshape(256,256,3))
  plt.show()
  print()

# 6. Compare with the actual input

for i,j in enumerate(range(len(img_final))):
  print('Input Image v/s Reconstructed Image : ', i)
  fig = plt.figure(figsize=(10,7))
  fig.add_subplot(1,2,1)
  plt.imshow(img_final[j].reshape(256,256,3))

  fig.add_subplot(1,2,2)
  plt.imshow(pred[j].reshape(256,256,3))
  plt.show()
  print()