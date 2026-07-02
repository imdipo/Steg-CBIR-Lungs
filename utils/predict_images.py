import os
from collections import Counter
import decode_stegano

def prediksi_kondisi_gambar_baru(path_gambar_baru, retriever_object):
    top_3 = retriever_object.cari_3_terdekat(path_gambar_baru)

    if not top_3:
        print("Gambar tidak dapat diproses atau tidak ditemukan kembarannya")
        return "Unknown"

    list_kondisi = []

    print(f"\n=== HASIL RETRIEVAL UNTUK: {os.path.basename(path_gambar_baru)} ===")
    for idx, data in enumerate(top_3, 1):
        path_stegano_db = data['path_asli']

        # Ekstrak dictionary metadata pasien dari gambar stegano
        info_pasien = decode_stegano.decode_single(path_stegano_db)

        if info_pasien and 'kondisi' in info_pasien:
            kondisi_penyakit = info_pasien['kondisi']
            list_kondisi.append(kondisi_penyakit)

            print(f"  terdekat {idx}: {os.path.basename(path_stegano_db)} | Kondisi Pasien: {kondisi_penyakit}")
        else:
            print(f"  terdekat {idx}: {os.path.basename(path_stegano_db)} | [TIDAK ADA METADATA]")

    if list_kondisi:
        hitung_data = Counter(list_kondisi)
        kondisi_terbanyak = hitung_data.most_common(1)[0][0]

        print(f"=> Kesimpulan Prediksi (Voting terbanyak): {kondisi_terbanyak}")
        return kondisi_terbanyak

    return "Unknown"