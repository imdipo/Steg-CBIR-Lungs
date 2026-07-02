import sampling, metadata_dummy

from pathlib import Path
from utils.encode_stegano import main as jalankan_stegano
from utils.databaseBuilder import XRayDatabaseBuilder

folder_dataset = Path("Dataset_Paru")
folder_metadata = Path("Metadata")

FOLDER_STEGANO = "Hasil_Stegano"
FILE_DATABASE = "pasangan_img_emb.jsonl"
FILE_PICKLE = "pickle_PCA.pkl"


def main():
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
    

    

if __name__ == "__main__":
    main()

    


    

    



