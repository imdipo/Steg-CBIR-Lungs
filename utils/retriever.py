import os
import json
import pickle
import numpy as np
from skimage.feature import hog
from scipy.spatial.distance import cdist
from .preprocessing import XRayPreprocessor
# from preprocessing import XRayPreprocessor


"""
buat ngetes gambar baru
ngambil gambar dengan kemiripan terdekat dari database
"""

class ImageRetriever:
    def __init__(self, model_pickle_path, database_jsonl_path):
        self.preprocessor = XRayPreprocessor()
        self.database = []

        with open(model_pickle_path, 'rb') as f:
            self.pca = pickle.load(f)

        with open(database_jsonl_path, 'r') as f:
            for line in f:
                self.database.append(json.loads(line))

        print(f"sudah memuat model PCA dan {len(self.database)} data indeks.")

    def _ekstrak_hog_mentah(self, img_clean):
        return hog(img_clean, orientations=9, pixels_per_cell=(16, 16), cells_per_block=(2, 2))

    def cari_3_terdekat(self, path_gambar_baru):
        """gambarnya kita balikin 3 gambar paling mirip"""
        img_clean = self.preprocessor.preprocessing_satu_gambar(path_gambar_baru)
        if img_clean is None:
            return []
        fitur_hog = self._ekstrak_hog_mentah(img_clean)
        vektor_baru = self.pca.transform([fitur_hog])[0]

        # buat ngitung jarak euclideannya
        semua_vektor_db = [data['embedding'] for data in self.database]
        jarak = cdist([vektor_baru], semua_vektor_db, metric='euclidean')[0]
        indeks_terdekat = np.argsort(jarak)[:3]

        hasil_retrieve = [self.database[idx] for idx in indeks_terdekat]

        # --- PANGGIL VISUALISASI DI SINI SEBELUM DI-RETURN ---
        # Kita ambil juga nilai jaraknya untuk ditampilkan sebagai skor kemiripan
        jarak_3_teratas = [jarak[idx] for idx in indeks_terdekat]
        self.tampilkan_plot_retrieval(path_gambar_baru, hasil_retrieve, jarak_3_teratas)

        return hasil_retrieve

    def tampilkan_plot_retrieval(self, path_kueri, hasil_retrieve, list_jarak):
        """Fungsi pembantu khusus membuat layout gambar bersebelahan"""
        # Bikin kanvas plot 1 baris dengan 4 kolom (1 kueri + 3 hasil)
        fig, axes = plt.subplots(1, 4, figsize=(15, 5))

        # 1. Plot Gambar Baru (Kueri) di kolom pertama
        img_kueri = cv2.imread(path_kueri, cv2.IMREAD_GRAYSCALE)
        axes[0].imshow(img_kueri, cmap='gray')
        axes[0].set_title("GAMBAR BARU (QUERY)", color='blue', fontweight='bold')
        axes[0].axis('off') # Hilangkan angka koordinat biar bersih

        # 2. Plot 3 Gambar Kembarannya di kolom berikutnya
        for i, data in enumerate(hasil_retrieve):
            path_db = data['path_asli']
            img_db = cv2.imread(path_db, cv2.IMREAD_GRAYSCALE)

            # Tampilkan di indeks axes ke-1, 2, dan 3
            axes[i+1].imshow(img_db, cmap='gray')
            # Kasih judul nama file dan jarak matematikanya (makin kecil jarak = makin mirip)
            axes[i+1].set_title(f"Rank {i+1}\nDist: {list_jarak[i]:.4f}", color='green')
            axes[i+1].axis('off')

        plt.tight_layout()
        plt.show()