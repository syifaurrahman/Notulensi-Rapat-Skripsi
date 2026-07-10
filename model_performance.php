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
</head>
<body>

<?php include 'sidebar.php'; ?>

<main class="main-content">
    <!-- Top Bar -->
    <div class="top-bar">
        <div class="page-title">
            <h1>Performa Model</h1>
            <p>Akurasi & metrik evaluasi untuk setiap model yang digunakan</p>
        </div>
        <div class="header-date">
            <i class="fas fa-calendar-check"></i>
            <span id="realtime-clock"></span>
        </div>
    </div>

    <!-- ══════════════════════════════════════════════
         SECTION 1 — WHISPER (Transkripsi)
    ══════════════════════════════════════════════ -->
    <div class="model-section-header">
        <div class="model-badge whisper-badge">
            <i class="fas fa-microphone-lines"></i>
        </div>
        <div>
            <h2 class="model-section-title">Whisper <span class="model-tag">OpenAI</span></h2>
            <p class="model-section-desc">Model transkripsi speech-to-text berbasis Transformer</p>
        </div>
    </div>

    <!-- ── Whisper: Live vs Upload metric panels ── -->
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:24px;">

        <!-- PANEL LIVE -->
        <div style="background:#fff; border-radius:18px; border:1.5px solid #bae6fd; padding:22px 24px; box-shadow:0 2px 12px rgba(2,132,199,.07);">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:18px;">
                <div style="width:36px;height:36px;border-radius:10px;background:#e0f2fe;display:flex;align-items:center;justify-content:center;color:#0284c7;font-size:1rem;">
                    <i class="fas fa-broadcast-tower"></i>
                </div>
                <div>
                    <div style="font-weight:700;font-size:1rem;color:#0a1c32;">Live Transcription</div>
                    <div style="font-size:0.75rem;color:#64748b;">Perekaman suara langsung via mikrofon</div>
                </div>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px;">
                <div style="background:#f0f9ff;border-radius:12px;padding:14px 12px;border:1px solid #bae6fd;text-align:center;">
                    <div style="font-size:0.7rem;font-weight:600;color:#0369a1;text-transform:uppercase;letter-spacing:.04em;margin-bottom:6px;">WER</div>
                    <div id="live-wer" style="font-size:1.5rem;font-weight:700;color:#0a1c32;">—</div>
                    <div style="font-size:0.68rem;color:#64748b;margin-top:3px;">↓ Semakin kecil semakin baik</div>
                </div>
                <div style="background:#f0fdf4;border-radius:12px;padding:14px 12px;border:1px solid #86efac;text-align:center;">
                    <div style="font-size:0.7rem;font-weight:600;color:#15803d;text-transform:uppercase;letter-spacing:.04em;margin-bottom:6px;">WAcc</div>
                    <div id="live-wacc" style="font-size:1.5rem;font-weight:700;color:#0a1c32;">—</div>
                    <div style="font-size:0.68rem;color:#64748b;margin-top:3px;">↑ Semakin besar semakin baik</div>
                </div>
                <div style="background:#faf5ff;border-radius:12px;padding:14px 12px;border:1px solid #d8b4fe;text-align:center;">
                    <div style="font-size:0.7rem;font-weight:600;color:#7c3aed;text-transform:uppercase;letter-spacing:.04em;margin-bottom:6px;">CER</div>
                    <div id="live-cer" style="font-size:1.5rem;font-weight:700;color:#0a1c32;">—</div>
                    <div style="font-size:0.68rem;color:#64748b;margin-top:3px;">↓ Semakin kecil semakin baik</div>
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
                    <div style="font-weight:700;font-size:1rem;color:#0a1c32;">Upload File</div>
                    <div style="font-size:0.75rem;color:#64748b;">Unggah rekaman rapat (MP3/MP4)</div>
                </div>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px;">
                <div style="background:#fffbeb;border-radius:12px;padding:14px 12px;border:1px solid #fde68a;text-align:center;">
                    <div style="font-size:0.7rem;font-weight:600;color:#b45309;text-transform:uppercase;letter-spacing:.04em;margin-bottom:6px;">WER</div>
                    <div id="upload-wer" style="font-size:1.5rem;font-weight:700;color:#0a1c32;">—</div>
                    <div style="font-size:0.68rem;color:#64748b;margin-top:3px;">↓ Semakin kecil semakin baik</div>
                </div>
                <div style="background:#f0fdf4;border-radius:12px;padding:14px 12px;border:1px solid #86efac;text-align:center;">
                    <div style="font-size:0.7rem;font-weight:600;color:#15803d;text-transform:uppercase;letter-spacing:.04em;margin-bottom:6px;">WAcc</div>
                    <div id="upload-wacc" style="font-size:1.5rem;font-weight:700;color:#0a1c32;">—</div>
                    <div style="font-size:0.68rem;color:#64748b;margin-top:3px;">↑ Semakin besar semakin baik</div>
                </div>
                <div style="background:#faf5ff;border-radius:12px;padding:14px 12px;border:1px solid #d8b4fe;text-align:center;">
                    <div style="font-size:0.7rem;font-weight:600;color:#7c3aed;text-transform:uppercase;letter-spacing:.04em;margin-bottom:6px;">CER</div>
                    <div id="upload-cer" style="font-size:1.5rem;font-weight:700;color:#0a1c32;">—</div>
                    <div style="font-size:0.68rem;color:#64748b;margin-top:3px;">↓ Semakin kecil semakin baik</div>
                </div>
            </div>
        </div>

    </div>

    <!-- Chart perbandingan WER, WAcc, CER: Live vs Upload -->
    <div class="mp-chart-row" style="grid-template-columns:1fr;">
        <div class="mp-chart-card">
            <div class="mp-chart-header">
                <i class="fas fa-chart-bar" style="color:#0284c7;"></i>
                <span>Perbandingan Metrik Whisper: Live vs Upload</span>
            </div>
            <div class="mp-chart-wrap" style="height:200px;">
                <canvas id="whisperCompareChart"></canvas>
            </div>
        </div>
    </div>

    <!-- Whisper Small Info Card -->
    <div class="mp-table-card">
        <div class="mp-table-header">
            <i class="fas fa-info-circle" style="color:#0284c7;"></i>
            <span>Model yang Digunakan</span>
        </div>
        <div style="padding: 4px 0;">
            <div style="background:#f0f9ff; border-radius:14px; padding:18px 22px; border:1px solid #bae6fd; display:flex; align-items:center; gap:16px;">
                <div style="width:48px;height:48px;border-radius:12px;background:#0284c7;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                    <i class="fas fa-microphone-lines" style="color:#fff;font-size:1.25rem;"></i>
                </div>
                <div>
                    <div style="font-size:1.3rem;font-weight:700;color:#0a1c32;">Whisper Small</div>
                    <div style="font-size:0.8rem;color:#0369a1;margin-top:2px;">OpenAI · Speech-to-Text · Bahasa Indonesia dan English</div>
                </div>
            </div>
        </div>
    </div>

    <div class="mp-divider"></div>

    <!-- ══════════════════════════════════════════════
         SECTION 2 — LEXRANK (Ringkasan Ekstraktif)
    ══════════════════════════════════════════════ -->
    <div class="model-section-header">
        <div class="model-badge lexrank-badge">
            <i class="fas fa-network-wired"></i>
        </div>
        <div>
            <h2 class="model-section-title">LexRank <span class="model-tag" style="background:#d1fae5;color:#065f46;">Extractive</span></h2>
            <p class="model-section-desc">Algoritma graph-based untuk ringkasan ekstraktif otomatis</p>
        </div>
    </div>

    <!-- LexRank ROUGE — 2 Kolom Live vs Upload -->
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:24px;">

        <!-- Kolom Live — Uji Korelasi -->
        <div style="background:#f8faff; border:1.5px solid #bfdbfe; border-radius:14px; padding:18px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:14px;">
                <span style="width:10px;height:10px;border-radius:50%;background:#0284c7;
                             display:inline-block;box-shadow:0 0 5px #93c5fd;"></span>
                <span style="font-weight:700; font-size:0.82rem; color:#0369a1; letter-spacing:.04em;">LIVE TRANSCRIPTION — UJI KORELASI</span>
            </div>
            <div style="font-size:0.75rem;color:#0369a1;margin-bottom:12px;">
                <i class="fas fa-info-circle"></i>
                LexRank bersifat <strong>ekstraktif</strong> — kalimat dipilih langsung dari transkripsi Whisper.
            </div>
            <div style="display:flex; flex-direction:column; gap:10px;">
                <div class="mp-kpi-card" style="margin:0;">
                    <div class="mp-kpi-icon" style="background:#e0f2fe;color:#0284c7;"><i class="fas fa-wave-square"></i></div>
                    <div class="mp-kpi-info">
                        <span class="mp-kpi-label">Cosine Similarity</span>
                        <span class="mp-kpi-value" style="color:#0284c7;">69.15%</span>
                        <span class="mp-kpi-note good">Relevansi topik (↑ Semakin besar semakin baik)</span>
                    </div>
                </div>
                <div class="mp-kpi-card" style="margin:0;">
                    <div class="mp-kpi-icon" style="background:#d1fae5;color:#059669;"><i class="fas fa-check-double"></i></div>
                    <div class="mp-kpi-info">
                        <span class="mp-kpi-label">Sentence Coverage</span>
                        <span class="mp-kpi-value" style="color:#059669;">99.00%</span>
                        <span class="mp-kpi-note good">Kutipan langsung dari kalimat transkrip</span>
                    </div>
                </div>
                <div class="mp-kpi-card" style="margin:0;">
                    <div class="mp-kpi-icon" style="background:#f0fdf4;color:#16a34a;"><i class="fas fa-percentage"></i></div>
                    <div class="mp-kpi-info">
                        <span class="mp-kpi-label">Jaccard Similarity</span>
                        <span class="mp-kpi-value" style="color:#16a34a;">21.01%</span>
                        <span class="mp-kpi-note neutral">Kecocokan kosakata unik (↑ Semakin besar semakin baik)</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Kolom Upload — Uji Korelasi -->
        <div style="background:#f0fdfa; border:1.5px solid #99f6e4; border-radius:14px; padding:18px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:14px;">
                <span style="width:10px;height:10px;border-radius:50%;background:#0d9488;
                             display:inline-block;box-shadow:0 0 5px #5eead4;"></span>
                <span style="font-weight:700; font-size:0.82rem; color:#0f766e; letter-spacing:.04em;">UPLOAD FILE — UJI KORELASI</span>
            </div>
            <div style="font-size:0.75rem;color:#0f766e;margin-bottom:12px;">
                <i class="fas fa-info-circle"></i>
                LexRank bersifat <strong>ekstraktif</strong> — kalimat dipilih langsung dari transkripsi Whisper.
            </div>
            <div style="display:flex; flex-direction:column; gap:10px;">
                <div class="mp-kpi-card" style="margin:0;">
                    <div class="mp-kpi-icon" style="background:#ccfbf1;color:#0f766e;"><i class="fas fa-wave-square"></i></div>
                    <div class="mp-kpi-info">
                        <span class="mp-kpi-label">Cosine Similarity</span>
                        <span class="mp-kpi-value" style="color:#0d9488;">62.52%</span>
                        <span class="mp-kpi-note good">Relevansi topik (↑ Semakin besar semakin baik)</span>
                    </div>
                </div>
                <div class="mp-kpi-card" style="margin:0;">
                    <div class="mp-kpi-icon" style="background:#d1fae5;color:#059669;"><i class="fas fa-check-double"></i></div>
                    <div class="mp-kpi-info">
                        <span class="mp-kpi-label">Sentence Coverage</span>
                        <span class="mp-kpi-value" style="color:#059669;">100.00%</span>
                        <span class="mp-kpi-note good">Semua kalimat berasal dari transkripsi asli</span>
                    </div>
                </div>
                <div class="mp-kpi-card" style="margin:0;">
                    <div class="mp-kpi-icon" style="background:#ccfbf1;color:#0f766e;"><i class="fas fa-percentage"></i></div>
                    <div class="mp-kpi-info">
                        <span class="mp-kpi-label">Jaccard Similarity</span>
                        <span class="mp-kpi-value" style="color:#0f766e;">10.99%</span>
                        <span class="mp-kpi-note neutral">Kecocokan kosakata unik (↑ Semakin besar semakin baik)</span>
                    </div>
                </div>
            </div>
        </div>
    </div>


    <!-- LexRank Charts -->

    <div class="mp-chart-row">
        <div class="mp-chart-card">
            <div class="mp-chart-header">
                <i class="fas fa-chart-radar" style="color:#059669;"></i>
                <span>Perbandingan ROUGE-L — Live vs Upload</span>
            </div>
            <div class="mp-chart-wrap">
                <canvas id="lexrankRougeChart"></canvas>
            </div>
        </div>
        <div class="mp-chart-card">
            <div class="mp-chart-header">
                <i class="fas fa-chart-area" style="color:#059669;"></i>
                <span>Distribusi Skor Kalimat (Sentence Score)</span>
            </div>
            <div class="mp-chart-wrap">
                <canvas id="lexrankScoreChart"></canvas>
            </div>
        </div>
    </div>

    <div class="mp-divider"></div>

    <!-- ══════════════════════════════════════════════
         SECTION 3 — LLM / OLLAMA (Ringkasan Abstraktif)
    ══════════════════════════════════════════════ -->
    <div class="model-section-header">
        <div class="model-badge llm-badge">
            <i class="fas fa-brain"></i>
        </div>
        <div>
            <h2 class="model-section-title">LLM / Ollama <span class="model-tag" style="background:#ede9fe;color:#5b21b6;">Abstractive</span></h2>
            <p class="model-section-desc">Model bahasa besar untuk ringkasan abstraktif & pemahaman konteks</p>
        </div>
    </div>

    <!-- LLM ROUGE — 2 Kolom Live vs Upload -->
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:24px;">

        <!-- Kolom Live -->
        <div style="background:#faf5ff; border:1.5px solid #ddd6fe; border-radius:14px; padding:18px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:14px;">
                <span style="width:10px;height:10px;border-radius:50%;background:#7c3aed;
                             display:inline-block;box-shadow:0 0 5px #c4b5fd;"></span>
                <span style="font-weight:700; font-size:0.82rem; color:#5b21b6; letter-spacing:.04em;">LIVE TRANSCRIPTION</span>
            </div>
            <div style="display:flex; flex-direction:column; gap:10px;">
                <div class="mp-kpi-card" style="margin:0;">
                    <div class="mp-kpi-icon" style="background:#ede9fe;color:#7c3aed;"><i class="fas fa-star"></i></div>
                    <div class="mp-kpi-info">
                        <span class="mp-kpi-label">ROUGE-L (F1-Score)</span>
                        <span class="mp-kpi-value" id="llm-live-f1">—</span>
                        <span class="mp-kpi-note good">Skor keseimbangan (↑ Semakin besar semakin baik)</span>
                    </div>
                </div>
                <div class="mp-kpi-card" style="margin:0;">
                    <div class="mp-kpi-icon" style="background:#f5f3ff;color:#6d28d9;"><i class="fas fa-bullseye"></i></div>
                    <div class="mp-kpi-info">
                        <span class="mp-kpi-label">ROUGE-L (Precision)</span>
                        <span class="mp-kpi-value" id="llm-live-p">—</span>
                        <span class="mp-kpi-note good">Ketepatan ringkasan (↑ Semakin besar semakin baik)</span>
                    </div>
                </div>
                <div class="mp-kpi-card" style="margin:0;">
                    <div class="mp-kpi-icon" style="background:#faf5ff;color:#9333ea;"><i class="fas fa-magnet"></i></div>
                    <div class="mp-kpi-info">
                        <span class="mp-kpi-label">ROUGE-L (Recall)</span>
                        <span class="mp-kpi-value" id="llm-live-r">—</span>
                        <span class="mp-kpi-note good">Cakupan informasi (↑ Semakin besar semakin baik)</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Kolom Upload -->
        <div style="background:#fdf4ff; border:1.5px solid #e9d5ff; border-radius:14px; padding:18px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:14px;">
                <span style="width:10px;height:10px;border-radius:50%;background:#a855f7;
                             display:inline-block;box-shadow:0 0 5px #d8b4fe;"></span>
                <span style="font-weight:700; font-size:0.82rem; color:#6b21a8; letter-spacing:.04em;">UPLOAD FILE</span>
            </div>
            <div style="display:flex; flex-direction:column; gap:10px;">
                <div class="mp-kpi-card" style="margin:0;">
                    <div class="mp-kpi-icon" style="background:#ede9fe;color:#7c3aed;"><i class="fas fa-star"></i></div>
                    <div class="mp-kpi-info">
                        <span class="mp-kpi-label">ROUGE-L (F1-Score)</span>
                        <span class="mp-kpi-value" id="llm-upload-f1">—</span>
                        <span class="mp-kpi-note good">Skor keseimbangan (↑ Semakin besar semakin baik)</span>
                    </div>
                </div>
                <div class="mp-kpi-card" style="margin:0;">
                    <div class="mp-kpi-icon" style="background:#f5f3ff;color:#6d28d9;"><i class="fas fa-bullseye"></i></div>
                    <div class="mp-kpi-info">
                        <span class="mp-kpi-label">ROUGE-L (Precision)</span>
                        <span class="mp-kpi-value" id="llm-upload-p">—</span>
                        <span class="mp-kpi-note good">Ketepatan ringkasan (↑ Semakin besar semakin baik)</span>
                    </div>
                </div>
                <div class="mp-kpi-card" style="margin:0;">
                    <div class="mp-kpi-icon" style="background:#faf5ff;color:#9333ea;"><i class="fas fa-magnet"></i></div>
                    <div class="mp-kpi-info">
                        <span class="mp-kpi-label">ROUGE-L (Recall)</span>
                        <span class="mp-kpi-value" id="llm-upload-r">—</span>
                        <span class="mp-kpi-note good">Cakupan informasi (↑ Semakin besar semakin baik)</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Info tambahan LLM -->
    <div class="mp-kpi-row" style="margin-bottom:0; grid-template-columns: 1fr;">
        <div class="mp-kpi-card" style="max-width: 500px; margin: 0 auto; width: 100%;">
            <div class="mp-kpi-icon" style="background:#faf5ff;color:#9333ea;"><i class="fas fa-server"></i></div>
            <div class="mp-kpi-info">
                <span class="mp-kpi-label">Model LLM</span>
                <span class="mp-kpi-value">Llama 3.2 <span style="font-size:1rem;font-weight:normal;">(3B)</span></span>
                <span class="mp-kpi-note neutral"><i class="fas fa-code-branch"></i> via Ollama local server</span>
            </div>
        </div>
    </div>

    <!-- LLM Charts -->
    <div class="mp-chart-row" style="grid-template-columns: 1fr;">
        <div class="mp-chart-card">
            <div class="mp-chart-header">
                <i class="fas fa-chart-bar" style="color:#7c3aed;"></i>
                <span>Perbandingan ROUGE-L: LexRank vs LLM</span>
            </div>
            <div class="mp-chart-wrap" style="height: 250px;">
                <canvas id="llmCompareChart"></canvas>
            </div>
        </div>
    </div>

    <!-- Overall Comparison Table -->
    <div class="mp-divider"></div>
    <div class="model-section-header">
        <div class="model-badge" style="background:linear-gradient(135deg,#2463eb,#7c3aed);">
            <i class="fas fa-trophy" style="color:#fff;"></i>
        </div>
        <div>
            <h2 class="model-section-title">Ringkasan Perbandingan Model</h2>
            <p class="model-section-desc">Evaluasi gabungan ketiga model dalam pipeline Notulensia</p>
        </div>
    </div>
    <div class="mp-table-card">
        <div class="mp-table-wrap">
            <table class="mp-table">
                <thead>
                    <tr>
                        <th>Model</th>
                        <th>Tugas</th>
                        <th>Metrik Utama</th>
                        <th>Skor</th>
                        <th>Rekomendasi</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><i class="fas fa-microphone-lines" style="color:#0284c7;margin-right:6px;"></i><strong>Whisper Small</strong></td>
                        <td>Transkripsi Audio</td>
                        <td>WAcc (Live) / WAcc (Upload)</td>
                        <td>
                            <span class="mp-badge warn" title="Rata-rata 4 live podcast">44.68% Live</span>
                            <span class="mp-badge good" title="Pengujian upload aktual">75.50% Upload</span>
                        </td>
                        <td><span class="mp-badge best">✓ Aktif</span></td>
                    </tr>
                    <tr>
                        <td><i class="fas fa-network-wired" style="color:#059669;margin-right:6px;"></i><strong>LexRank</strong></td>
                        <td>Ringkasan Ekstraktif</td>
                        <td>ROUGE-L F1 (Live) / ROUGE-L F1 (Upload)</td>
                        <td>
                            <span class="mp-badge good" title="Rata-rata 4 live podcast">27.85% Live</span>
                            <span class="mp-badge warn" title="Pengujian upload aktual">10.80% Upload</span>
                        </td>
                        <td><span class="mp-badge best">&#10003; Aktif</span></td>
                    </tr>
                    <tr>
                        <td><i class="fas fa-arrows-left-right" style="color:#0d9488;margin-right:6px;"></i><strong>LexRank Korelasi</strong></td>
                        <td>Korelasi vs Transkripsi</td>
                        <td>Cosine Similarity (Live) / Cosine Similarity (Upload)</td>
                        <td>
                            <span class="mp-badge good" title="Rata-rata 4 live podcast">69.15% Live</span>
                            <span class="mp-badge good" title="Pengujian upload aktual">62.52% Upload</span>
                        </td>
                        <td><span class="mp-badge best">&#10003; Aktif</span></td>
                    </tr>
                    <tr>
                        <td><i class="fas fa-brain" style="color:#7c3aed;margin-right:6px;"></i><strong>LLM / Ollama</strong></td>
                        <td>Ringkasan Abstraktif</td>
                        <td>ROUGE-L F1 (Live) / ROUGE-L F1 (Upload)</td>
                        <td>
                            <span class="mp-badge good" title="Rata-rata 4 live podcast">27.85% Live</span>
                            <span class="mp-badge warn" title="Pengujian upload aktual">16.20% Upload</span>
                        </td>
                        <td><span class="mp-badge best">✓ Aktif</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

