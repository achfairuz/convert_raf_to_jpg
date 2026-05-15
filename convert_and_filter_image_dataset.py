import os
import shutil
from pathlib import Path
from datetime import datetime

# =========================
# DATASET FOLDER
# =========================

dataset_folder = r"D:\DATASET\downy-mildew"



images_folder = os.path.join(dataset_folder, "train", "images")
labels_folder = os.path.join(dataset_folder, "train", "labels")

output_folder = os.path.join(dataset_folder, "downy_mildew_only")

# =========================
# CLASS DOWNY MILDEW
# =========================

# names:
# 0 = Alternaria Leaf Blight
# 1 = Cucumber Mosaic Virus
# 2 = Downy Mildew
# 3 = Healthy
# 4 = Powdery Mildew

DOWNY_MILDEW_CLASS_ID = "2"

os.makedirs(output_folder, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

counter = 1

# =========================
# AMBIL SEMUA LABEL
# =========================

label_files = list(Path(labels_folder).glob("*.txt"))

print(f"Ditemukan {len(label_files)} file label. Memulai filter...")

skipped = 0

for label_path in label_files:

    try:

        # baca isi label
        with open(label_path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        # =================================
        # HARUS TEPAT 1 OBJECT
        # =================================
        if len(lines) != 1:
            skipped += 1
            continue

        # ambil class id
        class_id = lines[0].split()[0]

        # =================================
        # HARUS DOWNY MILDEW
        # =================================
        if class_id != DOWNY_MILDEW_CLASS_ID:
            skipped += 1
            continue

        # =================================
        # CARI FILE GAMBAR
        # =================================
        image_path = None

        for ext in [".jpg", ".jpeg", ".png"]:

            candidate = Path(images_folder) / f"{label_path.stem}{ext}"

            if candidate.exists():
                image_path = candidate
                break

        if image_path is None:
            skipped += 1
            continue

        # =================================
        # COPY GAMBAR SAJA
        # =================================
        new_name = f"leaf_{counter}_{timestamp}.jpg"

        output_path = os.path.join(output_folder, new_name)

        shutil.copy(image_path, output_path)

        print(f"[SUCCESS] {image_path.name} -> {new_name}")

        counter += 1

    except Exception as e:
        print(f"[ERROR] {label_path.name}: {e}")

print(f"\nSelesai semua. Total disalin: {counter - 1} file, dilewati: {skipped} file.")
print(f"Output folder: {output_folder}")