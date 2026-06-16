# DATA SIMULASI RAPAT — SISTEM NOTULENSIA
## Digunakan sebagai Ground Truth untuk Pengujian WER dan ROUGE-L

---

## METADATA SIMULASI

| Atribut          | Detail                                             |
|------------------|----------------------------------------------------|
| Jenis Rapat      | Rapat Akademik Program Studi                       |
| Topik            | Evaluasi Kurikulum & Usulan Mata Kuliah Baru       |
| Jumlah Pembicara | 5 (Moderator, Dosen A, Dosen B, Dosen C, Mahasiswa)|
| Estimasi Durasi  | ±12–15 menit (jika direkam)                        |
| Bahasa           | Indonesia semi-formal                              |
| Fungsi           | Ground truth untuk WER (transkripsi) & ROUGE-L (ringkasan) |
| Tanggal Simulasi | 10 Maret 2025 (fiktif)                             |

---

## NASKAH DIALOG SIMULASI

```
[RAPAT AKADEMIK — Evaluasi Kurikulum dan Usulan Mata Kuliah Baru]
[Tanggal Simulasi: 10 Maret 2025 | Ruang: Ruang Rapat Program Studi Teknik Informatika]

Peserta:
1. Moderator  : Dr. Ahmad Fauzi, M.T. (Ketua Program Studi)
2. Dosen A    : Dr. Budi Santoso, M.Kom.
3. Dosen B    : Ibu Citra Dewi, M.T.
4. Dosen C    : Pak Dedi Wijaya, M.Sc.
5. Mahasiswa  : Eko Prasetyo (Perwakilan BEM Prodi)
```

---

Moderator: Baik, rapat kita mulai. Saya ucapkan terima kasih kepada semua yang hadir pada sore hari ini. Hari ini kita akan membahas dua agenda utama. Agenda pertama adalah evaluasi pelaksanaan mata kuliah semester genap tahun akademik dua ribu dua puluh empat stroke dua ribu dua puluh lima. Agenda kedua adalah usulan penambahan mata kuliah kecerdasan buatan ke dalam kurikulum prodi. Silakan Pak Budi untuk membuka diskusi terkait agenda pertama.

Dosen A: Terima kasih Pak Ketua. Berdasarkan rekap nilai ujian akhir semester yang sudah saya kompilasi, nilai rata-rata mahasiswa pada mata kuliah Struktur Data mengalami penurunan sekitar dua belas persen dibandingkan semester sebelumnya. Dari rata-rata tujuh puluh dua menjadi enam puluh tiga koma empat. Saya menduga ini terkait dengan beban praktikum yang terlalu padat, ditambah materi yang cukup abstrak untuk mahasiswa semester dua.

Dosen B: Saya setuju dengan Pak Budi. Dalam dua bulan terakhir, saya perhatikan banyak mahasiswa yang datang ke jam konsultasi saya, dan sebagian besar mempertanyakan kaitan antara teori yang diajarkan di kelas dengan implementasi di praktikum. Sepertinya ada gap yang cukup besar antara dua sesi tersebut. Mungkin kita perlu menyediakan semacam modul penghubung atau bridging material antara teori dan praktik.

Moderator: Itu poin yang bagus Bu Citra. Sebelum kita bahas solusinya, bagaimana dengan masukan dari sisi mahasiswa? Mas Eko, apakah ada yang ingin disampaikan?

Mahasiswa: Iya, Pak. Terima kasih sudah memberi kesempatan. Dari perspektif kami sebagai mahasiswa, masalah utamanya ada dua hal. Pertama, jadwal praktikum sering bentrok dengan jadwal ujian atau kuis mata kuliah lain sehingga kami kewalahan. Kedua, referensi buku yang digunakan di kelas kadang berbeda dengan modul praktikum, jadi kami bingung mana yang harus dijadikan patokan untuk belajar. Banyak teman yang akhirnya belajar dua versi dan itu sangat melelahkan.

Dosen C: Itu masukan yang sangat berharga, Mas Eko. Berdasarkan apa yang disampaikan, saya usul agar silabus praktikum direvisi dan diselaraskan langsung dengan materi perkuliahan. Kita bisa membuat matriks ketertelusuran, yaitu semacam tabel yang memetakan setiap capaian pembelajaran di kelas dengan modul praktikum yang relevan. Dengan begitu mahasiswa punya panduan yang jelas.

Moderator: Ide yang bagus Pak Dedi. Nanti bisa kita tindaklanjuti dengan membentuk tim kecil untuk merevisi silabus. Sekarang kita masuk ke agenda kedua yaitu usulan mata kuliah baru. Bu Citra sudah mengirimkan draf proposalnya kemarin. Bu Citra, bisa dijelaskan secara singkat poin-poin utamanya?