</main>

<script src="assets/js/realtime-clock.js"></script>
<script>
// ── Chart.js Global Defaults ──────────────────────────────
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = '#617388';

// ── 1. WHISPER: Perbandingan WER, WAcc, CER — Live vs Upload ──
// !! Ganti nilai di bawah dengan hasil pengujian aktual Anda !!
const whisperMetrics = {
    live:   { wer: 55.32, wacc: 44.68, cer: 43.11 },  // rata-rata 4 live podcast (01 Juli 2026)
    upload: { wer: 24.50, wacc: 75.50, cer: 17.57 },  // hasil pengujian aktual (21 Juni 2026)
};

// Fungsi isi nilai pada card Live & Upload
function fillWhisperMetrics() {
    const fmt = (v, suffix) => (v !== null && v !== undefined) ? v + suffix : '—';
    document.getElementById('live-wer').textContent   = fmt(whisperMetrics.live.wer,   '%');
    document.getElementById('live-wacc').textContent  = fmt(whisperMetrics.live.wacc,  '%');
    document.getElementById('live-cer').textContent   = fmt(whisperMetrics.live.cer,   '%');
    document.getElementById('upload-wer').textContent  = fmt(whisperMetrics.upload.wer,  '%');
    document.getElementById('upload-wacc').textContent = fmt(whisperMetrics.upload.wacc, '%');
    document.getElementById('upload-cer').textContent  = fmt(whisperMetrics.upload.cer,  '%');
}
fillWhisperMetrics();

