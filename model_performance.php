<?php
require_once 'cek_login.php';

// Hanya Admin (level = 1) yang boleh mengakses halaman ini
if ($level_user != 1) {
    header("Location: dashboard.php");
    exit();
}
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notulensia · Performa Model</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/style.css">
    <link rel="stylesheet" href="assets/css/model_performance.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        /* Modern Tab Bar Styling */
        .mp-tabs {
            display: flex;
            gap: 8px;
            margin-bottom: 24px;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 8px;
            overflow-x: auto;
        }
        .mp-tab-btn {
            background: none;
            border: none;
            padding: 10px 18px;
            font-size: 0.9rem;
            font-weight: 600;
            color: #64748b;
            cursor: pointer;
            border-radius: 8px 8px 0 0;
            transition: all 0.2s;
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .mp-tab-btn:hover {
            color: #1e3a5f;
            background: #f1f5f9;
        }
        .mp-tab-btn.active {
            color: #3b82f6;
            border-bottom: 3px solid #3b82f6;
            background: #eff6ff;
        }
        .mp-tab-content {
            display: none;
        }
        .mp-tab-content.active {
            display: block;
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Image Display Styling */
        .mp-image-card {
            background: #ffffff;
            border-radius: 20px;
            padding: 20px;
            border: 1px solid #ecf2f9;
            box-shadow: 0 6px 18px -10px rgba(0,45,85,0.07);
            margin-bottom: 24px;
            text-align: center;
        }
        .mp-image-card img {
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            box-shadow: 0 4px 14px rgba(0,45,85,0.08);
            transition: transform 0.3s;
        }
        .mp-image-card img:hover {
            transform: scale(1.01);
        }
        .mp-image-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: #1e3a5f;
            margin-bottom: 12px;
            text-align: left;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Grid Layouts for Metrik */
        .mp-grid-3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 20px;
        }
        .mp-grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }

        @media (max-width: 992px) {
            .mp-grid-3 { grid-template-columns: 1fr; }
            .mp-grid-2 { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>

<?php include 'sidebar.php'; ?>

<main class="main-content">
    <!-- Top Bar -->
    <div class="top-bar">
        <div class="page-title">
            <h1>Performa Model</h1>
            <p>Hasil evaluasi metrik visual dan pengujian sistem Notulensi Rapat</p>
        </div>
        <div class="header-date">
            <i class="fas fa-calendar-check"></i>
            <span id="realtime-clock"></span>
        </div>
    </div>

    <!-- Tab Navigation -->
    <div class="mp-tabs">
        <button class="mp-tab-btn active" onclick="switchTab(event, 'tab-whisper')">
            <i class="fas fa-microphone-lines"></i> ASR Whisper
        </button>
        <button class="mp-tab-btn" onclick="switchTab(event, 'tab-filters')">
            <i class="fas fa-filter"></i> Preprocessing Filters
        </button>
        <button class="mp-tab-btn" onclick="switchTab(event, 'tab-nlp')">
            <i class="fas fa-brain"></i> NLP & Summarization
        </button>
    </div>

    <!-- ══════════════════════════════════════════════
         TAB 1: ASR WHISPER
    ══════════════════════════════════════════════ -->
    <div id="tab-whisper" class="mp-tab-content active">
        <!-- Live vs Upload KPI -->
        <div class="mp-grid-2">
            <!-- PANEL LIVE -->
            <div style="background:#fff; border-radius:18px; border:1.5px solid #bae6fd; padding:22px 24px; box-shadow:0 2px 12px rgba(2,132,199,.07);">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:18px;">
                    <div style="width:36px;height:36px;border-radius:10px;background:#e0f2fe;display:flex;align-items:center;justify-content:center;color:#0284c7;font-size:1rem;">
                        <i class="fas fa-broadcast-tower"></i>
                    </div>
                    <div>
                        <div style="font-weight:700;font-size:1rem;color:#0a1c32;">Live Transcription (Average)</div>
                        <div style="font-size:0.75rem;color:#64748b;">4 Dataset Podcast Live Streaming</div>
                    </div>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px;">
                    <div style="background:#f0f9ff;border-radius:12px;padding:14px 12px;border:1px solid #bae6fd;text-align:center;">
                        <div style="font-size:0.7rem;font-weight:600;color:#0369a1;text-transform:uppercase;margin-bottom:6px;">WER</div>
                        <div id="live-wer" style="font-size:1.5rem;font-weight:700;color:#0a1c32;">55.32%</div>
                        <div style="font-size:0.68rem;color:#64748b;margin-top:3px;">↓ Lebih kecil = baik</div>
                    </div>
                    <div style="background:#f0fdf4;border-radius:12px;padding:14px 12px;border:1px solid #86efac;text-align:center;">
                        <div style="font-size:0.7rem;font-weight:600;color:#15803d;text-transform:uppercase;margin-bottom:6px;">WAcc</div>
                        <div id="live-wacc" style="font-size:1.5rem;font-weight:700;color:#0a1c32;">44.68%</div>
                        <div style="font-size:0.68rem;color:#64748b;margin-top:3px;">↑ Lebih besar = baik</div>
                    </div>
                    <div style="background:#faf5ff;border-radius:12px;padding:14px 12px;border:1px solid #d8b4fe;text-align:center;">
                        <div style="font-size:0.7rem;font-weight:600;color:#7c3aed;text-transform:uppercase;margin-bottom:6px;">CER</div>
                        <div id="live-cer" style="font-size:1.5rem;font-weight:700;color:#0a1c32;">43.10%</div>
                        <div style="font-size:0.68rem;color:#64748b;margin-top:3px;">↓ Lebih kecil = baik</div>
                    </div>
                </div>
            </div>

            <!-- PANEL UPLOAD -->
            <div style="background:#fff; border-radius:18px; border:1.5px solid #fde68a; padding:22px 24px; box-shadow:0 2px 12px rgba(217,119,6,.07);">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:18px;">
                    <div style="width:36px;height:36px;border-radius:10px;background:#fef3c7;display:flex;align-items:center;justify-content:center;color:#d97706;font-size:1rem;">
                        <i class="fas fa-cloud-arrow-up"></i>
                    </div>
                    <div>
                        <div style="font-weight:700;font-size:1rem;color:#0a1c32;">Upload File (Average)</div>
                        <div style="font-size:0.75rem;color:#64748b;">9 Dataset Upload Rekaman Rapat</div>
                    </div>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px;">
                    <div style="background:#fffbeb;border-radius:12px;padding:14px 12px;border:1px solid #fde68a;text-align:center;">
                        <div style="font-size:0.7rem;font-weight:600;color:#b45309;text-transform:uppercase;margin-bottom:6px;">WER</div>
                        <div id="upload-wer" style="font-size:1.5rem;font-weight:700;color:#0a1c32;">17.26%</div>
                        <div style="font-size:0.68rem;color:#64748b;margin-top:3px;">↓ Lebih kecil = baik</div>
                    </div>
                    <div style="background:#f0fdf4;border-radius:12px;padding:14px 12px;border:1px solid #86efac;text-align:center;">
                        <div style="font-size:0.7rem;font-weight:600;color:#15803d;text-transform:uppercase;margin-bottom:6px;">WAcc</div>
                        <div id="upload-wacc" style="font-size:1.5rem;font-weight:700;color:#0a1c32;">82.74%</div>
                        <div style="font-size:0.68rem;color:#64748b;margin-top:3px;">↑ Lebih besar = baik</div>
                    </div>
                    <div style="background:#faf5ff;border-radius:12px;padding:14px 12px;border:1px solid #d8b4fe;text-align:center;">
                        <div style="font-size:0.7rem;font-weight:600;color:#7c3aed;text-transform:uppercase;margin-bottom:6px;">CER</div>
                        <div id="upload-cer" style="font-size:1.5rem;font-weight:700;color:#0a1c32;">10.71%</div>
                        <div style="font-size:0.68rem;color:#64748b;margin-top:3px;">↓ Lebih kecil = baik</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Whisper Compare Chart -->
        <div class="mp-chart-row" style="grid-template-columns:1fr;">
            <div class="mp-chart-card">
                <div class="mp-chart-header">
                    <i class="fas fa-chart-bar" style="color:#0284c7;"></i>
                    <span>Perbandingan Metrik Rata-rata Whisper</span>
                </div>
                <div class="mp-chart-wrap" style="height:250px;">
                    <canvas id="whisperCompareChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Whisper Per-Topic Detail Image -->
        <div class="mp-image-card">
            <div class="mp-image-title">
                <i class="fas fa-chart-line" style="color:#4CAF50;"></i>
                <span>Distribusi Akurasi Whisper per Topik Rapat & Podcast</span>
            </div>
            <img src="visual%20uji/1_whisper_accuracy.png" alt="Whisper Accuracy Detailed">
        </div>
    </div>

    <!-- ══════════════════════════════════════════════
         TAB 3: PREPROCESSING FILTERS
    ══════════════════════════════════════════════ -->
    <div id="tab-filters" class="mp-tab-content">
        <!-- ── FILTER 1: NOISE REDUCTION ── -->
        <div class="model-section-header">
            <div class="model-badge" style="background:#ef5350;color:#fff;">
                <i class="fas fa-volume-xmark"></i>
            </div>
            <div>
                <h2 class="model-section-title">1. Noise Reduction Filter <span class="model-tag" style="background:#ffebee;color:#c62828;">Audio Clean</span></h2>
                <p class="model-section-desc">Pembersihan noise spektral gating sebelum transkripsi Whisper</p>
            </div>
        </div>

        <div class="mp-grid-3">
            <div class="mp-kpi-card">
                <div class="mp-kpi-icon" style="background:#ffebee;color:#c62828;"><i class="fas fa-chart-line"></i></div>
                <div class="mp-kpi-info">
                    <span class="mp-kpi-label">Akurasi Sebelum NR</span>
                    <span class="mp-kpi-value">61.67%</span>
                    <span class="mp-kpi-note warn">Akurasi Word WAcc</span>
                </div>
            </div>
            <div class="mp-kpi-card">
                <div class="mp-kpi-icon" style="background:#e8f5e9;color:#2e7d32;"><i class="fas fa-circle-check"></i></div>
                <div class="mp-kpi-info">
                    <span class="mp-kpi-label">Akurasi Sesudah NR</span>
                    <span class="mp-kpi-value">96.11%</span>
                    <span class="mp-kpi-note good">Mendekati Audio Bersih</span>
                </div>
            </div>
            <div class="mp-kpi-card">
                <div class="mp-kpi-icon" style="background:#e3f2fd;color:#1565c0;"><i class="fas fa-bolt"></i></div>
                <div class="mp-kpi-info">
                    <span class="mp-kpi-label">Peningkatan (Δ)</span>
                    <span class="mp-kpi-value" style="color:#2e7d32;">+34.44%</span>
                    <span class="mp-kpi-note good">Optimalisasi Akurasi</span>
                </div>
            </div>
        </div>

        <!-- Noise Reduction Images -->
        <div class="mp-grid-2">
            <div class="mp-image-card" style="margin-bottom:0;">
                <div class="mp-image-title">
                    <i class="fas fa-chart-column" style="color:#ef5350;"></i>
                    <span>Perbandingan Metrik Sebelum vs Sesudah Noise Reduction</span>
                </div>
                <img src="visual%20uji/2_noise_reduction.png" alt="Noise Reduction Bar">
            </div>
            <div class="mp-image-card" style="margin-bottom:0;">
                <div class="mp-image-title">
                    <i class="fas fa-circle-nodes" style="color:#1e88e5;"></i>
                    <span>Radar Chart Cakupan Perbaikan WAcc</span>
                </div>
                <img src="visual%20uji/2b_noise_radar.png" alt="Noise Reduction Radar">
            </div>
        </div>

        <div class="mp-divider"></div>

        <!-- ── FILTER 2: WORD FILLER REMOVAL ── -->
        <div class="model-section-header">
            <div class="model-badge" style="background:#4caf50;color:#fff;">
                <i class="fas fa-comment-slash"></i>
            </div>
            <div>
                <h2 class="model-section-title">2. Word Filler Removal <span class="model-tag" style="background:#e8f5e9;color:#2e7d32;">Text Cleaning</span></h2>
                <p class="model-section-desc">Pembersihan otomatis kata sisipan (em, eh, ya kan, dll.)</p>
            </div>
        </div>

        <div class="mp-grid-3">
            <div class="mp-kpi-card">
                <div class="mp-kpi-icon" style="background:#e3f2fd;color:#1565c0;"><i class="fas fa-bullseye"></i></div>
                <div class="mp-kpi-info">
                    <span class="mp-kpi-label">Precision</span>
                    <span class="mp-kpi-value">96.42%</span>
                    <span class="mp-kpi-note good">Akurasi kata yang dihapus</span>
                </div>
            </div>
            <div class="mp-kpi-card">
                <div class="mp-kpi-icon" style="background:#e8f5e9;color:#2e7d32;"><i class="fas fa-arrow-down-wide-short"></i></div>
                <div class="mp-kpi-info">
                    <span class="mp-kpi-label">Recall</span>
                    <span class="mp-kpi-value">98.77%</span>
                    <span class="mp-kpi-note good">Filler yang berhasil ditemukan</span>
                </div>
            </div>
            <div class="mp-kpi-card">
                <div class="mp-kpi-icon" style="background:#fff3e0;color:#ef6c00;"><i class="fas fa-star"></i></div>
                <div class="mp-kpi-info">
                    <span class="mp-kpi-label">F1-Score</span>
                    <span class="mp-kpi-value">97.58%</span>
                    <span class="mp-kpi-note good">Keseimbangan harmonis</span>
                </div>
            </div>
        </div>

        <!-- Word Filler Image -->
        <div class="mp-image-card">
            <div class="mp-image-title">
                <i class="fas fa-table" style="color:#4caf50;"></i>
                <span>Confusion Matrix & Metrik Word Filler Removal</span>
            </div>
            <img src="visual%20uji/3_word_filler_removal.png" alt="Word Filler Removal Charts">
        </div>

        <div class="mp-divider"></div>

        <!-- ── FILTER 3: HALLUCINATION FILTER ── -->
        <div class="model-section-header">
            <div class="model-badge" style="background:#ff9800;color:#fff;">
                <i class="fas fa-triangle-exclamation"></i>
            </div>
            <div>
                <h2 class="model-section-title">3. Hallucination Filter <span class="model-tag" style="background:#fff3e0;color:#e65100;">Anti-Hallu</span></h2>
                <p class="model-section-desc">Pencegahan Whisper menghasilkan teks halusinasi saat audio hening</p>
            </div>
        </div>

        <div class="mp-grid-3">
            <div class="mp-kpi-card">
                <div class="mp-kpi-icon" style="background:#e3f2fd;color:#1565c0;"><i class="fas fa-check"></i></div>
                <div class="mp-kpi-info">
                    <span class="mp-kpi-label">Average Precision</span>
                    <span class="mp-kpi-value">92.47%</span>
                    <span class="mp-kpi-note good">Sangat aman (tidak salah hapus)</span>
                </div>
            </div>
            <div class="mp-kpi-card">
                <div class="mp-kpi-icon" style="background:#ffebee;color:#c62828;"><i class="fas fa-eye-slash"></i></div>
                <div class="mp-kpi-info">
                    <span class="mp-kpi-label">Average Recall</span>
                    <span class="mp-kpi-value">50.49%</span>
                    <span class="mp-kpi-note warn">Sebagian halusinasi masih lolos</span>
                </div>
            </div>
            <div class="mp-kpi-card">
                <div class="mp-kpi-icon" style="background:#f3e5f5;color:#6a1b9a;"><i class="fas fa-chart-pie"></i></div>
                <div class="mp-kpi-info">
                    <span class="mp-kpi-label">Average Accuracy</span>
                    <span class="mp-kpi-value">91.59%</span>
                    <span class="mp-kpi-note good">Akurasi klasifikasi filter</span>
                </div>
            </div>
        </div>

        <!-- Hallucination Image -->
        <div class="mp-image-card">
            <div class="mp-image-title">
                <i class="fas fa-chart-bar" style="color:#ff9800;"></i>
                <span>Metrik & Distribusi Deteksi Hallucination Filter per Kondisi</span>
            </div>
            <img src="visual%20uji/4_hallucination_filter.png" alt="Hallucination Filter Charts">
        </div>
    </div>

    <!-- ══════════════════════════════════════════════
         TAB 4: NLP & SUMMARIZATION
    ══════════════════════════════════════════════ -->
    <div id="tab-nlp" class="mp-tab-content">
        <!-- LEXRANK -->
        <div class="model-section-header">
            <div class="model-badge lexrank-badge">
                <i class="fas fa-network-wired"></i>
            </div>
            <div>
                <h2 class="model-section-title">1. Hybrid Extractive LexRank <span class="model-tag" style="background:#d1fae5;color:#065f46;">Extractive</span></h2>
                <p class="model-section-desc">Pencarian kalimat terpenting berdasarkan graph-similarity</p>
            </div>
        </div>

        <div class="mp-grid-2">
            <div style="background:#f8faff; border:1.5px solid #bfdbfe; border-radius:14px; padding:18px;">
                <div style="font-weight:700; font-size:0.85rem; color:#0369a1; margin-bottom:12px;">LIVE PODCAST (AVERAGE)</div>
                <div style="display:flex; flex-direction:column; gap:8px;">
                    <div class="mp-kpi-card" style="margin:0; padding:10px 14px;">
                        <span style="font-size:0.8rem;font-weight:600;width:150px;">Cosine Similarity:</span>
                        <strong style="color:#0284c7;">69.15%</strong>
                    </div>
                    <div class="mp-kpi-card" style="margin:0; padding:10px 14px;">
                        <span style="font-size:0.8rem;font-weight:600;width:150px;">Sentence Coverage:</span>
                        <strong style="color:#059669;">99.00%</strong>
                    </div>
                    <div class="mp-kpi-card" style="margin:0; padding:10px 14px;">
                        <span style="font-size:0.8rem;font-weight:600;width:150px;">Jaccard Similarity:</span>
                        <strong style="color:#16a34a;">21.01%</strong>
                    </div>
                </div>
            </div>

            <div style="background:#f0fdfa; border:1.5px solid #99f6e4; border-radius:14px; padding:18px;">
                <div style="font-weight:700; font-size:0.85rem; color:#0f766e; margin-bottom:12px;">UPLOAD RAPAT (AVERAGE)</div>
                <div style="display:flex; flex-direction:column; gap:8px;">
                    <div class="mp-kpi-card" style="margin:0; padding:10px 14px;">
                        <span style="font-size:0.8rem;font-weight:600;width:150px;">Cosine Similarity:</span>
                        <strong style="color:#0d9488;">62.52%</strong>
                    </div>
                    <div class="mp-kpi-card" style="margin:0; padding:10px 14px;">
                        <span style="font-size:0.8rem;font-weight:600;width:150px;">Sentence Coverage:</span>
                        <strong style="color:#059669;">100.00%</strong>
                    </div>
                    <div class="mp-kpi-card" style="margin:0; padding:10px 14px;">
                        <span style="font-size:0.8rem;font-weight:600;width:150px;">Jaccard Similarity:</span>
                        <strong style="color:#0f766e;">10.99%</strong>
                    </div>
                </div>
            </div>
        </div>

        <!-- LexRank Image -->
        <div class="mp-image-card">
            <div class="mp-image-title">
                <i class="fas fa-diagram-project" style="color:#009688;"></i>
                <span>Metrik Detail, Hubungan Kompresi, dan Cosine Similarity LexRank</span>
            </div>
            <img src="visual%20uji/5_lexrank_summarization.png" alt="LexRank Charts">
        </div>

        <div class="mp-divider"></div>

        <!-- OLLAMA -->
        <div class="model-section-header">
            <div class="model-badge llm-badge">
                <i class="fas fa-brain"></i>
            </div>
            <div>
                <h2 class="model-section-title">2. Ollama Llama 3.2 (3B) <span class="model-tag" style="background:#ede9fe;color:#5b21b6;">Abstractive</span></h2>
                <p class="model-section-desc">Pembentukan notulensi naratif terstruktur menggunakan LLM lokal</p>
            </div>
        </div>

        <div class="mp-grid-2">
            <div style="background:#fcf8ff; border:1.5px solid #d8b4fe; border-radius:14px; padding:18px;">
                <div style="font-weight:700; font-size:0.85rem; color:#7c3aed; margin-bottom:12px;">BERTScore Live (Average)</div>
                <div style="display:flex; flex-direction:column; gap:8px;">
                    <div class="mp-kpi-card" style="margin:0; padding:10px 14px;">
                        <span style="font-size:0.8rem;font-weight:600;width:150px;">BERTScore Precision:</span>
                        <strong style="color:#7c3aed;">64.04%</strong>
                    </div>
                    <div class="mp-kpi-card" style="margin:0; padding:10px 14px;">
                        <span style="font-size:0.8rem;font-weight:600;width:150px;">BERTScore Recall:</span>
                        <strong style="color:#7c3aed;">65.80%</strong>
                    </div>
                    <div class="mp-kpi-card" style="margin:0; padding:10px 14px;">
                        <span style="font-size:0.8rem;font-weight:600;width:150px;">BERTScore F1:</span>
                        <strong style="color:#7c3aed;">64.90%</strong>
                    </div>
                </div>
            </div>

            <div style="background:#fcf8ff; border:1.5px solid #d8b4fe; border-radius:14px; padding:18px;">
                <div style="font-weight:700; font-size:0.85rem; color:#7c3aed; margin-bottom:12px;">BERTScore Upload (Average)</div>
                <div style="display:flex; flex-direction:column; gap:8px;">
                    <div class="mp-kpi-card" style="margin:0; padding:10px 14px;">
                        <span style="font-size:0.8rem;font-weight:600;width:150px;">BERTScore Precision:</span>
                        <strong style="color:#7c3aed;">65.00%</strong>
                    </div>
                    <div class="mp-kpi-card" style="margin:0; padding:10px 14px;">
                        <span style="font-size:0.8rem;font-weight:600;width:150px;">BERTScore Recall:</span>
                        <strong style="color:#7c3aed;">63.87%</strong>
                    </div>
                    <div class="mp-kpi-card" style="margin:0; padding:10px 14px;">
                        <span style="font-size:0.8rem;font-weight:600;width:150px;">BERTScore F1:</span>
                        <strong style="color:#7c3aed;">64.42%</strong>
                    </div>
                </div>
            </div>
        </div>

        <!-- BERTScore Image -->
        <div class="mp-image-card">
            <div class="mp-image-title">
                <i class="fas fa-brain" style="color:#7c3aed;"></i>
                <span>Evaluasi Semantik: BERTScore (Precision, Recall, F1) Ollama per Topik</span>
            </div>
            <img src="visual%20uji/6_bertscore_ollama.png" alt="BERTScore Ollama Charts">
        </div>
    </div>

</main>

<script src="assets/js/realtime-clock.js"></script>
<script>
// ── Switch Tabs Function ───────────────────────────────────
function switchTab(evt, tabId) {
    const contents = document.getElementsByClassName('mp-tab-content');
    for (let i = 0; i < contents.length; i++) {
        contents[i].classList.remove('active');
    }

    const buttons = document.getElementsByClassName('mp-tab-btn');
    for (let i = 0; i < buttons.length; i++) {
        buttons[i].classList.remove('active');
    }

    document.getElementById(tabId).classList.add('active');
    evt.currentTarget.classList.add('active');
}

// ── Chart.js Global Defaults ──────────────────────────────
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = '#617388';

// ── Chart 1: Whisper WER/WAcc/CER ─────────────────────────
new Chart(document.getElementById('whisperCompareChart'), {
    type: 'bar',
    data: {
        labels: ['WER (%)', 'WAcc (%)', 'CER (%)'],
        datasets: [
            {
                label: 'Live Transcription (Rata-rata 4 Podcast)',
                data: [55.32, 44.68, 43.10],
                backgroundColor: 'rgba(2,132,199,0.75)',
                borderRadius: 8,
                borderSkipped: false,
            },
            {
                label: 'Upload File (Rata-rata 9 Rapat)',
                data: [17.26, 82.74, 10.71],
                backgroundColor: 'rgba(217,119,6,0.75)',
                borderRadius: 8,
                borderSkipped: false,
            }
        ]
    },
    options: {
        responsive: true, maintainAspectRatio: false,
        plugins: {
            legend: { position: 'top', labels: { usePointStyle: true, boxWidth: 8 } },
            tooltip: {
                callbacks: {
                    label: ctx => ctx.dataset.label + ': ' + ctx.raw + '%'
                }
            }
        },
        scales: {
            y: { beginAtZero: true, max: 100, ticks: { callback: v => v + '%' }, grid: { color: '#f1f5f9' } },
            x: { grid: { display: false } }
        }
    }
});
</script>
</body>
</html>
