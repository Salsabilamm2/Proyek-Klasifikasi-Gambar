# -*- coding: utf-8 -*-
"""Submission Klasifikasi Gambar.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Fhqv-JXmWvHA2IewpiRDN1FpIskU7iE2

# Proyek Klasifikasi Gambar: Apparel Image Dataset
- **Nama:** Salsabila Mahiroh
- **Email:** Salsabilammm777@gmail.com
- **ID Dicoding:** salsabilammm

## Import Semua Packages/Library yang Digunakan
"""

import os
import shutil
import zipfile
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from keras.layers import TFSMLayer

"""## Data Preparation

### Data Loading
"""

# upload fie json
from google.colab import files
files.upload()

# unduh dan load dataset apparel
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json
!kaggle datasets download -d trolukovich/apparel-images-dataset

import zipfile
with zipfile.ZipFile("apparel-images-dataset.zip", 'r') as zip_ref:
    zip_ref.extractall("apparel_dataset")

# melihat jumlah citra dan ukuran resolusi
def print_images_resolution(directory):
    unique_sizes = set()
    total_images = 0

    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        image_files = os.listdir(subdir_path)
        num_images = len(image_files)
        print(f"{subdir}: {num_images}")
        total_images += num_images

        for img_file in image_files:
            img_path = os.path.join(subdir_path, img_file)
            with Image.open(img_path) as img:
                unique_sizes.add(img.size)

        for size in unique_sizes:
            print(f"- {size}")
        print("---------------")

    print(f"\nTotal: {total_images}")

# Memanggil fungsi direktori path 'apparel_dataset'
print_images_resolution("apparel_dataset")

"""**Catatan :**

- Dataset yang di gunakan adalah Apparel Image Dataset, yang memiliki total 11385 gambar, dengan jumlah 24 kelas di dalamnya
- Masing-masing gambar dalam dataset ini memiliki resolusi yang bervariasi atau beragam

### Data Preprocessing

#### Split Dataset
"""

# Cek isi folder dataset
base_dir = "apparel_dataset"
categories = os.listdir(base_dir)
print("Label kategori:", categories)

# melihat 3 gambar acak
# Set jumlah contoh per kelas
samples_per_class = 3

# Ukuran figure
plt.figure(figsize=(15, len(categories) * 3))

# Loop setiap kelas
for i, category in enumerate(categories):
    category_path = os.path.join(base_dir, category)
    images = os.listdir(category_path)

    # Ambil 3 gambar acak dari kelas tersebut
    selected_images = random.sample(images, samples_per_class)

    for j, img_name in enumerate(selected_images):
        img_path = os.path.join(category_path, img_name)
        img = mpimg.imread(img_path)

        plt.subplot(len(categories), samples_per_class, i * samples_per_class + j + 1)
        plt.imshow(img)
        plt.axis('off')
        if j == 1:
            plt.title(category, fontsize=12)

plt.tight_layout()
plt.show()

# Membuat folder untuk split data menjadi train, test, dan val
os.makedirs('apparel_split/train', exist_ok=True)
os.makedirs('apparel_split/val', exist_ok=True)
os.makedirs('apparel_split/test', exist_ok=True)

for category in categories:
    images = os.listdir(os.path.join(base_dir, category))
    random.shuffle(images)

    train_split = int(0.7 * len(images))
    val_split = int(0.9 * len(images))

    for phase, image_list in zip(['train', 'val', 'test'],
                                 [images[:train_split], images[train_split:val_split], images[val_split:]]):
        dest_dir = f'apparel_split/{phase}/{category}'
        os.makedirs(dest_dir, exist_ok=True)
        for img in image_list:
            src = os.path.join(base_dir, category, img)
            dst = os.path.join(dest_dir, img)
            shutil.copyfile(src, dst)

base_dir = 'apparel_dataset/apparel_images'
img_size = 128
batch_size = 32

# Data Augmentation & Preprocessing
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    width_shift_range=0.1,
    height_shift_range=0.1
)

val_test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    'apparel_split/train',
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='categorical'
)

val_generator = val_test_datagen.flow_from_directory(
    'apparel_split/val',
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='categorical'
)

test_generator = val_test_datagen.flow_from_directory(
    'apparel_split/test',
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='categorical'
)

