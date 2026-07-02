from PIL import Image
import numpy as np
import json
import os



def decode_lsb(image_path: str):
    img = Image.open(image_path).convert("RGB")
    arr = np.array(img, dtype=np.uint8)
    flat  = arr.flatten()
    chars  = []
    buffer = []

    for val in flat:
        buffer.append(int(val) & 1)
        if len(buffer) == 8:
            char = chr(int("".join(map(str, buffer)), 2))
            chars.append(char)
            buffer = []
            text_so_far = "".join(chars)
            if text_so_far.endswith(DELIMITER):
                return text_so_far[: -len(DELIMITER)]
    return None

def decode_single(path: str):
    pesan_rahasia = decode_lsb(path)

    if pesan_rahasia:
        try:
            data_pasien = json.load(pesan_rahasia)
            return data_pasien
        except (ValueError, SyntaxError) as e:
            print(f"Gagal parse struktur data dari gambar: {path} | Error: {e}")
            return None
    return None