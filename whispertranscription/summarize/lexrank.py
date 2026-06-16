"""
lexrank.py — Enhanced LexRank Summarization (6-Step Pipeline)
=============================================================
Pipeline yang dioptimalkan untuk transkrip Whisper Indonesia:

  ┌──────────────────────────────────────────────────────────┐
  │  Step 1: TEXT CLEANING                                   │
  │    → Hapus filler, artefak Whisper, perbaiki typo        │
  │                                                          │
  │  Step 2: SENTENCE SEGMENTATION                           │
  │    → Pecah teks menjadi kalimat utuh & logis             │
  │                                                          │
  │  Step 3: SENTENCE FILTERING                              │
  │    → Buang kalimat noise, deduplikasi                    │
  │                                                          │
  │  Step 4: KEY POINT EXTRACTION (LexRank)                  │
  │    → TF-IDF → Cosine Similarity → Power Iteration       │
  │                                                          │
  │  Step 5: REORGANIZATION                                  │
  │    → Susun: pembukaan → isi → penutup                    │
  │                                                          │
  │  Step 6: FINAL SUMMARIZATION                             │
  │    → Format paragraf bersih, kapitalisasi, tanda baca    │
  └──────────────────────────────────────────────────────────┘
"""

from __future__ import annotations

import re
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .config import SummaryConfig
from .ollama_rewriter import OllamaRewriter


# ══════════════════════════════════════════════════════════════
# Konstanta & Pattern
# ══════════════════════════════════════════════════════════════

# ── Filler words Indonesia & artefak Whisper ──────────────────
_FILLER_WORDS_EXACT = {
    # Interjeksi / filler lisan
    "eh", "ah", "oh", "uh", "um", "em", "eem", "eee", "hmm", "hm",
    "nah", "ya", "yaa", "yaaa", "iya", "iye", "iyaa",
    "gitu", "gitu ya", "gitu lho", "gitu kan",
    "kan", "lho", "lah", "nih", "sih", "deh", "kok", "dong",
    "tuh", "tuh kan",
    "jadi", "jadi ya", "jadi gini",
    "intinya", "pokoknya", "kira-kira",
    "terus", "trus", "kemudian", "lalu",
    "udah", "udah ya", "oke", "oke ya", "oke oke",
    "baik", "baik ya", "baik baik",
    "ayo", "yuk", "yuk yuk",
    # Artefak Whisper (halusinasi umum)
    "terima kasih", "terima kasih telah menonton",
    "terima kasih kerana menonton",
    "subscribe", "like", "komen",
    "musik", "music",
    "recording in progress", "recording stop",
    "...", "…",
}

# Filler di awal kalimat (regex)
_FILLER_START_RE = re.compile(
    r'^(?:(?:nah|ya|jadi|oke|baik|iya|eh|ah|oh|terus|trus|'
    r'gitu|kan|lah|lho|nih|sih|deh|kok|dong|tuh|'
    r'intinya|pokoknya|kemudian|lalu|udah|jadi\s+ya|'
    r'oke\s+ya|baik\s+ya|nah\s+ini|nah\s+itu),?\s*)+',
    re.IGNORECASE,
)

# Filler di akhir kalimat (regex)
_FILLER_END_RE = re.compile(
    r'(?:\s*,?\s*(?:ya|kan|lho|nih|sih|deh|gitu|dong|tuh|'
    r'gitu\s+ya|gitu\s+kan|ya\s+kan))+[.,]?\s*$',
    re.IGNORECASE,
)

# Filler inline (bunyi panjang: eee, aaa, uum, dll)
_FILLER_INLINE_RE = re.compile(
    r'\b(e{2,}|a{2,}|u{2,}|h{2,}m+|[eEaAuU]{3,})\b',
    re.IGNORECASE,
)

# ── Whisper artefak dalam brackets ────────────────────────────
_BRACKET_ARTIFACT_RE = re.compile(r'\[.*?\]')
_PAREN_ARTIFACT_RE = re.compile(r'\(.*?\)')

# ── Pattern kalimat noise (tidak informatif) ──────────────────
_NOISE_PATTERNS = [
    # Kalimat hanya pengulangan satu kata
    re.compile(r'^(\w+)(\s+\1){3,}$', re.IGNORECASE),
    # Kalimat terlalu pendek atau hanya tanda baca/angka
    re.compile(r'^[\W\d\s]{0,15}$'),
    # Kalimat dalam brackets
    re.compile(r'^\[.*?\]$'),
    # Kalimat yang hanya sapaan / filler
    re.compile(
        r'^(halo|hai|hello|oke|baik|silakan|silahkan|'
        r'terima\s+kasih|assalamu|wassalamu|'
        r'ada\s+lagi|ada\s+pertanyaan|'
        r'sebentar|tunggu|tunggu\s+sebentar)[.,!?\s]*$',
        re.IGNORECASE,
    ),
]

