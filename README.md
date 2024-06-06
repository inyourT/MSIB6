# Web Application Sistem Diagnosis Penyakit Diabetes
Proyek ini bertujuan untuk mengembangkan sistem diagnosis diabetes berbasis machine learning yang dapat digunakan oleh tenaga medis dan masyarakat umum. Sistem ini menganalisis data kesehatan seperti kadar gula darah, riwayat keluarga, dan indeks massa tubuh (BMI) untuk mendeteksi diabetes secara dini. Dengan antarmuka yang ramah pengguna sistem ini memberikan hasil diagnosa yang cepat, memudahkan semua kalangan dalam memahami dan mengelola risiko diabetes. Implementasi sistem ini diharapkan dapat meningkatkan kesadaran, deteksi dini, dan pengelolaan diabetes secara efektif.

## Pemilihan Model
### Model yang Dipilih
Setelah melakukan eksperimen dengan berbagai model, kami memilih  **Support Vector Machine (SVM)** untuk optimasi dan perbandingan lebih lanjut, dengan akurasi training yaitu 78% dan akurasi testingnya 77%.  Proses pemilihan melibatkan evaluasi beberapa model termasuk Logistic Regression dengan akurasi 75%, Decision Tree dengan akurasi 75%, k-Nearest Neighbors dengan akurasi 69%, dan Random Forest dengan akurasi 76%. Sehingga dengan begitu model yang kami tuliskan hanya bagian SVMnya saja.

### Alasan Pemilihan Model SVM
- **Support Vector Machine (SVM)**:
  - **Karakteristik Data**: SVM efektif dalam ruang berdimensi tinggi dan sangat berguna ketika jumlah dimensi melebihi jumlah sampel. SVM juga fleksibel berkat penggunaan berbagai fungsi kernel yang dapat beradaptasi dengan kompleksitas data.
  - **Performa**: SVM menunjukkan hasil yang menjanjikan dalam pengujian awal dengan metrik klasifikasi yang baik, sehingga sangat penting untuk sistem diagnosis medis.

### Tuning Hyperparameter dan Hasil
#### Support Vector Machine (SVM)
- **Hyperparameter yang Di-tuning**:
  - `kernel`: Jenis fungsi kernel (misalnya, linear, poly, rbf).

- **Parameter Terbaik yang Ditemukan**:
  - `kernel`: 'linear'

- **Hasil**:
  - **Akurasi**: 0.78

### Pilihan Model Akhir
Berdasarkan metrik evaluasi dan persyaratan khusus sistem diagnosis diabetes, kami memilih **Support Vector Machine** dengan parameter yang dioptimalkan sebagai model akhir untuk di-deploy. Pilihan ini didasarkan pada akurasi yang lebih tinggi dan ketahanan terhadap overfitting, yang esensial untuk diagnosis yang andal.

## Instalasi dan Penggunaan
Untuk menjalankan aplikasi web, ikuti langkah-langkah berikut:

1. **Clone Repositori**:
   ```bash
   git clone https://github.com/anindayr/Capstone-Project.git
  
   ```

2. **Jalankan Aplikasi**:
   ```bash
   streamlit run stream-diabetes.py
   ```

3. **Akses Aplikasi Web**:
   Buka browser web Anda dan navigasi ke `http://localhost:8502`.

## Dataset

Dataset yang digunakan untuk melatih model berasal dari [UCI Machine Learning Repository]( https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database). Pastikan Anda memiliki dataset dalam format dan jalur yang benar sebelum menjalankan skrip pelatihan.

README ini memberikan gambaran menyeluruh tentang proyek, menjelaskan proses pemilihan model, tuning hyperparameter, dan keputusan akhir untuk model yang di-deploy. Juga termasuk instruksi untuk mengatur dan menjalankan aplikasi web.
