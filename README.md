# 📸 Submission Klasifikasi Gambar
Proyek ini merupakan implementasi model klasifikasi gambar menggunakan TensorFlow dan Keras. Proyek ini dibuat sebagai bagian dari tugas akhir untuk pembelajaran Pengembangan Machine Learning.

## 🚀 Fitur
---
✅ **Klasifikasi Gambar**: Mengklasifikasikan gambar pakaian ke dalam 24 kategori berbeda 

✅ **Preprocessing Otomatis**: Termasuk augmentasi gambar (rotasi, flip horizontal, zoom, dst.) untuk meningkatkan generalisasi model.

✅ **Pelatihan Model CNN**: Menggunakan arsitektur CNN berbasis `Sequential` dengan `Conv2D` dan `Pooling` layer.

✅ **Evaluasi & Visualisasi**: Menampilkan grafik akurasi/loss, dan menghitung akurasi pada set data testing.

✅ **Konversi Model**: Menyimpan dan mengkonversi model ke format:
  - `SavedModel` 
  - `TensorFlow Lite` 
  - `TensorFlow Js`
  
✅ **Inference**: Prediksi 5 gambar acak dari data test menggunakan dua format model berbeda:
  - SavedModel (`TFSMLayer`)
  - TensorFlow Lite (`TFLite Interpreter`)
---

## Cara Menjalankan
---
👩‍💻 Menjalankan di Google Colab :
1. Buka notebook Google Colab:
> [https://colab.research.google.com/drive/1Fhqv-JXmWvHA2IewpiRDN1FpIskU7iE2?usp=sharing]
> Jika Ingin mengedit silahkan copy saja file colab nya ( jangan langsung menulis/mengubah kode di file colab tersebut)
2. Import library yang akan di gunakan dan upload file `kaggle.json` untuk mengunduh dataset dari Kaggle.
3. Jalankan sel-sel notebook secara berurutan mulai dari:
    - **Import Library**
    - **Load dataset**
    - **Split data**
    - **Augmentasi dan Preprocessing**
    - **Membangun dan Melatih Model**
    - **Evaluasi dan Visualisasi**
    - **Konversi ke SavedModel, TFLite, dan TF.js**
    - **Inference menggunakan SavedModel & TFLite**
4. Pastikan semua dependensi telah terinstal di environment Colab (Colab biasanya sudah siap pakai, tapi jika perlu install manual: `!pip install tensorflow tensorflowjs`).

👩‍💻 Clone repositori ini:
    git clone <https://github.com/Salsabilamm2/Proyek-Klasifikasi-Gambar>

👩‍💻 Akses file lengkap:
   GoogleDrive <https://drive.google.com/drive/folders/1MtoT2jTWR8suu2z8XiKKtzwroAN8mJbP?usp=drive_link>

---

## 📦 Dataset
---
- Nama Dataset : Apparel Images Dataset 
- Sumber : https://www.kaggle.com/datasets/trolukovich/apparel-images-dataset
- Jumlah Kelas: 24 kategori 
- Ukuran Gambar: Memiliki ukuran gambar awal yang bervariasi
- Dataset dibagi menjadi: 70% training, 20% validation, 10% testing
---

## 🧠 Model
---
- Arsitektur: Convolutional Neural Network (CNN) dengan Conv2D, MaxPooling2D, Dropout, dan Dense
- Optimasi: Adam, categorical_crossentropy, dan accuracy
- Callback: EarlyStopping, ModelCheckpoint
- Augmentasi: ImageDataGenerator dengan rotasi, zoom, flip, shift
---

## 📊 Hasil evaluasi model dan Visualisasi
---
- Akurasi Training: 91% 
- Akurasi Testing: 91%
- Visualisasi: Plot akurasi dan loss, prediksi gambar acak
---

## 💾 Format Model
---
Model dikonversi ke berbagai format untuk deployment:

✅ .Keras

✅ SavedModel

✅ TensorFlow Lite 

✅ TensorFlow.js
---

## 🔍 Inference
---
Inference dilakukan pada 5 gambar acak dari set test menggunakan:

✅ SavedModel (via TFSMLayer)

✅ TensorFlow Lite (via Interpreter)

Output: Gambar dengan label prediksi ditampilkan menggunakan matplotlib.
---

## 👩‍💻 Kontributor
---
- **Salsabila Mahiroh** 
---

## 📜 Lisensi
---
Proyek ini dilisensikan di bawah [jenis lisensi, misalnya MIT License]. Lihat file `LICENSE` untuk informasi lebih lanjut.
---
