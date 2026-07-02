import os
import json
import pickle
import numpy as np
from skimage.feature import hog
from sklearn.decomposition import PCA
from .preprocessing import XRayPreprocessor
"""
karena ini lebih mengarah pada penelitian,
jadi databasenya menggunakan file jsonl
"""

class XRayDatabaseBuilder:
    def __init__(self, n_components=50):
        self.preprocessor = XRayPreprocessor()
        self.pca = PCA(n_components=n_components)

    def _ekstrak_hog_mentah(self, img_clean):
        return hog(img_clean, orientations=9, pixels_per_cell=(16, 16), cells_per_block=(2, 2))

    def buat_database_embedding(self, folder_stegano, output_pickle_path, output_jsonl_path):
        format_gambar = ('.png', '.jpeg')
        semua_file = [f for f in os.listdir(folder_stegano) if f.lower().endswith(format_gambar)]

        list_path_asli = []
        list_fitur_hog = []

        print(f"ekstrak fitur dari {len(semua_file)} gambar")
        for file_name in semua_file:
            path_img = os.path.join(folder_stegano, file_name)
            img_clean = self.preprocessor.preprocessing_satu_gambar(path_img)

            if img_clean is not None:
                fitur_hog = self._ekstrak_hog_mentah(img_clean)
                list_fitur_hog.append(fitur_hog)
                list_path_asli.append(path_img)

        if len(list_fitur_hog) < self.pca.n_components:
            print("Jumlah gambar kurang untuk melatih PCA")
            return

        print("\nmelatih PCA & Menyimpan Model dalam bentuk .pkl")
        matriks_hog = np.array(list_fitur_hog)
        embedding_final = self.pca.fit_transform(matriks_hog)

        with open(output_pickle_path, 'wb') as f:
            pickle.dump(self.pca, f)
        print(f"Model PCA sukses disimpan ke -> {output_pickle_path}")

        print("\nhasil embedding ke Database (.jsonl) ---")
        with open(output_jsonl_path, 'w') as f:
            for i in range(len(list_path_asli)):
                data_objek = {
                    "path_asli": list_path_asli[i],
                    "embedding": embedding_final[i].tolist()
                }
                f.write(json.dumps(data_objek) + '\n')
        print(f"Database embedding sukses disimpan ke -> {output_jsonl_path}")