Dosen B: Tentu Pak. Saya mengusulkan mata kuliah baru bernama Machine Learning Terapan dengan bobot tiga satuan kredit semester. Mata kuliah ini akan mencakup tiga blok materi utama. Blok pertama adalah supervised learning yang meliputi regresi dan klasifikasi. Blok kedua adalah unsupervised learning yang mencakup clustering dan dimensionality reduction. Blok ketiga adalah pengantar neural networks dan deep learning dasar. Prasyarat untuk mengambil mata kuliah ini adalah sudah lulus Matematika Diskrit dan Statistika Dasar.

Dosen A: Saya tertarik dengan proposalnya Bu Citra. Tapi saya punya satu pertanyaan kritis: apakah kita punya cukup sumber daya manusia, dalam hal ini dosen yang kompeten di bidang machine learning? Karena ini bidang yang sangat spesifik dan membutuhkan keahlian yang tidak sembarangan.

Dosen B: Pertanyaan yang sangat relevan Pak Budi. Saya sudah melakukan pemetaan awal. Ada dua dosen yang menurut saya kompeten di bidang ini. Yang pertama adalah saya sendiri dengan latar belakang tesis S3 di bidang computer vision. Yang kedua adalah Pak Hendra dari Jurusan Teknik Elektro yang punya pengalaman riset di machine learning terapan. Kita bisa mengajukan pinjam beban mengajar lintas jurusan.

Dosen C: Oke itu sudah menjawab soal SDM. Tapi bagaimana dengan infrastruktur? Mahasiswa yang belajar machine learning pasti akan butuh komputer dengan kemampuan komputasi tinggi, minimal punya GPU yang cukup untuk melatih model. Kalau pakai CPU biasa, latihannya bisa berjam-jam dan itu tidak efisien untuk perkuliahan.

Mahasiswa: Betul Pak Dedi. Kalau boleh usul, mungkin untuk sementara bisa menggunakan Google Colab yang gratis. Mahasiswa bisa mengakses GPU T4 secara gratis dari Google selama beberapa jam per hari. Itu cukup untuk praktikum skala kecil. Nanti kalau ada anggaran pengadaan baru, laboratorium bisa dilengkapi GPU yang proper.

Moderator: Solusi yang sangat praktis Mas Eko. Oke, saya rasa diskusi kita sudah cukup produktif. Mari kita rangkum keputusan yang kita sepakati hari ini. Untuk agenda pertama terkait Struktur Data: kita akan membentuk tim kecil yang bertugas merevisi silabus praktikum dan menambahkan modul penghubung antara materi teori dan praktik. Tim ini akan terdiri dari Pak Budi, Bu Citra, dan perwakilan mahasiswa. Deadline revisi adalah akhir bulan ini. Untuk agenda kedua terkait Machine Learning Terapan: kita menyetujui proposal ini untuk diajukan ke rapat tingkat fakultas pada bulan depan, dengan catatan bahwa kesiapan infrastruktur berbasis cloud perlu didokumentasikan terlebih dahulu sebagai lampiran proposal. Apakah ada yang ingin menambahkan sebelum rapat kita tutup?

Dosen A: Tidak ada tambahan dari saya. Sudah cukup jelas dan komprehensif.

Dosen B: Saya setuju dengan kesimpulan yang disampaikan. Terima kasih Pak Ketua.

Dosen C: Oke, saya setuju. Terima kasih atas arahannya.

Mahasiswa: Terima kasih banyak atas kesempatan yang diberikan untuk menyampaikan aspirasi kami.

Moderator: Baik. Dengan ini rapat hari ini resmi kita tutup. Notulensi akan didistribusikan ke seluruh peserta paling lambat dua hari kerja setelah rapat ini melalui email resmi prodi. Terima kasih atas partisipasi semua pihak. Sampai jumpa di rapat berikutnya.

---

## NOTULENSI REFERENSI (Ground Truth untuk ROUGE-L)

Dokumen berikut adalah notulensi yang dibuat secara manual dari naskah di atas.
Gunakan ini sebagai **reference summary** dalam perhitungan ROUGE-L.

---

**Pembukaan:**
- Rapat akademik Program Studi Teknik Informatika dibuka oleh Ketua Program Studi, Dr. Ahmad Fauzi, M.T., dengan dua agenda utama: evaluasi pelaksanaan mata kuliah semester genap 2024/2025 dan usulan penambahan mata kuliah kecerdasan buatan.
- Rapat dihadiri oleh tiga dosen dan satu perwakilan mahasiswa BEM Prodi.

