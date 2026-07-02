import json
import os
import sys
import numpy as np
from PIL import Image
from config import constant

JSONL_FILE  = "pathData.jsonl"
OUTPUT_DIR  = "Hasil_Stegano"


def text_to_bits(text: str) -> list[int]:
    """Ubah string UTF-8 menjadi list bit (0/1) dengan aman."""
    bits = []
    for byte in text.encode("utf-8"):
        for bit in f"{byte:08b}":
            bits.append(int(bit)) # Format byte menjadi 8-bit biner string, lalu ubah ke int
    return bits


def encode_lsb(image_path: str, message: str, output_path: str) -> None:
    img = Image.open(image_path).convert("RGB")
    arr = np.array(img, dtype=np.uint8)

    full_message = message + DELIMITER
    bits = text_to_bits(full_message)

    max_bits = arr.size  # total elemen (H × W × 3)
    if len(bits) > max_bits:
        raise ValueError(
            f"Pesan terlalu panjang ({len(bits)} bit) "
            f"untuk gambar berukuran {arr.size} pixel-channel. "
            f"Kapasitas maks: {max_bits} bit."
        )

    flat = arr.flatten().copy()

    # Mengganti LSB dengan operasi bitwise
    for idx, bit in enumerate(bits):
        flat[idx] = (flat[idx] & 0xFE) | bit  # 0xFE membersihkan bit terakhir

    result = flat.reshape(arr.shape)
    out_img = Image.fromarray(result, "RGB")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # PNG wajib hukumnya biar bit LSB tidak rusak karena kompresi
    out_img.save(output_path, format="PNG")

def main():
    if not os.path.exists(JSONL_FILE):
        print(f"[ERROR] File '{JSONL_FILE}' tidak ditemukan di direktori ini.")
        sys.exit(1)

    success = 0
    failed  = 0
    skipped = 0

    with open(JSONL_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    total = len(lines)
    print(f"Ditemukan {total} entri di {JSONL_FILE}\n")

    for i, line in enumerate(lines, 1):
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"[{i}/{total}] JSON tidak valid {e}")
            failed += 1
            continue

        img_path  = entry.get("path_gambar",  "").replace("\\", "/")
        meta_path = entry.get("path_metadata", "").replace("\\", "/")

        if not os.path.exists(img_path):
            print(f"[{i}/{total}] Gambar tidak ditemukan: {img_path}")
            skipped += 1
            continue
        if not os.path.exists(meta_path):
            print(f"[{i}/{total}] Metadata tidak ditemukan: {meta_path}")
            skipped += 1
            continue

        with open(meta_path, "r", encoding="utf-8") as mf:
            metadata_text = mf.read().strip()

        file_name = os.path.basename(img_path)
        file_name_png = os.path.splitext(file_name)[0] + ".png"
        out_path = os.path.join(OUTPUT_DIR, file_name_png).replace("\\", "/")

        try:
            encode_lsb(img_path, metadata_text, out_path)
            print(f"[{i}/{total}] {img_path}  →  {out_path}")
            success += 1
        except ValueError as ve:
            print(f"[{i}/{total}] KAPASITAS: {ve}")
            failed += 1
        except Exception as e:
            print(f"[{i}/{total}] ERROR: {e}")
            failed += 1

    print(f"""Selesai!
  Berhasil  : {success}
  Dilewati  : {skipped}
  Gagal     : {failed}
  Total       : {total}
Output tersimpan di folder: {OUTPUT_DIR}/
""")

if __name__ == "__main__":
    main()