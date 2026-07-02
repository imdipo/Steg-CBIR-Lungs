import random
import os
from pathlib import Path
import json

class metadataGenerator():
    def __init__(self, path_gambar):
        self.path_gambar = Path(path_gambar)
        self.list_gambar = self.scan_nama_gambar()

        self.folder_tujuan = Path("Metadata")
        self.folder_tujuan.mkdir(exist_ok=True)

    
    def scan_nama_gambar(self):
        ekstensi = (".jpeg", ".png")
        nama_files = []

        for file in self.path_gambar.iterdir():
            if file.suffix.lower() in ekstensi:
                nama_files.append(file)
        
        return nama_files
    
    def buat_metadata(self):
        nama_depan = ["Jono", "Siti", "Ahmad", "Dewi", "Budi", "Rina", "Eko", "Lestari", "Hadi", "Putri", "Agus", "Maya", "Dedi", "Nina", "Fajar"]
        nama_belakang = ["Santoso", "Wijaya", "Pratama", "Kusuma", "Saputra", "Ningsih", "Rahman", "Susanto", "Hidayat", "Permana"]

        for i, pathGambar in enumerate(self.list_gambar, 1):
            nama = random.choice(nama_depan) + " " + random.choice(nama_belakang)
            umur = random.randint(18, 80)

            nama_file = pathGambar.stem
            

            data = {
                "id_pasien": f"pasien-{i:04d}",
                "nama": nama,
                "umur": umur,
                "kondisi": self.path_gambar.name
            }

            output_folder = self.folder_tujuan / self.path_gambar.name
            output_folder.mkdir(parents=True, exist_ok=True)

            output_file = output_folder / f"{nama_file}.txt"

            with open(output_file, "w") as file:
                json.dump(data, file, indent=4)

                print(f"{nama_file}.txt sudah")
            
            struktur_json = {
                "path_gambar" : str(pathGambar),
                "path_metadata": str(output_file)
            }

            file_jsonl = "pathData.jsonl" # buat naro path gambar sama pasangan path txt nya 

            with open(file_jsonl, "a", encoding="utf-8") as jsonl:
                jsonl.write(json.dumps(struktur_json) + '\n') 
        

    

if __name__ == "__main__":
    generator = metadataGenerator("Dataset_Paru/Cancer")
    generator.buat_metadata()



