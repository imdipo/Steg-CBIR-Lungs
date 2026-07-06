# Secure Content-Based Image Retrieval (SCBIR) for X-Ray Images

Proyek ini adalah sistem **Content-Based Image Retrieval (CBIR)** sederhana yang dirancang untuk menganalisis dan mencari kemiripan gambar medis (gambar X-Ray paru paru). "Secure" karena informasi metadata pasien (nama, jenis penyakit) disimpan didalam gambarnya dengan metode Stegano LSB (least significant bit). awalnya mau menggunakan stegano-GAN tapi diluar lingkup mata kuliah 
---

## Fitur Utama
1. **Ekstraksi Fitur**: Mengekstrak fitur visual dari dataset gambar X-Ray menggunakan OpenCV dan menyimpannya ke dalam basis data lokal (`.jsonl` / `.pkl`).
2. **Pencarian Gambar Kembar (Retrieval)**: Mencari gambar yang paling mirip berdasarkan gambar kueri (*query image*) yang dimasukkan oleh pengguna menggunakan perhitungan jarak komputasi.
3. **Visualisasi Hasil**: menyimpan hasil pencarian gambar terdekat.

---

## Prerequisites
Sebelum menjalankan aplikasi, pastikan perangkat Anda sudah terinstal:
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Pastikan Docker Engine dalam status *Running*).

---

## step-by-step

### 1. Unduh Dataset Gambar
Karena ukuran dataset gambar medis cukup besar, dataset tidak dimasukkan ke dalam repositori ini. 
* Silakan unduh folder dataset melalui tautan Google Drive berikut: **[GDrive](link_dataset_gambar.txt)**
* Ekstrak file ZIP hasil unduhan tersebut ke salah satu folder di laptop Anda (misal: `C:\Users\NamaAnda\Documents\dataset_xray`).

tapi, yang di drive ga gede gede banget sih intinya struktur dataset yang diharapkan tuh gini
```
dataset/
├── kanker/
│   ├── gambar_01.png
│   └── gambar_02.jpeg
├── tbc/
│   ├── gambar_01.png
│   └── gambar_02.jpeg
└── normal/
    ├── gambar_01.png
    └── gambar_02.jpeg
```

### 2. Jalankan Container Docker
Buka Terminal (PowerShell/CMD di Windows atau Terminal di Mac/Linux), lalu jalankan perintah berikut untuk mengunduh Image dari Docker Hub dan menghubungkannya dengan dataset di lokal:

```bash
docker run -it \
  --name scbir-aktif \
  -v "C:\Users\NamaAnda\Documents\dataset_xray:/app/dataset" \
  dockerdipo/scbir-app:v1
```