# ── Pattern kalimat non-informatif (Q&A, personal, transisi) ──
_NON_INFORMATIVE_PATTERNS = [
    # Kalimat tanya-jawab moderasi
    re.compile(r'ada\s+(yang\s+)?(mau\s+)?(di)?tanya(kan)?', re.IGNORECASE),
    re.compile(r'ada\s+pertanyaan', re.IGNORECASE),
    re.compile(r'silakan\s+(kalau|jika|bila)', re.IGNORECASE),
    re.compile(r'boleh\s+(langsung\s+)?(unmute|tanya|sampaikan)', re.IGNORECASE),
    # Filler transisi tanpa konten
    re.compile(r'^(oke|baik|nah)\s*,?\s*(kita\s+)?(lanjut|lanjutkan|mulai)', re.IGNORECASE),
    # Komentar personal dosen
    re.compile(r'laptop\s+saya', re.IGNORECASE),
    re.compile(r'saya\s+(baru\s+)?lahir', re.IGNORECASE),
    # Artefak recording
    re.compile(r'recording', re.IGNORECASE),
]

# ── Koreksi typo Whisper umum (Bahasa Indonesia) ──────────────
_TYPO_CORRECTIONS = {
    # Whisper sering salah dengar kata-kata ini
    "atml": "HTML",
    "attml": "HTML",
    "html": "HTML",
    "css": "CSS",
    "chess": "CSS",
    "leot": "layout",
    "lewatin": "layout",
    "leotin": "layout",
    "leoting": "layout",
    "larafel": "Laravel",
    "firescoap": "VS Code",
    "fiat squad": "VS Code",
    "meskel": "MySQL",
    "sam": "XAMPP",
    "xam": "XAMPP",
    "peneriti": "peneliti",
    "persyarat": "prasyarat",
    "mataku": "mata kuliah",
    "matakulia": "mata kuliah",
    "attps": "HTTPS",
    "attp": "HTTP",
    "javascript": "JavaScript",
    "php": "PHP",
    "wmkm": "UMKM",
    "umkm": "UMKM",
    "vs code": "VS Code",
    "vscode": "VS Code",
    "bootstrap": "Bootstrap",
    "github": "GitHub",
    "enginex": "Nginx",
    "engine x": "Nginx",
    "apac": "Apache",
    "json": "JSON",
    "wordpress": "WordPress",
    "figma": "Figma",
    "notepad++": "Notepad++",
}

# Konjungsi / frasa transisi untuk split kalimat panjang
_CONJUNCTION_SPLIT_RE = re.compile(
    r',\s*(?=(?:dan|yang|kemudian|selain|namun|tetapi|'
    r'sehingga|karena|jika|agar|bahwa|untuk|dengan|'
    r'sedangkan|sementara|walaupun|meskipun|'
    r'dalam|pada|di|ke|dari)\b)',
    re.IGNORECASE,
)


# ══════════════════════════════════════════════════════════════
# LexRankSummarizer — Enhanced 6-Step Pipeline
# ══════════════════════════════════════════════════════════════

