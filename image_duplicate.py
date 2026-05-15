import os
from pathlib import Path

import imagehash
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

# =========================
# KONFIGURASI
# =========================

TARGET_DIR   = r"D:\DATASET\Downy_mildew_20260515_130347"
HASH_THRESHOLD = 10        # 0 = identik persis, makin besar makin longgar
THUMB_SIZE   = (200, 200)
EXTENSIONS   = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".heic"}

# =========================
# SCAN & HASH
# =========================

def scan_images(folder: str) -> list[Path]:
    return [
        p for p in Path(folder).iterdir()
        if p.is_file() and p.suffix.lower() in EXTENSIONS
    ]


def compute_hashes(image_paths: list[Path]) -> dict:
    hashes = {}
    total = len(image_paths)
    for i, path in enumerate(image_paths, 1):
        try:
            with Image.open(path) as img:
                hashes[path] = imagehash.phash(img)
        except Exception as e:
            print(f"[SKIP] {path.name}: {e}")
        if i % 50 == 0 or i == total:
            print(f"  Hash: {i}/{total} file selesai")
    return hashes


def find_duplicate_groups(hashes: dict, threshold: int) -> list[list[Path]]:
    paths = list(hashes.keys())
    parent = {p: p for p in paths}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        parent[find(x)] = find(y)

    for i, p1 in enumerate(paths):
        for p2 in paths[i + 1:]:
            if hashes[p1] - hashes[p2] <= threshold:
                union(p1, p2)

    groups: dict = {}
    for p in paths:
        root = find(p)
        groups.setdefault(root, []).append(p)

    return [g for g in groups.values() if len(g) > 1]


# =========================
# GUI
# =========================

