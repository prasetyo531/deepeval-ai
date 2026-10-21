# Rencana Seri Artikel Medium

Tulis artikel setelah eksperimen terkait benar-benar dijalankan. Bedakan hasil stub lokal dari temuan pada agent staging atau produksi.

## Seri Agent QA

1. **Dari chatbot ke agent: apa yang perlu diuji QA?** Bedakan jawaban akhir dengan rangkaian keputusan, tool call, izin, dan efek samping.
2. **Mendefinisikan kebenaran untuk agent bertool.** Susun task, expected tools dan args, state awal/akhir, serta aturan kapan agent harus meminta konfirmasi.
3. **Membangun harness lokal dengan pytest dan DeepEval.** Tunjukkan dataset sintetis, stub agent, pemeriksaan trace deterministik, batas versi metrik, dan laporan.
4. **Menghubungkan harness ke agent staging.** Bahas adapter, trace, sandbox, tool write/destructive, dan cara memastikan tes tidak mengubah data produksi.
5. **Mengalibrasi LLM judge.** Bandingkan skor Task Completion dan Argument Correctness dengan review SME, catat threshold dan ketidaksepakatan.
6. **Membawa agent eval ke CI dan operasi.** Jalankan smoke subset per merge request, full eval terjadwal, simpan metadata, serta tambahkan kasus gagal yang sudah ditinjau.

## Panduan penulisan

- Gunakan hanya hasil yang benar-benar dijalankan dan jelaskan apakah targetnya stub, staging, atau produksi.
- Pisahkan kontrak deterministik dari skor judge probabilistik.
- Sertakan threshold, makna, dan batas tiap metrik.
- Gunakan data sintetis; jangan publikasikan kredensial, data pelanggan, atau prompt internal.
- Jangan menyebut satu atau beberapa kasus sebagai bukti bahwa agent aman secara umum.

## Status

Semua artikel masih direncanakan. Artikel 3 dapat dimulai dari harness saat ini dengan menyebut bahwa ia menguji rangkaian test, bukan kualitas agent perusahaan.
