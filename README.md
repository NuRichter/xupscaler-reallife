# XUpscaler RealLife

Upscaler khusus foto dan gambar nyata, bukan digital art. Pipeline ini menggabungkan delapan model secara berurutan supaya hasil akhirnya sedetail mungkin, sambil tetap terasa natural.

Ini adalah bagian dari ekosistem XUpscaler yang lebih besar. Versi GUI akan hadir nanti.

---

## Cara pakai

Install dulu:

```bash
pip install -e .
```

Lalu jalankan:

```bash
xup run
```

Kamu akan diminta input path gambar dan skala. Bisa juga langsung dari argumen:

```bash
xup run "C:\Users\kamu\foto.jpg" --scale 4x
```

Drag and drop path ke terminal juga oke, tanda kutip otomatis dibuang.

Output disimpan di folder yang sama dengan file input:

- `foto_reallife_4x.png` - hasil akhir
- `foto_reallife_4x.zip` - file yang sama, tapi sudah dikemas

---

## Cek status model

```bash
xup status
```

Ini menampilkan model mana yang sudah siap, mana yang masih perlu diunduh, dan mana yang perlu diunduh manual.

---

## Auto-download

Pertama kali jalan, semua model yang bisa diunduh otomatis akan diambil dari HuggingFace dan disimpan di folder `models/`. Proses ini hanya terjadi sekali.

Beberapa model (seperti OSEDiff) perlu akses manual karena ada gated repo. Instruksi akan muncul di terminal kalau sudah saatnya.

Kalau mau skip auto-download:

```bash
xup run foto.jpg --scale 4x --no-download
```

Kalau auto-download gagal, kamu bisa unduh manual dan taruh file-nya di folder `models/<nama_model>/` sesuai tabel di bawah.

---

## Download manual

Letakkan tiap file weight di folder `models/` sesuai kolom path-nya.

| Model     | File                             | Path                  | Link                                                               |
| --------- | -------------------------------- | --------------------- | ------------------------------------------------------------------ |
| SUPIR     | `SUPIR-v0Q.ckpt`               | `models/supir/`     | [Kijai/SUPIR_pruned](https://huggingface.co/Kijai/SUPIR_pruned)       |
| DiffBIR   | `general_swinir_v1.ckpt`       | `models/diffbir/`   | [lxq007/DiffBIR](https://huggingface.co/lxq007/DiffBIR)               |
| DiffBIR   | `v2.pth`                       | `models/diffbir/`   | [lxq007/DiffBIR](https://huggingface.co/lxq007/DiffBIR)               |
| SeeSR     | `ram_swin_large_14m.pth`       | `models/seesr/`     | [starboardai/seesr](https://huggingface.co/starboardai/seesr)         |
| SeeSR     | `seesr.safetensors`            | `models/seesr/`     | [starboardai/seesr](https://huggingface.co/starboardai/seesr)         |
| PASD      | `pasd.safetensors`             | `models/pasd/`      | [zhanggy/PASD](https://huggingface.co/zhanggy/PASD)                   |
| ResShift  | `resshift_realsrx4_s15_v1.pth` | `models/resshift/`  | [ShinyPikachu/ResShift](https://huggingface.co/ShinyPikachu/ResShift) |
| InvSR     | `invsr.pth`                    | `models/invsr/`     | [zsyOAOA/InvSR](https://huggingface.co/zsyOAOA/InvSR)                 |
| OSEDiff   | `osediff.pkl`                  | `models/osediff/`   | [rongyaofang/OSEDiff](https://huggingface.co/rongyaofang/OSEDiff)    |
| FaithDiff | `faithdiff.safetensors`        | `models/faithdiff/` | [KunpengSong/FaithDiff](https://huggingface.co/KunpengSong/FaithDiff) |

> OSEDiff memerlukan login HuggingFace dan persetujuan akses sebelum bisa diunduh. Buka link-nya, login, lalu request access dulu.

Setelah file ada di tempat yang benar, jalankan `xup status` untuk verifikasi.

---

## Skip model tertentu

```bash
xup run foto.jpg --scale 4x --skip osediff --skip faithdiff
```

Model yang di-skip tidak mempengaruhi model lainnya. Pipeline tetap jalan.

---

## Scale yang didukung

`2`, `2x`, `4`, `4x`, `8`, `8x`

---

## Pipeline

```
SUPIR -> DiffBIR -> SeeSR -> PASD -> ResShift -> InvSR -> OSEDiff -> FaithDiff
```

Tiap model load, jalan, lalu unload sebelum model berikutnya mulai. VRAM tidak akan meledak (semoga).

---

## Struktur project

```
xupscaler/
  cli.py          entry point
  pipeline.py     orchestrator
  downloader.py   auto-download weights
  output.py       simpan gambar dan zip
  utils.py        parse path dan scale
  models/
    registry.py   source of truth semua metadata model
    base.py       interface dasar
    supir.py      ... dan tujuh model lainnya
models/           folder weights (gitignored)
```

---

## Catatan

- Ini masih versi awal. Implementasi inference tiap model masih stub dan akan diisi satu per satu.
- Windows jadi target utama dulu, tapi tidak ada yang Linux-breaking di sini.
- Kalau ada bug atau model yang gagal, pipeline tetap lanjut ke model berikutnya.