class DuplicateReviewApp:
    def __init__(self, root: tk.Tk, groups: list[list[Path]]):
        self.root = root
        self.groups = groups
        self.current_index = 0
        self.deleted_count = 0
        self.check_vars: list[tuple[tk.BooleanVar, Path]] = []
        self.img_refs: list = []          # cegah garbage collection

        self.root.title("Deteksi Duplikat Gambar")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(True, True)
        self.root.minsize(500, 420)

        self._build_ui()
        self._show_group()

    # --------------------------------------------------
    # Build UI
    # --------------------------------------------------

    def _build_ui(self):
        # Header
        self.header_label = tk.Label(
            self.root, text="",
            font=("Segoe UI", 12, "bold"),
            bg="#1e1e1e", fg="white"
        )
        self.header_label.pack(pady=(12, 4))

        # Scrollable canvas untuk gambar
        canvas_frame = tk.Frame(self.root, bg="#1e1e1e")
        canvas_frame.pack(fill="both", expand=True, padx=10)

        self.canvas = tk.Canvas(canvas_frame, bg="#1e1e1e", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=scrollbar.set)
        scrollbar.pack(side="bottom", fill="x")
        self.canvas.pack(side="top", fill="both", expand=True)

        # Frame di dalam canvas
        self.img_frame = tk.Frame(self.canvas, bg="#1e1e1e")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.img_frame, anchor="nw")
        self.img_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Tombol aksi
        btn_frame = tk.Frame(self.root, bg="#1e1e1e")
        btn_frame.pack(pady=10)

        self.btn_delete = tk.Button(
            btn_frame, text="Hapus Terpilih",
            font=("Segoe UI", 10, "bold"),
            bg="#c0392b", fg="white", padx=16, pady=8,
            relief="flat", cursor="hand2",
            command=self._delete_selected
        )
        self.btn_delete.pack(side="left", padx=8)

        self.btn_skip = tk.Button(
            btn_frame, text="Lewati",
            font=("Segoe UI", 10),
            bg="#2980b9", fg="white", padx=16, pady=8,
            relief="flat", cursor="hand2",
            command=self._skip
        )
        self.btn_skip.pack(side="left", padx=8)

        self.btn_cancel = tk.Button(
            btn_frame, text="Batal Semua",
            font=("Segoe UI", 10),
            bg="#555555", fg="white", padx=16, pady=8,
            relief="flat", cursor="hand2",
            command=self._cancel
        )
        self.btn_cancel.pack(side="left", padx=8)

        # Status bar
        self.status_label = tk.Label(
            self.root, text="",
            font=("Segoe UI", 9),
            bg="#1e1e1e", fg="#aaaaaa"
        )
        self.status_label.pack(pady=(0, 10))

    def _on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event=None):
        # Sesuaikan tinggi frame dalam canvas
        self.canvas.itemconfig(self.canvas_window, height=event.height)

    # --------------------------------------------------
    # Tampilkan grup duplikat
    # --------------------------------------------------

    def _show_group(self):
        if self.current_index >= len(self.groups):
            self._finish()
            return

        # Bersihkan area gambar
        for widget in self.img_frame.winfo_children():
            widget.destroy()
        self.check_vars.clear()
        self.img_refs.clear()

        group = self.groups[self.current_index]

        self.header_label.config(
            text=f"Grup {self.current_index + 1} / {len(self.groups)}   —   {len(group)} gambar mirip ditemukan"
        )

        for path in group:
            col = tk.Frame(self.img_frame, bg="#2d2d2d", padx=6, pady=6)
            col.pack(side="left", padx=8, pady=8)

            # Thumbnail
            try:
                img = Image.open(path)
                img.thumbnail(THUMB_SIZE, Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.img_refs.append(photo)
                tk.Label(col, image=photo, bg="#2d2d2d").pack()
            except Exception:
                tk.Label(col, text="[Gagal memuat]", bg="#2d2d2d",
                         fg="#e74c3c", width=22, height=10).pack()

            # Info file
            size_kb = path.stat().st_size // 1024
            tk.Label(
                col,
                text=f"{path.name}\n{size_kb} KB",
                font=("Segoe UI", 8), bg="#2d2d2d", fg="#cccccc",
                wraplength=200, justify="center"
            ).pack(pady=(4, 2))

            # Checkbox
            var = tk.BooleanVar(value=False)
            self.check_vars.append((var, path))
            tk.Checkbutton(
                col, text="Tandai untuk dihapus",
                variable=var, font=("Segoe UI", 8),
                bg="#2d2d2d", fg="#ff6b6b",
                selectcolor="#c0392b",
                activebackground="#2d2d2d",
                activeforeground="#ff6b6b"
            ).pack()

        self.status_label.config(
            text=f"Centang gambar yang ingin dihapus lalu klik 'Hapus Terpilih'   |   "
                 f"Total sudah dihapus: {self.deleted_count} file   |   "
                 f"Sisa grup: {len(self.groups) - self.current_index}"
        )

    # --------------------------------------------------
    # Aksi tombol
    # --------------------------------------------------

    def _delete_selected(self):
        to_delete = [p for var, p in self.check_vars if var.get()]

        if not to_delete:
            messagebox.showwarning(
                "Tidak ada pilihan",
                "Belum ada gambar yang ditandai untuk dihapus."
            )
            return

        confirm = messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Yakin ingin menghapus {len(to_delete)} file berikut?\n\n"
            + "\n".join(f"  • {p.name}" for p in to_delete)
        )
        if not confirm:
            return

        for path in to_delete:
            try:
                os.remove(path)
                print(f"[DELETED] {path}")
                self.deleted_count += 1
            except Exception as e:
                print(f"[ERROR] Gagal hapus {path.name}: {e}")

        self.current_index += 1
        self._show_group()

    def _skip(self):
        self.current_index += 1
        self._show_group()

    def _cancel(self):
        if messagebox.askyesno("Batal Semua", "Yakin ingin menghentikan proses sekarang?"):
            print(f"\nProses dibatalkan. Total dihapus: {self.deleted_count} file.")
            self.root.destroy()

    def _finish(self):
        messagebox.showinfo(
            "Selesai",
            f"Semua grup sudah ditinjau.\n\nTotal file dihapus: {self.deleted_count}"
        )
        print(f"\nSelesai. Total dihapus: {self.deleted_count} file.")
        self.root.destroy()


# =========================
# MAIN
# =========================

def main():
    print(f"Target folder: {TARGET_DIR}")
    print("-" * 50)

    images = scan_images(TARGET_DIR)
    if not images:
        print("Tidak ada gambar ditemukan di folder tersebut.")
        return

    print(f"Ditemukan {len(images)} gambar. Menghitung hash perceptual...")
    hashes = compute_hashes(images)

    print(f"Mencari duplikat (threshold = {HASH_THRESHOLD})...")
    groups = find_duplicate_groups(hashes, HASH_THRESHOLD)

    if not groups:
        print("Tidak ada gambar duplikat atau mirip yang ditemukan.")
        return

    total_dup = sum(len(g) for g in groups)
    print(f"Ditemukan {len(groups)} grup, {total_dup} gambar terlibat.")
    print("Membuka jendela GUI...\n")

    root = tk.Tk()
    app = DuplicateReviewApp(root, groups)

    # Paksa window muncul di depan
    root.lift()
    root.attributes("-topmost", True)
    root.after(500, lambda: root.attributes("-topmost", False))
    root.focus_force()

    root.mainloop()


if __name__ == "__main__":
    main()
