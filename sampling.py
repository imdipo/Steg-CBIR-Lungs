from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent
DATASET_ASAL = BASE_DIR / "dataset"
DATASET_TUJUAN = Path("Eval")

ekstensi = {".png", ".jpeg"}

def run_sampling(path, jumlah_gambar):
    for folder in path.iterdir():
        print(folder)
        folder_kesehatan = DATASET_TUJUAN / folder.name

        folder_kesehatan.mkdir(parents=True, exist_ok=True)

        total_gambar = 0
        for gambar in folder.iterdir():
            if gambar.suffix.lower() in ekstensi:
                if total_gambar < jumlah_gambar:
                    
                    file_tujuan = folder_kesehatan / gambar.name

                    shutil.move(gambar, file_tujuan)
                    total_gambar += 1



