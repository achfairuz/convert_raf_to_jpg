# Convert RAF to JPG

Script Python untuk mengkonversi file gambar (termasuk **RAW format Fujifilm `.RAF`**) menjadi file **JPEG**, dengan penamaan otomatis berbasis timestamp.

## Fitur

- Konversi file `.RAF` (Fujifilm RAW) ke `.JPG` menggunakan `rawpy`
- Konversi format gambar lain (`.PNG`, `.BMP`, `.TIFF`, dll.) ke `.JPG` menggunakan `Pillow`
- Penamaan file output otomatis: `leaf_<nomor>_<timestamp>.jpg`
- Melewati subfolder secara otomatis

## Struktur Folder

```
convert_raf_to_jpg/
├── main.py
├── requirements.txt
├── image/              # Letakkan file gambar input di sini
├── result_convert/     # Hasil konversi akan tersimpan di sini
└── dataset_result/
```

## Persyaratan

- Python 3.8+
- Dependencies (lihat `requirements.txt`):
  - `rawpy`
  - `imageio`
  - `pillow`

## Instalasi

1. Clone atau download repository ini.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Cara Penggunaan

1. Masukkan file gambar (`.RAF`, `.JPG`, `.PNG`, dll.) ke dalam folder `image/`.
2. Jalankan script:

```bash
python main.py
```

3. Hasil konversi akan tersimpan di folder `result_convert/` dengan format nama:
   ```
   leaf_1_20260513_120000.jpg
   leaf_2_20260513_120000.jpg
   ...
   ```

## Contoh Output

```
[SUCCESS] IMG_0001.RAF -> leaf_1_20260513_153045.jpg
[SUCCESS] photo.png -> leaf_2_20260513_153045.jpg
[ERROR] corrupted.raf: ...pesan error...
Selesai semua.
```