// ── 2. LEXRANK: ROUGE-L — Live ──
// Sumber: akurasi/ollama/live_ratarata.txt (rata-rata 4 live podcast, 01 Juli 2026)
const lexrankMetrics = {
    live:   { f1: 27.85, precision: 33.80, recall: 26.30 }, // rata-rata ROUGE-L Ollama vs LexRank
};

function fillLexRankMetrics() {
    const fmt = (v, suffix) => (v !== null && v !== undefined) ? v + suffix : '—';
    const elF1 = document.getElementById('lr-live-f1');
    const elP = document.getElementById('lr-live-p');
    const elR = document.getElementById('lr-live-r');
    if (elF1) elF1.textContent = fmt(lexrankMetrics.live.f1, '%');
    if (elP) elP.textContent = fmt(lexrankMetrics.live.precision, '%');
    if (elR) elR.textContent = fmt(lexrankMetrics.live.recall, '%');
}
fillLexRankMetrics();

// ── 3. LLM / OLLAMA: Perbandingan ROUGE-L — Live vs Upload ──
// Live: akurasi/ollama/live_ratarata.txt (rata-rata 4 live podcast, 01 Juli 2026)
const llmMetrics = {
    live:   { f1: 27.85, precision: 33.80, recall: 26.30 }, // rata-rata 4 live podcast
    upload: { f1: 16.20, precision: 24.10, recall: 12.46 }, // hasil pengujian aktual (21 Juni 2026)
};