"""**Catatan :**
- Dataset di bagi menjadi data training, data testing, dan data validasi dengan porsi :

**Training set:** 70%, **Validation set:** 20%, dan **Testing set:** 10%

## Modelling
"""

# pemodelan dengan model sequential, conv2d, dan pooling layer
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(img_size, img_size, 3)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dropout(0.5),
    Dense(512, activation='relu'),
    Dense(train_generator.num_classes, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

# Callback
callbacks = [
    EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True),
    ModelCheckpoint('best_model.keras', monitor='val_accuracy', save_best_only=True)
]

# Train model
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=50,
    callbacks=callbacks
)

"""## Evaluasi dan Visualisasi"""

# Setelah training selesai, dan load model terbaik dari .keras
model = tf.keras.models.load_model('best_model.keras')

test_loss, test_accuracy = model.evaluate(test_generator)

print(f'Test Loss: {test_loss}')
print(f'Test Accuracy: {test_accuracy}')

# Mengambil riwayat akurasi train dari objek history
train_accuracy = history.history['accuracy']

# Menampilkan akurasi train
print(f"Akurasi Train: {train_accuracy[-1] * 100:.2f}%")

# membuat dan melihat plot akurasi dan loss
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train')
plt.plot(history.history['val_accuracy'], label='Val')
plt.title("Accuracy")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train')
plt.plot(history.history['val_loss'], label='Val')
plt.title("Loss")
plt.legend()
plt.show()

"""## Konversi Model"""

# menyimpan ke format save model
model.export('saved_model/apparel_model')

# Simpan label ke file label.txt
labels = list(train_generator.class_indices.keys())
with open("label.txt", "w") as f:
    for label in labels:
        f.write(label + "\n")

# Konversi model ke format TFLite
import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_saved_model("saved_model/apparel_model")
tflite_model = converter.convert()

# Simpan model TFLite ke file
with open("model.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ Model berhasil dikonversi ke TensorFlow Lite.")

# Instal TensorFlow.js
!pip install tensorflowjs

# Buat folder untuk menyimpan model TFJS
!mkdir -p tfjs_model

# Konversi model dari SavedModel ke TFJS
!tensorflowjs_converter \
    --input_format=tf_saved_model \
    --output_format=tfjs_graph_model \
    saved_model/apparel_model tfjs_model

# Print pesan berhasil
print("✅ Model berhasil dikonversi ke TensorFlow.js.")

"""## Inference (Optional)

**Inference dengan Save Model**
"""

# Load model menggunakan TFSMLayer
model = TFSMLayer('saved_model/apparel_model', call_endpoint='serve')

# Load label
with open("label.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]

# Ambil 5 gambar acak dari test folder
test_folder = 'apparel_split/test'
all_classes = os.listdir(test_folder)
random_images = []

for _ in range(5):
    cls = random.choice(all_classes)
    img_file = random.choice(os.listdir(os.path.join(test_folder, cls)))
    img_path = os.path.join(test_folder, cls, img_file)
    random_images.append(img_path)

# Prediksi dan tampilkan
plt.figure(figsize=(15, 5))
for i, img_path in enumerate(random_images):
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = model(img_array)
    pred_label = labels[np.argmax(pred)]

    plt.subplot(1, 5, i+1)
    plt.imshow(img)
    plt.title(f"Pred: {pred_label}")
    plt.axis('off')

plt.tight_layout()
plt.show()

"""**Inference dengan TfLite**"""

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load label
with open("label.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]

# Ambil 5 gambar acak dari test folder
test_folder = 'apparel_split/test'
all_classes = os.listdir(test_folder)
random_images = []

for _ in range(5):
    cls = random.choice(all_classes)
    img_file = random.choice(os.listdir(os.path.join(test_folder, cls)))
    img_path = os.path.join(test_folder, cls, img_file)
    random_images.append(img_path)

# Prediksi dan tampilkan
plt.figure(figsize=(15, 5))
for i, img_path in enumerate(random_images):
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0).astype(np.float32)

    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    pred_label = labels[np.argmax(output)]

    plt.subplot(1, 5, i+1)
    plt.imshow(img)
    plt.title(f"Pred: {pred_label}")
    plt.axis('off')

plt.tight_layout()
plt.show()