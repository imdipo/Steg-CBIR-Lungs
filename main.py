import sampling, metadata_dummy

from pathlib import Path
from utils.encode_stegano import main as jalankan_stegano
from utils.databaseBuilder import XRayDatabaseBuilder
from utils.retriever import ImageRetriever
from utils.predict_images import prediksi_kondisi_gambar_baru

folder_dataset = Path("Dataset_Paru")
folder_metadata = Path("Metadata")

FOLDER_STEGANO = Path("Hasil_Stegano")
FILE_DATABASE = Path("pasangan_img_emb.jsonl")
FILE_PICKLE = Path("pickle_PCA.pkl")


def proses_data_dulu():
    if not folder_dataset.is_dir():
        sampling.run_sampling(path="dataset", jumlah_gambar=50)
    
    jenis = [file.name for file in Path("dataset").iterdir() if file.is_dir()]

    if not folder_metadata.is_dir():
        for label in jenis:
            generator = metadata_dummy.metadataGenerator(f"folder_dataset/{label}")
            generator.buat_metadata()

    jalankan_stegano()

    mesin_embed = XRayDatabaseBuilder(n_components=50)
    mesin_embed.buat_database_embedding(
        folder_stegano=FOLDER_STEGANO,
        output_pickle_path=FILE_PICKLE,
        output_jsonl_path=FILE_DATABASE
    )

def tes_gambar_baru():
    if not FILE_PICKLE.is_file():
        print("ga ada file picklenya, jalanin dulu tahap 1")
        return
        
    if not FILE_DATABASE.is_file():
        print("ga ada file jsonlnya, jalanin dulu tahap 1")
        return

    path_gambar = input("path gambar yang mau dicek (contoh: test.png): ").strip().replace('"', '').replace("\\","/")

    if not Path(path_gambar).exists():
        print(f"{path_gambar} ga ketemu")
        return

    retriever = ImageRetriever(FILE_PICKLE, FILE_DATABASE)

    hasil_prediksi = prediksi_kondisi_gambar_baru(path_gambar, retriever)

    return hasil_prediksi

def main():
    while True:
        print("SISTEM STEGANO PARU-PARU")
        print("1. Jalankan pipeline data (Sampling -> Metadata -> LSB). wajib kalau file pendukungnya belum ada")
        print("2. Uji Coba Gambar Baru (Retriever)")
        print("3. Keluar")
        
        pilihan = input("Pilih menu (1/2/3): ").strip()
        
        if pilihan == "1":
            proses_data_dulu()
        elif pilihan == "2":
            tes_gambar_baru()
        elif pilihan == "3":
            print("ga 2 2nya dadah")
            break
        else:
            print("[WARNING] Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()
    


    

    



