import os
from pathlib import Path
from datetime import datetime

import rawpy
import imageio
from PIL import Image

# Folder input dan output
input_folder = "image"
output_folder = "result_convert"

os.makedirs(output_folder, exist_ok=True)

# Ambil semua file
all_files = list(Path(input_folder).iterdir())

# Timestamp sekali saja
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

counter = 1

for file_path in all_files:

    # Skip kalau folder
    if file_path.is_dir():
        continue

    try:
        # Nama baru
        new_name = f"leaf_{counter}_{timestamp}.jpg"
        output_path = os.path.join(output_folder, new_name)

        # =========================
        # Kalau file .RAF
        # =========================
        if file_path.suffix.lower() == ".raf":

            with rawpy.imread(str(file_path)) as raw:
                rgb = raw.postprocess()

            imageio.imwrite(output_path, rgb)

        # =========================
        # Selain .RAF
        # =========================
        else:
            img = Image.open(file_path)
            img.convert("RGB").save(output_path, "JPEG", quality=95)

        print(f"[SUCCESS] {file_path.name} -> {new_name}")

        counter += 1

    except Exception as e:
        print(f"[ERROR] {file_path.name}: {e}")

print("Selesai semua.")