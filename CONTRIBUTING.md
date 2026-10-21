# Panduan Kontribusi

Terima kasih sudah membantu mengembangkan AI Testing Lab. Fokus aktif proyek adalah evaluasi agent customer support bertool dengan Python, pytest, dan DeepEval. Stub lokal hanya memvalidasi harness.

## 1. Siapkan environment

Jalankan perintah dari folder proyek:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 2. Buat branch untuk perubahan

Jika proyek sudah berada di Git dan kontribusi dibuat melalui pull request, mulai dari branch terbaru:

```bash
git switch main
git pull
git switch -c feature/deskripsi-perubahan
```

Gunakan nama branch yang menjelaskan perubahan, misalnya `test/add-refund-cases` atau `docs/update-setup-guide`.

## 3. Buat perubahan

- Tambahkan atau perbarui skenario agent di `testdata/agent_dataset.json`.
- Jika perilaku agent simulasi berubah, perbarui `utils/agent_stub.py` dan pastikan trace, allowlist, output, serta state yang diharapkan konsisten.
- Perbarui `tests/` untuk menguji perilaku baru. Pertahankan pemisahan antara pemeriksaan deterministik dan evaluasi berbasis LLM.
- Perbarui dokumentasi di `docs/` atau `README.md` jika perubahan memengaruhi cara setup, menjalankan tes, atau menafsirkan hasil.
- Gunakan assertion deterministik untuk tool trace, izin, dan perubahan state yang punya kontrak jelas. Pisahkan metrik berbasis judge jika nanti ditambahkan.

## 4. Jalankan evaluasi

```bash
npm run test:qa
```

Pastikan semua kasus lulus. Periksa ringkasan di terminal atau buka `reports/agent-harness.html`. Jika ada tes yang gagal, perbaiki masalahnya atau jelaskan alasan kegagalan yang memang diharapkan.

## 5. Jaga kredensial dan biaya

- Jangan menulis API key, token, atau data pelanggan sungguhan ke source code, dataset, atau laporan yang akan di-commit.
- `npm run test:qa` menjalankan agent harness lokal dan tidak memerlukan API key.
- Sebelum menambahkan panggilan model berbayar, dokumentasikan provider, konfigurasi key, perkiraan biaya, dan sumber nondeterminisme.
- Pastikan contoh dataset tetap sintetis dan tidak memuat informasi pribadi.

## 6. Siapkan perubahan untuk ditinjau

Sebelum mengajukan pull request:

- Tinjau perubahan dan pastikan file `.venv/`, `.env`, cache, serta laporan lokal tidak ikut ditambahkan.
- Pastikan dokumentasi mencerminkan perilaku terbaru.
- Jelaskan tujuan perubahan, cakupan tes, hasil eksekusi, serta batasan yang masih ada.

## Batasan milestone saat ini

Agent yang diuji masih berupa stub deterministik. Kontribusi yang menambahkan agent staging, judge semantik, security testing yang lebih luas, atau CI perlu menyertakan kriteria evaluasi dan batasan yang sesuai; jangan menyatakan agent produksi aman atau akurat berdasarkan hasil stub.