**Evaluasi Mata Kuliah Struktur Data:**
- Dr. Budi Santoso melaporkan bahwa nilai rata-rata mahasiswa pada mata kuliah Struktur Data mengalami penurunan sebesar 12% dari rata-rata 72 menjadi 63,4.
- Penyebab diduga adalah beban praktikum yang terlalu padat dan materi yang abstrak bagi mahasiswa semester dua.
- Ibu Citra Dewi mengidentifikasi adanya gap antara materi teori di kelas dan implementasi praktikum berdasarkan frekuensi kunjungan mahasiswa ke jam konsultasi.
- Perwakilan mahasiswa menyampaikan dua masalah utama: jadwal praktikum yang sering bentrok dengan ujian mata kuliah lain, dan ketidaksesuaian referensi antara kelas dan modul praktikum.
- Pak Dedi Wijaya mengusulkan pembuatan matriks ketertelusuran yang memetakan capaian pembelajaran teori dengan modul praktikum yang relevan.

**Usulan Mata Kuliah Machine Learning Terapan:**
- Ibu Citra Dewi mengusulkan mata kuliah Machine Learning Terapan dengan bobot 3 SKS.
- Materi mencakup tiga blok: supervised learning (regresi dan klasifikasi), unsupervised learning (clustering dan dimensionality reduction), serta pengantar neural networks dan deep learning.
- Prasyarat mata kuliah adalah Matematika Diskrit dan Statistika Dasar.
- Sumber daya pengajar: Ibu Citra Dewi (latar belakang computer vision) dan Pak Hendra dari Teknik Elektro (riset machine learning terapan).
- Solusi infrastruktur jangka pendek: penggunaan Google Colab (GPU T4 gratis) untuk praktikum, sambil menunggu pengadaan GPU di laboratorium.

**Pertanyaan dan Diskusi:**
- Pertanyaan: Apakah tersedia dosen yang kompeten di bidang machine learning? — Jawaban: Ada dua dosen yang dapat mengampu, yaitu Ibu Citra Dewi dan Pak Hendra dari Teknik Elektro melalui skema pinjam beban mengajar.
- Pertanyaan: Bagaimana dengan kebutuhan infrastruktur GPU? — Jawaban: Sementara menggunakan Google Colab yang menyediakan akses GPU gratis, sambil merencanakan pengadaan GPU untuk laboratorium.

**Kesimpulan:**
- Untuk mata kuliah Struktur Data: dibentuk tim kecil (Pak Budi, Bu Citra, dan perwakilan mahasiswa) untuk merevisi silabus praktikum dan menambahkan modul penghubung teori-praktik, dengan deadline akhir bulan berjalan.
- Untuk mata kuliah Machine Learning Terapan: proposal disetujui untuk diajukan ke rapat tingkat fakultas bulan depan, dengan syarat kesiapan infrastruktur cloud didokumentasikan sebagai lampiran.

**Penutup:**
- Rapat ditutup oleh Ketua Program Studi.
- Notulensi akan didistribusikan ke seluruh peserta via email resmi prodi paling lambat dua hari kerja setelah rapat.

---

## CARA PENGGUNAAN DALAM PENGUJIAN

### 1. Pengujian WER (Word Error Rate)
```
Reference (R) : Naskah dialog di atas (teks bersih tanpa nama pembicara)
Hypothesis (H): Output transkripsi Whisper dari rekaman audio naskah ini
Tool          : pip install jiwer
```
```python
from jiwer import wer, cer
reference  = "baik rapat kita mulai saya ucapkan terima kasih..."  # naskah bersih
hypothesis = "baik rapat kita mulai saya ucapkan terima kasih..."  # output Whisper
print(f"WER : {wer(reference, hypothesis)*100:.2f}%")
print(f"CER : {cer(reference, hypothesis)*100:.2f}%")
```

### 2. Pengujian ROUGE-L
```
Reference (R) : Notulensi Referensi di atas (ground truth buatan manusia)
Hypothesis (H): Output notulensi dari sistem Notulensia (LexRank + Llama 3.2)
Tool          : pip install rouge-score
```
```python
from rouge_score import rouge_scorer
scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=False)
scores = scorer.score(reference_summary, system_output)
print(f"ROUGE-L Precision : {scores['rougeL'].precision:.4f}")
print(f"ROUGE-L Recall    : {scores['rougeL'].recall:.4f}")
print(f"ROUGE-L F1-Score  : {scores['rougeL'].fmeasure:.4f}")
```

### 3. Cara Mendapatkan Audio dari Naskah
**Opsi A (Recommended):** Minta 3-5 teman membacakan naskah bersama (role-play rapat) → rekam dengan mikrofon → simpan sebagai `.wav`
**Opsi B:** Gunakan TTS (Text-to-Speech) tools seperti ElevenLabs, Google TTS, atau gTTS untuk setiap pembicara → gabungkan audio → simpan sebagai `.mp3`

---
*File ini bagian dari penelitian skripsi "Notulensia — Sistem Notulensi Rapat Otomatis Berbasis AI"*