function fillLlmMetrics() {
    const fmt = (v, suffix) => (v !== null && v !== undefined) ? v + suffix : '—';
    document.getElementById('llm-live-f1').textContent   = fmt(llmMetrics.live.f1,   '%');
    document.getElementById('llm-live-p').textContent    = fmt(llmMetrics.live.precision, '%');
    document.getElementById('llm-live-r').textContent    = fmt(llmMetrics.live.recall,    '%');
    document.getElementById('llm-upload-f1').textContent = fmt(llmMetrics.upload.f1, '%');
    document.getElementById('llm-upload-p').textContent  = fmt(llmMetrics.upload.precision, '%');
    document.getElementById('llm-upload-r').textContent  = fmt(llmMetrics.upload.recall,    '%');
}
fillLlmMetrics();


// Chart: Grouped Bar — Live vs Upload (WER, WAcc, CER)
new Chart(document.getElementById('whisperCompareChart'), {
    type: 'bar',
    data: {
        labels: ['WER (%)', 'WAcc (%)', 'CER (%)'],
        datasets: [
            {
                label: 'Live Transcription',
                data: [
                    whisperMetrics.live.wer,
                    whisperMetrics.live.wacc,
                    whisperMetrics.live.cer
                ],
                backgroundColor: 'rgba(2,132,199,0.75)',
                borderRadius: 8,
                borderSkipped: false,
            },
            {
                label: 'Upload File',
                data: [
                    whisperMetrics.upload.wer,
                    whisperMetrics.upload.wacc,
                    whisperMetrics.upload.cer
                ],
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
                    label: ctx => {
                        const val = ctx.raw;
                        return ctx.dataset.label + ': ' + (val !== null ? val + '%' : 'Belum diisi');
                    }
                }
            }
        },
        scales: {
            y: { beginAtZero: true, max: 100, ticks: { callback: v => v + '%' }, grid: { color: '#f1f5f9' } },
            x: { grid: { display: false } }
        }
    }
});

