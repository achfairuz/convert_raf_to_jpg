# Convert RAF to JPG & Dataset Filter

Kumpulan script Python untuk:

1. **Mengkonversi** file gambar (`.RAF`, `.HEIC`, `.PNG`, dll.) menjadi **JPEG** — `main.py`
2. **Memfilter dataset YOLOv8** berdasarkan kelas tertentu — `convert_and_filter_image_dataset.py`
3. **Mendeteksi gambar duplikat/mirip** secara visual & interaktif — `image_duplicate.py`

---

## Script 1 — `main.py` : Konversi Gambar ke JPG

### Fitur

- Konversi file `.RAF` (Fujifilm RAW) ke `.JPG` menggunakan `rawpy`
- Konversi file `.HEIC` (Apple/iPhone) ke `.JPG` menggunakan `pillow-heif`
- Konversi format lain (`.PNG`, `.BMP`, `.TIFF`, dll.) ke `.JPG` menggunakan `Pillow`
- Penamaan file output otomatis: `leaf_<nomor>_<timestamp>.jpg`
- Melewati subfolder secara otomatis

### Cara Penggunaan

1. Masukkan file gambar ke dalam folder `image/`
2. Jalankan:

```bash
python main.py
```

3. Hasil tersimpan di `result_convert/`

### Contoh Output

```
[SUCCESS] IMG_0001.RAF  -> leaf_1_20260515_153045.jpg
[SUCCESS] photo.HEIC    -> leaf_2_20260515_153045.jpg
[SUCCESS] scan.png      -> leaf_3_20260515_153045.jpg
[ERROR]   corrupted.raf : ...pesan error...
Selesai semua.
```

---

## Script 2 — `convert_and_filter_image_dataset.py` : Filter Dataset YOLOv8

### Fitur

- Membaca label YOLOv8 (format `.txt`) dari folder `train/labels/`
- Menyaring gambar yang hanya memiliki **tepat 1 objek** dengan **kelas tertentu**
- Menyalin gambar yang lolos filter ke folder output baru
- Menampilkan ringkasan: total disalin & dilewati

### Konfigurasi

Edit bagian ini di awal script sebelum menjalankan:

```python
dataset_folder = r"D:\DATASET\nama-dataset"   # path folder dataset
DOWNY_MILDEW_CLASS_ID = "2"                   # ID kelas yang ingin difilter
```

Mapping kelas (sesuaikan dengan `data.yaml` dataset):

| ID  | Nama Kelas             |
| --- | ---------------------- |
| 0   | Alternaria Leaf Blight |
| 1   | Cucumber Mosaic Virus  |
| 2   | Downy Mildew           |
| 3   | Healthy                |
| 4   | Powdery Mildew         |

### Struktur Dataset yang Diharapkan

```
nama-dataset/
├── data.yaml
└── train/
    ├── images/   # file .jpg / .jpeg / .png
    └── labels/   # file .txt (format YOLOv8)
```

### Cara Penggunaan

1. Sesuaikan `dataset_folder` dan `CLASS_ID` di dalam script
2. Jalankan:

```bash
python convert_and_filter_image_dataset.py
```

3. Hasil tersimpan di subfolder output (misalnya `downy_mildew_only/` atau `healthy_only/`)

### Contoh Output

```
Ditemukan 3099 file label. Memulai filter...
[SUCCESS] leaf_001.jpg -> leaf_1_20260515_122714.jpg
[SUCCESS] leaf_002.jpg -> leaf_2_20260515_122714.jpg
...
Selesai semua. Total disalin: 2208 file, dilewati: 891 file.
Output folder: D:\DATASET\nama-dataset\downy_mildew_only
```

---

## Struktur Folder Workspace

```
convert_raf_to_jpg/
├── main.py                              # Script konversi gambar
├── convert_and_filter_image_dataset.py  # Script filter dataset YOLOv8
├── image_duplicate.py                   # Script deteksi duplikat gambar
├── requirements.txt
├── image/                               # Input gambar untuk main.py
├── result_convert/                      # Output konversi main.py
└── dataset_result/
```

---

## Script 3 — `image_duplicate.py` : Deteksi Gambar Duplikat / Mirip

### Fitur

- Mendeteksi gambar duplikat atau mirip menggunakan **perceptual hash (phash)**
- Tahan terhadap perbedaan kecil (resize, kompresi, brightness)
- Menampilkan **GUI interaktif** — thumbnail semua gambar per grup
- Pilihan per grup: **hapus**, **lewati**, atau **batalkan semua**
- Menampilkan nama file dan ukuran (KB) setiap gambar

### Konfigurasi

Edit bagian ini di awal script:

```python
TARGET_DIR     = r"D:\DATASET\nama-folder"  # folder yang ingin dicek
HASH_THRESHOLD = 10                          # 0 = identik persis, makin besar makin longgar
```

### Cara Penggunaan

1. Sesuaikan `TARGET_DIR` di dalam script
2. Jalankan:

```bash
python image_duplicate.py
```

3. GUI akan terbuka — tinjau setiap grup gambar mirip secara visual

### Tombol di GUI

| Tombol             | Aksi                                                                 |
| ------------------ | -------------------------------------------------------------------- |
| **Hapus Terpilih** | Konfirmasi lalu hapus file yang dicentang, lanjut ke grup berikutnya |
| **Lewati**         | Skip grup ini, lanjut ke grup berikutnya                             |
| **Batal Semua**    | Hentikan seluruh proses                                              |

### Contoh Output Terminal

```
Target folder: D:\DATASET\Downy_mildew_20260515_130347
Ditemukan 512 gambar. Menghitung hash perceptual...
  Hash: 50/512 file selesai
  Hash: 100/512 file selesai
  ...
Ditemukan 8 grup, 21 gambar terlibat.
[DELETED] D:\DATASET\...\leaf_3_20260515.jpg
[DELETED] D:\DATASET\...\leaf_7_20260515.jpg

Selesai. Total dihapus: 2 file.
```

---

## Persyaratan

- Python 3.8+
- Dependencies:

```bash
pip install -r requirements.txt
```

| Package       | Kegunaan                               |
| ------------- | -------------------------------------- |
| `rawpy`       | Membaca file RAW Fujifilm (`.RAF`)     |
| `imageio`     | Menyimpan hasil konversi RAW           |
| `pillow`      | Konversi format gambar umum            |
| `pillow-heif` | Dukungan format `.HEIC` (iPhone/Mac)   |
| `imagehash`   | Perceptual hash untuk deteksi duplikat |