class LexRankSummarizer:
    """
    Extractive summarizer berbasis LexRank, dioptimalkan untuk teks
    hasil Whisper (penuh filler words dan minim tanda baca).

    Pipeline 6 tahap:
      1. Text Cleaning       — bersihkan noise global
      2. Sentence Segmentation — pecah jadi kalimat logis
      3. Sentence Filtering   — buang non-informatif, dedup
      4. Key Point Extraction  — LexRank scoring
      5. Reorganization       — urutkan pembukaan→isi→penutup
      6. Final Summarization  — format paragraf bersih

    Cara pakai:
        cfg = SummaryConfig()
        summarizer = LexRankSummarizer(cfg)
        ringkasan = summarizer.summarize(teks_panjang)
    """

    def __init__(self, cfg: SummaryConfig | None = None):
        self.cfg = cfg or SummaryConfig()
        self.ollama = OllamaRewriter(self.cfg)

    # ══════════════════════════════════════════════════════════
    # Public API
    # ══════════════════════════════════════════════════════════

    def summarize(self, text: str) -> str:
        """
        Ringkas teks Whisper menggunakan 6-step pipeline.
        Return string ringkasan dalam format paragraf yang bersih.
        """
        return self.summarize_with_debug(text)['ringkasan']

    def summarize_with_debug(self, text: str) -> dict:
        """
        Sama dengan summarize(), tapi juga mengembalikan data debug
        perangkingan LexRank untuk ditampilkan di frontend.

        Return:
            {
              'ringkasan': str,
              'ranked_sentences': [
                  {'rank': 1, 'score': 0.92, 'sentence': '...'},
                  ...
              ]
            }
        """
        if not text or len(text.strip()) < 50:
            return {'ringkasan': text.strip(), 'ranked_sentences': []}

        # ── Step 1: Text Cleaning ─────────────────────────────
        cleaned = self._step1_text_cleaning(text)

        if len(cleaned.strip()) < 50:
            return {'ringkasan': cleaned.strip(), 'ranked_sentences': []}

        # ── Step 2: Sentence Segmentation ─────────────────────
        raw_sentences = self._step2_sentence_segmentation(cleaned)

        if not raw_sentences:
            return {'ringkasan': self._polish_sentence(cleaned[:500]), 'ranked_sentences': []}

        # ── Step 3: Sentence Filtering ────────────────────────
        filtered = self._step3_sentence_filtering(raw_sentences)

        if not filtered:
            raw_sentences.sort(key=len, reverse=True)
            target = max(self.cfg.min_sentences, min(8, len(raw_sentences)))
            filtered = raw_sentences[:target]

        # ── HITUNG TARGET DINAMIS (Dynamic Adaptation) ───────
        target_sentences = int(len(filtered) * self.cfg.compression_ratio)
        target_sentences = max(self.cfg.min_sentences, min(target_sentences, self.cfg.max_sentences))

        # ── Debug: perangkingan LexRank ───────────────────────
        ranked_sentences = []

        if len(filtered) <= target_sentences:
            organized = filtered
            # Semua kalimat dianggap sama penting
            for i, s in enumerate(filtered):
                ranked_sentences.append({'rank': i + 1, 'score': 1.0, 'sentence': s})
        else:
            # ── Step 4: Key Point Extraction (LexRank) ────────
            top_sentences, top_indices = self._step4_lexrank_extraction(filtered, target=target_sentences)

            # Hitung ulang skor seluruh kalimat untuk debug panel
            try:
                tfidf_matrix = self._build_tfidf_matrix(filtered)
                if tfidf_matrix is not None:
                    sim_matrix = self._build_similarity_matrix(tfidf_matrix)
                    scores = self._power_iteration(sim_matrix)
                    # Urutkan semua kalimat dari skor tertinggi
                    sorted_idx = np.argsort(scores)[::-1].tolist()
                    for rank, idx in enumerate(sorted_idx):
                        ranked_sentences.append({
                            'rank': rank + 1,
                            'score': round(float(scores[idx]), 4),
                            'sentence': filtered[idx],
                        })
                else:
                    for i, s in enumerate(top_sentences):
                        ranked_sentences.append({'rank': i + 1, 'score': 0.0, 'sentence': s})
            except Exception:
                for i, s in enumerate(top_sentences):
                    ranked_sentences.append({'rank': i + 1, 'score': 0.0, 'sentence': s})

            # ── Step 5: Reorganization ────────────────────────
            organized = self._step5_reorganize(top_sentences, top_indices, len(filtered))

        # ── Step 6: Final Summarization ───────────────────────
        if self.ollama.is_available():
            print("[LexRank] Memanggil Ollama untuk abstractive rewriting...", flush=True)
            rewritten = self.ollama.rewrite(organized, full_context=cleaned)
            if rewritten:
                return {'ringkasan': rewritten, 'ranked_sentences': ranked_sentences}

        # Fallback jika Ollama down/gagal
        ringkasan = self._step6_final_format(organized)
        return {'ringkasan': ringkasan, 'ranked_sentences': ranked_sentences}


    # ══════════════════════════════════════════════════════════
    # Step 1: TEXT CLEANING
    # ══════════════════════════════════════════════════════════

    def _step1_text_cleaning(self, text: str) -> str:
        """
        Bersihkan teks Whisper secara global:
        - Hapus karakter non-printable
        - Hapus artefak Whisper (brackets, halusinasi)
        - Hapus filler inline
        - Koreksi typo umum
        - Normalisasi spasi & tanda baca
        """
        # 1a. Hapus karakter non-printable
        text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', ' ', text)

        # 1b. Hapus artefak Whisper dalam brackets
        text = _BRACKET_ARTIFACT_RE.sub(' ', text)
        text = _PAREN_ARTIFACT_RE.sub(' ', text)

        # 1c. Hapus artefak halusinasi Whisper (frasa lengkap)
        for artifact in self.cfg.extra_whisper_artifacts:
            text = re.sub(re.escape(artifact), ' ', text, flags=re.IGNORECASE)

        # Juga hapus yang hardcoded
        for artifact in _FILLER_WORDS_EXACT:
            if len(artifact) > 15:  # Hanya frasa panjang
                text = re.sub(
                    r'\b' + re.escape(artifact) + r'\b',
                    ' ', text, flags=re.IGNORECASE
                )

        # 1d. Hapus bunyi filler inline (eee, aaa, uum, dll)
        text = _FILLER_INLINE_RE.sub('', text)

        # 1e. Normalisasi tanda baca ganda
        text = re.sub(r'\.{2,}', '.', text)
        text = re.sub(r'\?{2,}', '?', text)
        text = re.sub(r'!{2,}', '!', text)
        text = re.sub(r',{2,}', ',', text)

        # 1f. Hapus pengulangan kata berturut (>2x)
        text = re.sub(r'\b(\w+)(\s+\1){2,}\b', r'\1', text, flags=re.IGNORECASE)

        # 1g. Koreksi typo Whisper umum
        text = self._apply_typo_corrections(text)

        # 1h. Normalisasi spasi
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def _apply_typo_corrections(self, text: str) -> str:
        """Koreksi typo Whisper yang umum untuk Bahasa Indonesia."""
        for wrong, correct in _TYPO_CORRECTIONS.items():
            # Case-insensitive word-boundary replacement
            pattern = re.compile(r'\b' + re.escape(wrong) + r'\b', re.IGNORECASE)
            text = pattern.sub(correct, text)
        return text

    # ══════════════════════════════════════════════════════════
    # Step 2: SENTENCE SEGMENTATION
    # ══════════════════════════════════════════════════════════

    def _step2_sentence_segmentation(self, text: str) -> list[str]:
        """
        Tokenisasi kalimat cerdas untuk teks Whisper:
        - Split di tanda baca standar (.!?)
        - Pecah kalimat terlalu panjang di konjungsi/koma
        - Gabungkan fragmen terlalu pendek dengan kalimat sebelumnya
        """
        # 2a. Split di tanda baca standar
        parts = re.split(r'(?<=[.!?])\s+', text)

        # 2b. Pecah segmen yang terlalu panjang
        segments = []
        max_words = self.cfg.max_words_per_segment

        for part in parts:
            words = part.split()
            if len(words) <= max_words:
                segments.append(part.strip())
            else:
                # Coba split di koma + konjungsi
                sub = _CONJUNCTION_SPLIT_RE.split(part)
                if len(sub) > 1:
                    segments.extend(s.strip() for s in sub if s.strip())
                else:
                    # Fallback: potong tiap ~40 kata di koma
                    self._chunk_long_segment(words, segments)

        # 2c. Gabungkan fragmen terlalu pendek dengan sebelumnya
        merged = self._merge_short_fragments(segments)

        return [s.strip() for s in merged if s.strip()]

    def _chunk_long_segment(self, words: list[str], output: list[str]):
        """Pecah kata-kata panjang jadi chunk ~40 kata di titik koma."""
        buf = []
        for w in words:
            buf.append(w)
            if len(buf) >= 40 and (w.endswith(',') or w.endswith('.')):
                output.append(' '.join(buf))
                buf = []
        if buf:
            output.append(' '.join(buf))

    def _merge_short_fragments(self, segments: list[str]) -> list[str]:
        """Gabungkan fragmen < min_words dengan kalimat sebelumnya."""
        if not segments:
            return segments

        min_w = self.cfg.min_words_per_sentence
        merged = [segments[0]]

        for seg in segments[1:]:
            words = seg.split()
            if len(words) < min_w and merged:
                # Gabung ke kalimat sebelumnya
                merged[-1] = merged[-1].rstrip('.!?, ') + ', ' + seg
            else:
                merged.append(seg)

        return merged

    # ══════════════════════════════════════════════════════════
    # Step 3: SENTENCE FILTERING
    # ══════════════════════════════════════════════════════════

    def _step3_sentence_filtering(self, sentences: list[str]) -> list[str]:
        """
        Bersihkan & filter kalimat:
        - Hapus filler di awal/akhir
        - Buang kalimat noise / non-informatif
        - Deduplikasi (Jaccard overlap)
        - Buang kalimat terlalu pendek
        """
        result = []
        seen_word_sets = []

        for s in sentences:
            # 3a. Bersihkan kalimat individual
            cleaned = self._clean_single_sentence(s)

            # 3b. Filter: terlalu pendek
            if len(cleaned.split()) < self.cfg.min_words_per_sentence:
                continue

            # 3c. Filter: kurang karakter informatif
            if len(cleaned) < self.cfg.min_informative_chars:
                continue

            # 3d. Filter: pattern noise
            if any(p.search(cleaned) for p in _NOISE_PATTERNS):
                continue

            # 3e. Filter: non-informatif (Q&A, personal, transisi)
            if any(p.search(cleaned) for p in _NON_INFORMATIVE_PATTERNS):
                continue

            # 3f. Filter: deduplikasi (Jaccard overlap)
            word_set = frozenset(cleaned.lower().split())
            is_dup = False
            for existing_set in seen_word_sets:
                intersection = len(word_set & existing_set)
                union = len(word_set | existing_set)
                if union > 0 and intersection / union > self.cfg.dedup_threshold:
                    is_dup = True
                    break

            if is_dup:
                continue

            seen_word_sets.append(word_set)
            result.append(cleaned)

        return result

    def _clean_single_sentence(self, sentence: str) -> str:
        """Bersihkan satu kalimat: hapus filler, rapikan tanda baca."""

        # Hapus filler di awal
        sentence = _FILLER_START_RE.sub('', sentence).strip()

        # Hapus koma/spasi berlebih di awal
        sentence = re.sub(r'^[,\s]+', '', sentence)

        # Hapus filler di akhir
        sentence = _FILLER_END_RE.sub('', sentence).strip()

        # Rapikan spasi di sekitar tanda baca
        sentence = re.sub(r'\s+([.,!?])', r'\1', sentence)
        sentence = re.sub(r'([.,!?]){2,}', r'\1', sentence)

        # Hapus spasi ganda
        sentence = re.sub(r'\s+', ' ', sentence).strip()

        # Pastikan diakhiri titik
        if sentence and sentence[-1] not in '.!?':
            sentence += '.'

        # Kapitalisasi huruf pertama
        if sentence:
            sentence = sentence[0].upper() + sentence[1:]

        return sentence.strip()

    # ══════════════════════════════════════════════════════════
    # Step 4: KEY POINT EXTRACTION (LexRank)
    # ══════════════════════════════════════════════════════════

    def _step4_lexrank_extraction(
        self, sentences: list[str], target: int
    ) -> tuple[list[str], list[int]]:
        """
        LexRank: TF-IDF → Cosine Similarity → Power Iteration.
        Return (top_sentences, top_indices_dalam_list_asli).
        """
        # 4a. Bangun TF-IDF matrix
        tfidf_matrix = self._build_tfidf_matrix(sentences)

        if tfidf_matrix is None:
            # Fallback: ambil kalimat terpanjang
            n = min(target, len(sentences))
            indices = sorted(
                range(len(sentences)),
                key=lambda i: len(sentences[i]),
                reverse=True,
            )[:n]
            indices.sort()  # Kembalikan ke urutan asli
            return [sentences[i] for i in indices], indices

        # 4b. Similarity matrix
        sim_matrix = self._build_similarity_matrix(tfidf_matrix)

        # 4c. Power iteration (LexRank scores)
        scores = self._power_iteration(sim_matrix)

        # 4d. Ambil top-N, urutkan sesuai posisi asli
        n = min(target, len(sentences))
        top_indices = sorted(np.argsort(scores)[-n:].tolist())
        top_sentences = [sentences[i] for i in top_indices]

        return top_sentences, top_indices

    def _build_tfidf_matrix(self, sentences: list[str]):
        """Bangun TF-IDF matrix. Return None jika gagal."""
        try:
            # Indonesian stop words dasar
            indo_stop = {
                'yang', 'di', 'ke', 'dari', 'ini', 'itu', 'dan', 'atau',
                'dengan', 'untuk', 'pada', 'ada', 'akan', 'juga', 'sudah',
                'bisa', 'tidak', 'kalau', 'kita', 'saya', 'mereka', 'dia',
                'apa', 'itu', 'ini', 'lagi', 'lebih', 'harus', 'bisa',
                'mau', 'pakai', 'pake', 'kalian', 'nya', 'tadi', 'nanti',
                'misalnya', 'tentunya', 'memang', 'masih', 'udah', 'pun',
            }
            vectorizer = TfidfVectorizer(
                min_df=1,
                max_df=0.90,
                token_pattern=r"(?u)\b\w{2,}\b",
                sublinear_tf=True,
                ngram_range=(1, 2),
                stop_words=list(indo_stop),
            )
            return vectorizer.fit_transform(sentences)
        except Exception:
            return None

    def _build_similarity_matrix(self, tfidf_matrix) -> np.ndarray:
        """Cosine similarity → adjacency matrix dengan threshold."""
        sim = cosine_similarity(tfidf_matrix)
        np.fill_diagonal(sim, 0.0)
        sim[sim < self.cfg.similarity_threshold] = 0.0

        # Normalisasi row-stochastic
        row_sums = sim.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1.0
        return sim / row_sums

    def _power_iteration(self, sim_matrix: np.ndarray) -> np.ndarray:
        """LexRank power iteration (seperti PageRank)."""
        n = sim_matrix.shape[0]
        d = self.cfg.damping
        scores = np.ones(n) / n

        for _ in range(self.cfg.max_iter):
            new_scores = (1 - d) / n + d * sim_matrix.T.dot(scores)
            if np.linalg.norm(new_scores - scores) < self.cfg.convergence_threshold:
                break
            scores = new_scores

        return scores

    # ══════════════════════════════════════════════════════════
    # Step 5: REORGANIZATION
    # ══════════════════════════════════════════════════════════

    def _step5_reorganize(
        self,
        sentences: list[str],
        original_indices: list[int],
        total_sentences: int,
    ) -> list[str]:
        """
        Susun kalimat terpilih agar membentuk alur logis:
          - Pembukaan (kalimat dari 1/3 awal teks)
          - Isi (kalimat dari 1/3 tengah)
          - Penutup (kalimat dari 1/3 akhir)

        Kalimat sudah diurutkan berdasarkan posisi asli dari step 4,
        jadi urutan natural sudah terjaga. Di sini kita pastikan
        ada representasi dari setiap bagian.
        """
        if len(sentences) <= 3:
            return sentences

        # Bagi menjadi 3 zona berdasarkan posisi asli
        third = max(1, total_sentences // 3)

        opening = []
        body = []
        closing = []

        for sent, idx in zip(sentences, original_indices):
            if idx < third:
                opening.append(sent)
            elif idx < third * 2:
                body.append(sent)
            else:
                closing.append(sent)

        # Susun: pembukaan → isi → penutup
        organized = opening + body + closing

        return organized if organized else sentences

    # ══════════════════════════════════════════════════════════
    # Step 6: FINAL SUMMARIZATION (Format Output)
    # ══════════════════════════════════════════════════════════

    def _step6_final_format(self, sentences: list[str]) -> str:
        """
        Format kalimat terpilih menjadi paragraf bersih:
        - Kelompokkan per N kalimat (configurable)
        - Pastikan setiap kalimat sudah rapi
        - Gabung menjadi paragraf koheren
        """
        if not sentences:
            return ""

        # Polish setiap kalimat
        polished = [self._polish_sentence(s) for s in sentences]
        polished = [s for s in polished if s]  # Buang yang kosong

        if not polished:
            return ""

        # Group kalimat per paragraf
        group_size = self.cfg.sentences_per_paragraph
        paragraphs = []

        for i in range(0, len(polished), group_size):
            group = polished[i: i + group_size]
            para = ' '.join(group)
            paragraphs.append(para)

        return '\n\n'.join(paragraphs)

    def _polish_sentence(self, sentence: str) -> str:
        """Final polish: kapitalisasi, tanda baca, trim."""
        sentence = sentence.strip()
        if not sentence:
            return ""

        # Hapus spasi ganda
        sentence = re.sub(r'\s+', ' ', sentence)

        # Rapikan tanda baca
        sentence = re.sub(r'\s+([.,!?])', r'\1', sentence)
        sentence = re.sub(r'([.,!?]){2,}', r'\1', sentence)

        # Hapus koma di awal
        sentence = re.sub(r'^[,\s]+', '', sentence)

        # Pastikan diakhiri titik
        if sentence and sentence[-1] not in '.!?':
            sentence += '.'

        # Kapitalisasi
        if sentence:
            sentence = sentence[0].upper() + sentence[1:]

        return sentence.strip()