// ── 3. LEXRANK: ROUGE-L Components — Live vs Upload ──────────────────────────
// Live: akurasi/ollama/live_ratarata.txt (rata-rata 4 live podcast)
// Upload: data aktual sebelumnya
new Chart(document.getElementById('lexrankRougeChart'), {
    type: 'bar',
    data: {
        labels: ['Precision', 'Recall', 'F1-Score'],
        datasets: [
            {
                label: 'Live Transcription',
                data: [33.80, 26.30, 27.85],
                backgroundColor: 'rgba(2,132,199,0.75)',
                borderRadius: 8,
                borderSkipped: false,
            },
            {
                label: 'Upload File',
                data: [8.25, 15.62, 10.80],
                backgroundColor: 'rgba(5,150,105,0.75)',
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

// ── 4. LEXRANK: Sentence Score Distribution ───────────────
new Chart(document.getElementById('lexrankScoreChart'), {
    type: 'line',
    data: {
        labels: ['K1','K2','K3','K4','K5','K6','K7','K8','K9','K10'],
        datasets: [{
            label: 'Sentence Score',
            data: [0.82, 0.91, 0.65, 0.78, 0.95, 0.43, 0.88, 0.72, 0.60, 0.85],
            borderColor: '#10b981',
            backgroundColor: 'rgba(16,185,129,0.08)',
            tension: 0.4,
            fill: true,
            pointRadius: 5,
            pointBackgroundColor: '#059669',
        }]
    },
    options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
            y: { beginAtZero: true, max: 1.0, grid: { color: '#f1f5f9' } },
            x: { grid: { display: false } }
        }
    }
});

// ── 5. LLM vs LexRank ROUGE-L Comparison — Live vs Upload ──────────────────
// Live: akurasi/ollama/live_ratarata.txt (rata-rata 4 live podcast, 01 Juli 2026)
new Chart(document.getElementById('llmCompareChart'), {
    type: 'bar',
    data: {
        labels: ['ROUGE-L F1', 'ROUGE-L Precision', 'ROUGE-L Recall'],
        datasets: [
            {
                label: 'Live Transcription',
                data: [27.85, 33.80, 26.30],
                backgroundColor: 'rgba(124,58,237,0.75)',
                borderRadius: 8,
                borderSkipped: false,
            },
            {
                label: 'Upload File',
                data: [16.20, 24.10, 12.46],
                backgroundColor: 'rgba(168,85,247,0.45)',
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

// Kode Response Time dihapus sesuai permintaan
</script>
</body>
</html>
