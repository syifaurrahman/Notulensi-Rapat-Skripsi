# Landasan Teoretis dan Rumus Evaluasi Sistem Notulensi Rapat Otomatis

Dokumen ini berisi rangkuman seluruh rumus matematika, definisi variabel, penjelasan metrik, serta rujukan jurnal ilmiah internasional yang digunakan sebagai dasar evaluasi akurasi, korelasi, dan ketepatan ringkasan pada sistem notulensi rapat otomatis Anda.

---

## 1. Evaluasi Akurasi Transkripsi Suara (Model Whisper)
Evaluasi ini digunakan untuk mengukur kinerja transkripsi otomatis *speech-to-text* (hipotesis) terhadap hasil transkripsi manual (referensi/*ground truth*).

### A. Word Error Rate (WER)
WER menghitung persentase kesalahan transkripsi pada tingkat kata berdasarkan jumlah operasi pengeditan minimum yang diperlukan untuk mengubah teks transkripsi otomatis menjadi transkrip acuan manual.

#### **Rumus:**
$$WER = \frac{S + D + I}{N}$$

#### **Definisi Variabel:**
*   $S$ *(Substitution)*: Jumlah kata yang salah dikenali dan digantikan oleh kata lain (misal: "maka" ditulis "akan").
*   $D$ *(Deletion)*: Jumlah kata dalam referensi yang hilang atau terlewatkan pada hasil transkripsi otomatis.
*   $I$ *(Insertion)*: Jumlah kata tambahan yang muncul pada transkripsi otomatis namun tidak ada dalam referensi.
*   $N$ *(Total Words)*: Jumlah total kata keseluruhan yang ada pada transkrip referensi manual.

---

### B. Word Accuracy (WAcc)
WAcc mengukur persentase kata yang ditranskripsikan secara benar oleh sistem. Nilai WAcc didapatkan dari komplemen nilai WER (dibatasi minimal bernilai $0$ jika jumlah penyisipan sangat tinggi).

#### **Rumus:**
$$WAcc = 1 - WER = \frac{N - (S + D + I)}{N}$$

---

### C. Character Error Rate (CER)
CER memiliki konsep pengerjaan yang identik dengan WER, namun perhitungannya dilakukan pada level **karakter huruf** (spasi kosong biasanya diabaikan). CER digunakan karena lebih ketat dan dapat merepresentasikan tingkat kesalahan ejaan (*typo*) huruf demi huruf secara lebih mendalam.

#### **Rumus:**
$$CER = \frac{S_{\text{char}} + D_{\text{char}} + I_{\text{char}}}{N_{\text{char}}}$$

#### **Definisi Variabel:**
*   $S_{\text{char}}$: Jumlah karakter yang mengalami substitusi/salah eja huruf.
*   $D_{\text{char}}$: Jumlah karakter referensi yang hilang.
*   $I_{\text{char}}$: Jumlah karakter tambahan yang disisipkan.
*   $N_{\text{char}}$: Jumlah total karakter keseluruhan pada berkas referensi manual.

> [!NOTE]
> **Rujukan Jurnal Utama:**
> *   **NIST (National Institute of Standards and Technology)**. *Speech Recognition Scoring Toolkit (SCTK)*. NIST menyusun standardisasi WER dan CER sebagai tolok ukur baku pengujian mesin ASR sejak awal dekade 1980-an.
> *   **Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey, C., & Sutskever, I. (2023)**. *"Robust Speech Recognition via Large-Scale Weak Supervision"*. *Proceedings of the 40th International Conference on Machine Learning (ICML)*. Jurnal resmi OpenAI Whisper yang menguji performa model Whisper menggunakan metrik WER dan CER.

---

## 2. Uji Korelasi Ringkasan Ekstraktif (LexRank) dng Transkrip Asli
Pengujian korelasi digunakan untuk mengukur seberapa representatif kalimat-kalimat penting yang diekstrak oleh algoritma LexRank terhadap keseluruhan isi transkrip rapat.

### A. Cosine Similarity (TF-IDF)
Mengukur kemiripan arah sudut antara vektor frekuensi kata ringkasan ($A$) dan vektor dokumen transkrip asli ($B$) menggunakan pembobotan TF-IDF (*Term Frequency-Inverse Document Frequency*).

#### **Rumus:**
$$\text{Cosine}(A, B) = \frac{A \cdot B}{\|A\| \|B\|} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$

#### **Definisi Variabel:**
*   $A_i$: Bobot TF-IDF kata ke-$i$ pada ringkasan LexRank.
*   $B_i$: Bobot TF-IDF kata ke-$i$ pada transkrip rapat asli.
*   $n$: Jumlah kosakata unik keseluruhan gabungan dari kedua dokumen.

---

### B. Jaccard Similarity
Mengukur tingkat tumpang tindih (*overlap*) kosakata unik yang digunakan antara ringkasan LexRank ($A$) dan dokumen transkrip asli ($B$).

#### **Rumus:**
$$\text{Jaccard}(A, B) = \frac{|A \cap B|}{|A \cup B|}$$

#### **Definisi Variabel:**
*   $|A \cap B|$: Jumlah kosakata unik yang muncul di **kedua** dokumen (irisan).
*   $|A \cup B|$: Jumlah total kosakata unik gabungan dari dokumen ringkasan dan transkrip asli (gabungan).

---

### C. Sentence Coverage
Mengukur persentase kalimat ringkasan LexRank yang benar-benar merupakan kutipan murni dari transkrip asli untuk menjamin tingkat *faithfulness* (pencegahan kalimat fiktif/halusinasi).

#### **Rumus:**
$$\text{Sentence Coverage} = \frac{\text{Jumlah Kalimat Ringkasan yang Lolos Validasi}}{\text{Total Kalimat pada Ringkasan}}$$

---

### D. Compression Ratio
Mengukur efektivitas kompresi atau tingkat kepadatan ringkasan yang dihasilkan dibandingkan dengan panjang dokumen asli.

#### **Rumus:**
$$\text{Compression Ratio} = \frac{\text{Jumlah Token pada Ringkasan LexRank}}{\text{Jumlah Token pada Transkrip Rapat Asli}}$$

---

### E. Rata-rata Korelasi
Rata-rata korelasi dihitung dari 4 metrik utama untuk mendapatkan nilai tunggal yang merepresentasikan korelasi ringkasan secara komprehensif.

#### **Rumus:**
$$\text{Rata-rata Korelasi} = \frac{\text{Cosine} + \text{Jaccard} + \text{Token Retention} + \text{Sentence Coverage}}{4}$$

> [!NOTE]
> **Rujukan Jurnal Utama:**
> *   **Erkan, G., & Radev, D. R. (2004)**. *"LexRank: Graph-based Lexical Centrality as Salience in Text Summarization"*. *Journal of Artificial Intelligence Research (JAIR)*, 22, 457-479. Paper asli penemuan algoritma LexRank berbasis graf kemiripan Cosine TF-IDF.
> *   **Manning, C. D., Raghavan, P., & Schütze, H. (2008)**. *"Introduction to Information Retrieval"*. *Cambridge University Press*. Rujukan dasar untuk perhitungan Cosine TF-IDF dan Jaccard Similarity pada temu kembali informasi.

---

## 3. Uji Ketepatan Ringkasan / Summarization Accuracy (Ollama vs LexRank)
Pengujian ROUGE (*Recall-Oriented Understudy for Gisting Evaluation*) digunakan untuk membandingkan kecocokan notulensi akhir LLM (Ollama - sebagai hipotesis) terhadap referensi poin kunci (LexRank - sebagai acuan).

### A. ROUGE-N (ROUGE-1 & ROUGE-2)
ROUGE-N menghitung persentase tumpang tindih unit n-gram (unigram/kata tunggal pada ROUGE-1, dan bigram/pasangan kata berurutan pada ROUGE-2).

#### **Rumus:**
$$\text{Recall}_{\text{ROUGE-N}} = \frac{\sum_{S \in Ref} \sum_{gram_n \in S} Count_{match}(gram_n)}{\sum_{S \in Ref} \sum_{gram_n \in S} Count(gram_n)}$$

$$\text{Precision}_{\text{ROUGE-N}} = \frac{\sum_{S \in Hyp} \sum_{gram_n \in S} Count_{match}(gram_n)}{\sum_{S \in Hyp} \sum_{gram_n \in S} Count(gram_n)}$$

$$\text{F1-Score}_{\text{ROUGE-N}} = \frac{2 \times \text{Precision}_{\text{ROUGE-N}} \times \text{Recall}_{\text{ROUGE-N}}}{\text{Precision}_{\text{ROUGE-N}} + \text{Recall}_{\text{ROUGE-N}}}$$

#### **Definisi Variabel:**
*   $Ref$: Ringkasan referensi (LexRank).
*   $Hyp$: Ringkasan sistem (Ollama).
*   $gram_n$: Rangkaian $n$ kata berurutan (1 kata untuk ROUGE-1, 2 kata untuk ROUGE-2).
*   $Count_{match}(gram_n)$: Jumlah maksimum n-gram yang muncul bersamaan di dokumen acuan dan hipotesis.

---

### B. ROUGE-L (Longest Common Subsequence)
ROUGE-L didasarkan pada perhitungan *Longest Common Subsequence* (LCS), yaitu urutan kata terpanjang yang sama di antara kedua dokumen. Kelebihannya adalah tidak menuntut kecocokan kata berurutan secara kaku, sehingga sangat cocok mengevaluasi hasil ringkasan abstrak yang susunan kalimatnya dinamis.

#### **Rumus:**
$$\text{Recall}_{\text{LCS}} = \frac{\text{LCS}(Ref, Hyp)}{Length(Ref)}$$

$$\text{Precision}_{\text{LCS}} = \frac{\text{LCS}(Ref, Hyp)}{Length(Hyp)}$$

$$\text{F1-Score}_{\text{ROUGE-L}} = \frac{(1 + \beta^2) \times \text{Precision}_{\text{LCS}} \times \text{Recall}_{\text{LCS}}}{\text{Recall}_{\text{LCS}} + (\beta^2 \times \text{Precision}_{\text{LCS}})}$$

#### **Definisi Variabel:**
*   $\text{LCS}(Ref, Hyp)$: Panjang urutan kata terpanjang yang sama antara ringkasan referensi dan sistem.
*   $Length(Ref)$ / $Length(Hyp)$: Jumlah total kata pada berkas referensi dan sistem.
*   $\beta$: Bobot relatif Precision dan Recall. Umumnya diset bernilai $1$ (ROUGE F1-Score biasa).

> [!NOTE]
> **Rujukan Jurnal Utama:**
> *   **Lin, C. Y. (2004)**. *"ROUGE: A Package for Automatic Evaluation of Summaries"*. *Text Summarization Branches Out*, 74-81. Jurnal ilmiah pertama yang memperkenalkan paket metrik evaluasi ROUGE yang menjadi standar global di seluruh jurnal NLP.
