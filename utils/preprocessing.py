import cv2

"""
penjelasan kenapa alurnya begini dan parameternya segitu
sudah dijelaskan di google colab, link ditaro di readme depan
"""

class XRayPreprocessor:
    def __init__(self, crop_percent=0.1, target_size=(256, 256)):
        self.crop_percent = crop_percent
        self.target_size = target_size

        self.clahe_awal = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        self.clahe_akhir = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    def _crop_tepi(self, img):
        h, w = img.shape
        h_start = int(h * self.crop_percent)
        w_start = int(w * self.crop_percent)
        return img[h_start:int(h * (1 - self.crop_percent)), w_start:int(w * (1 - self.crop_percent))]

    def _buat_masker_paru(self, img_gray):
        img_kontras = self.clahe_awal.apply(img_gray)
        _, thresh = cv2.threshold(img_kontras, 150, 255, cv2.THRESH_BINARY_INV)
        kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (35, 35))
        mask_closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel_close)
        kernel_dilate = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        mask_final = cv2.dilate(mask_closed, kernel_dilate, iterations=1)

        return mask_final

    def _peningkatan_citra(self, img_masked):
        img_clahe = self.clahe_akhir.apply(img_masked)
        blur = cv2.GaussianBlur(img_clahe, (5, 5), 0)
        img_sharp = cv2.addWeighted(img_clahe, 4.5, blur, -3.5, 0)

        return img_sharp

    def preprocessing_satu_gambar(self, img_path):
        img_asli = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img_asli is None:
            print(f"Gambar {img_path} tidak ditemukan!")
            return None

        img_cropped = self._crop_tepi(img_asli)
        masker       = self._buat_masker_paru(img_cropped)
        img_masked   = cv2.bitwise_and(img_cropped, img_cropped, mask=masker)
        img_enhanced = self._peningkatan_citra(img_masked)

        # hasil akhir di-resize
        img_final = cv2.resize(img_enhanced, self.target_size)
        return img_final