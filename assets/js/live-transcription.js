/**
 * live-transcription.js
 * =====================
 * Menghubungkan halaman notulensi.php ke Whisper Web Server (Flask+SocketIO)
 * via WebSocket untuk transkripsi suara realtime.
 *
 * Fitur:
 *  - Deteksi & pilih microphone dari browser
 *  - Capture audio via AudioContext + ScriptProcessorNode
 *  - Stream audio chunks ke server via Socket.IO
 *  - Terima & tampilkan transkripsi realtime
 *  - Timer durasi recording
 *  - Simpan hasil ke file (server-side)
 */

// ══════════════════════════════════════════════════
// Config
// ══════════════════════════════════════════════════

const WHISPER_SERVER = 'http://localhost:5000';
const AUDIO_SAMPLE_RATE = 16000;  // Whisper butuh 16kHz
const BUFFER_SIZE = 4096;         // ScriptProcessor buffer size
const SEND_INTERVAL_MS = 2000;    // Kirim audio tiap 2 detik

// ══════════════════════════════════════════════════
// State
// ══════════════════════════════════════════════════

let socket = null;
let audioContext = null;
let mediaStream = null;
let scriptProcessor = null;
let sourceNode = null;
let isListening = false;
let audioChunks = [];
let sendTimer = null;
let durationTimer = null;
let durationSeconds = 0;

// Flag: true jika user menekan "Simpan Notulen" saat masih listening
let pendingSave = false;
// Menyimpan teks final dari server (setelah is_final: true)
let lastFinalText = '';

// ── FIX: Simpan pending summarize text jika socket reconnect diperlukan ──
let _pendingSummarizePayload = null;

// ── Hot-plug: flag agar refresh devicelist tidak ganggu sesi ──
let _isSwitchingMic = false;

// DOM elements (di-init saat DOM ready)
let micSelect, statusValue, statusIcon, startBtn, stopBtn;
let transcriptContent, durationDisplay, liveBadge;
let meetingNameInput;

// ══════════════════════════════════════════════════
// Init
// ══════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    // Cache DOM elements
    micSelect = document.getElementById('micSelect');
    statusValue = document.getElementById('statusValue');
    statusIcon = document.getElementById('statusIcon');
    startBtn = document.getElementById('startBtn');
    stopBtn = document.getElementById('stopBtn');
    transcriptContent = document.getElementById('transcriptContent');
    durationDisplay = document.getElementById('durationDisplay');
    liveBadge = document.getElementById('liveBadge');
    meetingNameInput = document.querySelector('.input-field[type="text"]');

    // Init microphone list
    initMicrophoneList();

    // Attach button handlers
    if (startBtn) startBtn.addEventListener('click', startListening);
    if (stopBtn) stopBtn.addEventListener('click', stopListening);

    // ── Hot-plug: dengarkan perubahan perangkat audio ──────────────────
    if (navigator.mediaDevices && navigator.mediaDevices.addEventListener) {
        navigator.mediaDevices.addEventListener('devicechange', _onDeviceChange);
    }

    // ── Switch mic saat user ganti select saat sedang listening ───────
    if (micSelect) {
        micSelect.addEventListener('change', () => {
            if (isListening) {
                switchMicrophone(micSelect.value);
            }
        });
    }

    // Set initial UI state
    updateUI('idle');
});


// ══════════════════════════════════════════════════
// Microphone Detection
// ══════════════════════════════════════════════════

async function initMicrophoneList() {
    if (!micSelect) return;

    // Minta permission dulu agar label device muncul
    try {
        const tempStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        tempStream.getTracks().forEach(t => t.stop());
    } catch (e) {
        console.warn('Mic permission denied:', e);
        micSelect.innerHTML = '<option value="">⚠ Izinkan akses mikrofon</option>';
        return;
    }

    await _refreshDeviceList();
}


/**
 * Refresh daftar device audio input ke dalam <select>.
 * Dipanggil saat halaman load dan saat devicechange event.
 * Tidak akan mengubah mic yang sedang aktif jika isListening === true.
 */
async function _refreshDeviceList() {
    if (!micSelect) return;

    try {
        const devices      = await navigator.mediaDevices.enumerateDevices();
        const audioInputs  = devices.filter(d => d.kind === 'audioinput');

        // Simpan pilihan saat ini agar tidak berubah saat refresh
        const currentValue = micSelect.value;

        micSelect.innerHTML = '';

        if (audioInputs.length === 0) {
            micSelect.innerHTML = '<option value="">Tidak ada mikrofon terdeteksi</option>';
            return;
        }

        audioInputs.forEach((device, idx) => {
            const option       = document.createElement('option');
            option.value       = device.deviceId;
            option.textContent = device.label || `Microphone ${idx + 1}`;
            micSelect.appendChild(option);
        });

        // Kembalikan ke pilihan sebelumnya jika masih tersedia
        if (currentValue && micSelect.querySelector(`option[value="${currentValue}"]`)) {
            micSelect.value = currentValue;
        }

    } catch (e) {
        console.error('Error enumerating devices:', e);
    }
}


/**
 * Handler saat perangkat audio terhubung / dicabut (Hot-plug).
 * Hanya memperbarui dropdown. Tidak memengaruhi sesi yang berjalan.
 */
async function _onDeviceChange() {
    console.log('[Mic] devicechange event — memperbarui daftar mikrofon...');

    await _refreshDeviceList();

    // Highlight select mic agar user tahu ada perubahan
    if (micSelect) {
        micSelect.classList.remove('mic-new-device');
        void micSelect.offsetWidth; // force reflow agar animasi restart
        micSelect.classList.add('mic-new-device');
        setTimeout(() => micSelect.classList.remove('mic-new-device'), 2500);
    }

    // Notifikasi kecil di UI jika sedang live
    if (isListening) {
        _showMicHotplugToast();
    }
}


/**
 * Tampilkan badge notifikasi kecil di area mic selector.
 */
function _showMicHotplugToast() {
    // Hapus toast lama jika ada
    const old = document.getElementById('mic-hotplug-toast');
    if (old) old.remove();

    const toast = document.createElement('div');
    toast.id = 'mic-hotplug-toast';
    toast.innerHTML = '<i class="fas fa-plug" style="margin-right:5px;"></i>Perangkat audio baru terdeteksi!';
    toast.style.cssText = [
        'position:fixed', 'bottom:24px', 'right:24px',
        'background:#2463eb', 'color:#fff',
        'padding:10px 18px', 'border-radius:10px',
        'font-size:0.82rem', 'font-weight:600',
        'box-shadow:0 4px 16px rgba(0,0,0,0.18)',
        'z-index:9999', 'animation:fadeInUp 0.3s ease',
        'display:flex', 'align-items:center',
    ].join(';');

    document.body.appendChild(toast);

    // Auto-hapus setelah 4 detik
    setTimeout(() => toast.remove(), 4000);
}


/**
 * Switch mikrofon yang aktif SAAT LIVE berjalan.
 * Hanya mengganti audio stream dan audio nodes.
 * Socket, send timer, dan transkripsi TIDAK terganggu.
 *
 * @param {string} newDeviceId - deviceId mic baru dari micSelect.value
 */
async function switchMicrophone(newDeviceId) {
    if (!isListening || _isSwitchingMic) return;

    _isSwitchingMic = true;
    console.log('[Mic] Switching mic ke:', newDeviceId);

    // Tampilkan indikator switch
    const statusInfo = document.querySelector('.save-info');
    if (statusInfo) statusInfo.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Beralih mikrofon...';

    try {
        // 1. Kirim sisa audio dari buffer lama sebelum putus
        sendAudioChunks();

        // 2. Putus source lama (bukan audioContext, bukan scriptProcessor)
        if (sourceNode) {
            sourceNode.disconnect();
            sourceNode = null;
        }
        if (mediaStream) {
            mediaStream.getTracks().forEach(t => t.stop());
            mediaStream = null;
        }

        // 3. Buka stream baru dari mic yang dipilih
        const constraints = {
            audio: {
                deviceId    : newDeviceId ? { exact: newDeviceId } : undefined,
                sampleRate  : { ideal: AUDIO_SAMPLE_RATE },
                channelCount: 1,
                echoCancellation : true,
                noiseSuppression : true,
                autoGainControl  : true,
            }
        };

        mediaStream = await navigator.mediaDevices.getUserMedia(constraints);

        // 4. Sambungkan stream baru ke audioContext yang sama
        //    (audioContext & scriptProcessor tetap jalan — tidak ada gap audio)
        sourceNode = audioContext.createMediaStreamSource(mediaStream);
        sourceNode.connect(scriptProcessor);

        console.log('[Mic] ✓ Berhasil beralih ke mic baru.');

        if (statusInfo) statusInfo.innerHTML = '<i class="fas fa-check-circle" style="color:#16a34a"></i> Mikrofon berhasil dialihkan';
        setTimeout(() => {
            if (statusInfo && isListening) {
                statusInfo.innerHTML = '<i class="fas fa-save"></i> auto-save aktif';
            }
        }, 3000);

    } catch (err) {
        console.error('[Mic] Gagal switch mic:', err);
        if (statusInfo) statusInfo.innerHTML = '<i class="fas fa-exclamation-circle" style="color:red"></i> Gagal beralih mikrofon';

        // Rollback: kembalikan ke mic sebelumnya jika ada track yang masih hidup
        // Jika mediaStream null (sudah di-stop) — sistem tetap berjalan dengan buffer
        // yang tersisa hingga adminnya ganti ke mic yang valid.
    }

    _isSwitchingMic = false;
}


// ══════════════════════════════════════════════════
// Socket.IO Connection
// ══════════════════════════════════════════════════

function connectSocket() {
    if (socket && socket.connected) return Promise.resolve();

    return new Promise((resolve, reject) => {
        socket = io(WHISPER_SERVER, {
            transports: ['websocket', 'polling'],
            reconnection: true,
            reconnectionAttempts: 5,
            reconnectionDelay: 1000,
            timeout: 10000
        });

        socket.on('connect', () => {
            console.log('✓ Connected to Whisper server');
            resolve();
        });

        socket.on('connect_error', (err) => {
            console.error('✗ Connection error:', err);
            updateUI('error', 'Tidak bisa terhubung ke server Whisper. Pastikan web_server.py berjalan.');
            reject(err);
        });

        socket.on('disconnect', () => {
            console.log('Disconnected from server');
            if (isListening) {
                stopListening();
                updateUI('error', 'Koneksi terputus');
            }
        });

        // Event handlers dari server
        socket.on('status_update', handleStatusUpdate);
        socket.on('transcription_update', handleTranscriptionUpdate);
        socket.on('model_ready', handleModelReady);
        socket.on('summarize_done', handleSummarizeDone);

        // Timeout
        setTimeout(() => {
            if (!socket.connected) {
                reject(new Error('Connection timeout'));
            }
        }, 10000);
    });
}


// ══════════════════════════════════════════════════
// Start / Stop Listening
// ══════════════════════════════════════════════════

async function startListening() {
    if (isListening) return;

    // Validasi jika input Judul Rapat kosong
    if (!meetingNameInput || meetingNameInput.value.trim() === '') {
        alert('Harap masukkan "Nama Rapat" terlebih dahulu sebelum memulai transkripsi.');
        if(meetingNameInput) meetingNameInput.focus();
        return;
    }

    // Reset UI
    if (transcriptContent) {
        transcriptContent.innerHTML = '<p class="transcript-placeholder"><i class="fas fa-spinner fa-spin"></i> Menghubungkan ke server...</p>';
    }

    try {
        // 1. Connect ke Socket.IO server
        await connectSocket();

        // 2. Buka mic stream
        const deviceId = micSelect ? micSelect.value : undefined;
        const constraints = {
            audio: {
                deviceId: deviceId ? { exact: deviceId } : undefined,
                sampleRate: { ideal: AUDIO_SAMPLE_RATE },
                channelCount: 1,
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: true
            }
        };

        mediaStream = await navigator.mediaDevices.getUserMedia(constraints);

        // 3. Setup AudioContext untuk capture raw PCM
        audioContext = new (window.AudioContext || window.webkitAudioContext)({
            sampleRate: AUDIO_SAMPLE_RATE
        });

        sourceNode = audioContext.createMediaStreamSource(mediaStream);

        // ScriptProcessorNode untuk mengakses raw audio
        scriptProcessor = audioContext.createScriptProcessor(BUFFER_SIZE, 1, 1);
        scriptProcessor.onaudioprocess = (event) => {
            if (!isListening) return;
            const inputData = event.inputBuffer.getChannelData(0);
            audioChunks.push(new Float32Array(inputData));
        };

        sourceNode.connect(scriptProcessor);
        scriptProcessor.connect(audioContext.destination);

        // 4. Kirim sinyal start ke server (sertakan judul rapat)
        const actualSampleRate = audioContext.sampleRate;
        const judulRapat = meetingNameInput ? meetingNameInput.value.trim() : '';
        socket.emit('start_listening', { sampleRate: actualSampleRate, judul_rapat: judulRapat });

        isListening = true;
        audioChunks = [];
        durationSeconds = 0;

        // 5. Mulai timer kirim audio periodik
        sendTimer = setInterval(sendAudioChunks, SEND_INTERVAL_MS);

        // 6. Mulai timer durasi
        startDurationTimer();

        updateUI('connecting');

    } catch (err) {
        console.error('Failed to start:', err);
        updateUI('error', err.message || 'Gagal memulai. Pastikan server berjalan & mic diizinkan.');
        cleanupAudio();
    }
}


function stopListening() {
    if (!isListening && !socket) return;

    isListening = false;

    // Kirim sisa audio
    sendAudioChunks();

    // Kirim stop ke server
    if (socket && socket.connected) {
        socket.emit('stop_listening');
    }

    // Stop timers
    if (sendTimer) {
        clearInterval(sendTimer);
        sendTimer = null;
    }
    stopDurationTimer();

    // Cleanup audio SAJA — socket TETAP HIDUP agar bisa request_summarize
    cleanupAudio();

    // FIX: Pastikan socket tidak di-disconnect otomatis setelah stop
    // Socket baru ditutup saat halaman di-reset atau di-navigate away

    updateUI('stopping');
}


// ══════════════════════════════════════════════════
// Audio Streaming
// ══════════════════════════════════════════════════

function sendAudioChunks() {
    if (!socket || !socket.connected || audioChunks.length === 0) return;

    // Gabungkan semua chunks menjadi satu Float32Array
    const totalLength = audioChunks.reduce((sum, chunk) => sum + chunk.length, 0);
    const combined = new Float32Array(totalLength);
    let offset = 0;
    for (const chunk of audioChunks) {
        combined.set(chunk, offset);
        offset += chunk.length;
    }

    // Kirim sebagai binary
    socket.emit('audio_data', combined.buffer);

    // Reset chunks
    audioChunks = [];
}


function cleanupAudio() {
    if (scriptProcessor) {
        scriptProcessor.disconnect();
        scriptProcessor = null;
    }
    if (sourceNode) {
        sourceNode.disconnect();
        sourceNode = null;
    }
    if (audioContext) {
        audioContext.close().catch(() => {});
        audioContext = null;
    }
    if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
        mediaStream = null;
    }
    audioChunks = [];
}


// ══════════════════════════════════════════════════
// Server Event Handlers
// ══════════════════════════════════════════════════

function handleStatusUpdate(data) {
    console.log('Status:', data);

    switch (data.status) {
        case 'loading_model':
            updateUI('loading_model');
            if (transcriptContent) {
                transcriptContent.innerHTML = '<p class="transcript-placeholder"><i class="fas fa-spinner fa-spin"></i> Memuat model Whisper (small)... Ini bisa memakan waktu beberapa saat.</p>';
            }
            break;

        case 'listening':
            updateUI('listening');
            if (transcriptContent) {
                transcriptContent.innerHTML = '<p class="transcript-placeholder"><i class="fas fa-microphone fa-beat"></i> Mendengarkan... Silakan berbicara.</p>';
            }
            break;

        case 'stopped':
            updateUI('stopped');
            if (data.saved_path) {
                const filename = data.saved_path.split(/[/\\]/).pop();
                showSavedNotification(filename);
            }
            break;

        case 'summarizing':
            updateUI('summarizing', data.db_id);
            break;

        case 'error':
            updateUI('error', data.message);
            break;
    }
}


function handleTranscriptionUpdate(data) {
    if (!transcriptContent) return;

    const text = data.text || '';
    if (!text) return;

    // Format teks ke HTML
    const paragraphs = text.split(/\n+/).filter(p => p.trim());
    let html = '';

    if (paragraphs.length > 0) {
        html = paragraphs.map(p => `<p>${escapeHtml(p)}</p>`).join('');
    } else {
        html = `<p>${escapeHtml(text)}</p>`;
    }

    // Tambahkan current text dengan highlight
    if (data.current && !data.is_final) {
        html += `<p class="transcript-current">${escapeHtml(data.current)}</p>`;
    }

    if (!data.is_final) {
        html += '<span class="transcript-cursor"></span>';
    }

    transcriptContent.innerHTML = html;

    // Auto-scroll ke bawah
    transcriptContent.scrollTop = transcriptContent.scrollHeight;

    // Simpan teks final
    if (data.is_final) {
        lastFinalText = text;
        // Jika user sudah tekan "Simpan Notulen" sebelum server selesai flush
        if (pendingSave) {
            pendingSave = false;
            _doRequestSummarize(lastFinalText);
        }
    }
}


function handleModelReady(data) {
    console.log('Model ready:', data);
    updateUI('listening');
}


function handleSummarizeDone(data) {
    console.log('Summarize done:', data);

    const summaryPanel = document.getElementById('summaryPanel');

    if (data.status === 'success') {
        const ringkasan = data.ringkasan || '';
        const dbId = data.db_id || '';

        // Tampilkan panel ringkasan
        if (summaryPanel) {
            summaryPanel.style.display = 'block';

            const contentEl = document.getElementById('summaryContent');
            if (contentEl) {
                // Format: paragraf per baris kosong
                const paragraphs = ringkasan.split(/\n\n+/).filter(p => p.trim());
                const html = paragraphs.map(p =>
                    `<p>${escapeHtml(p.trim())}</p>`
                ).join('');
                contentEl.innerHTML = html || `<p>${escapeHtml(ringkasan)}</p>`;
            }

            // Link ke report
            const reportLink = document.getElementById('summaryReportLink');
            if (reportLink && dbId) {
                reportLink.href = `report.php?highlight=${dbId}`;
                reportLink.style.display = 'inline-flex';
            }
        }

        // Update footnote
        const saveInfo = document.querySelector('.save-info');
        if (saveInfo) {
            saveInfo.innerHTML = '<i class="fas fa-check-circle" style="color:#16a34a;"></i> Ringkasan selesai &mdash; tersimpan di database';
        }

        updateUI('summarize_done');

    } else {
        // Error saat summarize
        if (summaryPanel) {
            summaryPanel.style.display = 'block';
            const contentEl = document.getElementById('summaryContent');
            if (contentEl) {
                contentEl.innerHTML = `<p class="transcript-error"><i class="fas fa-exclamation-circle"></i> Gagal membuat ringkasan: ${escapeHtml(data.message || 'Unknown error')}</p>`;
            }
        }
        updateUI('summarize_error');
    }
}


// ══════════════════════════════════════════════════
// UI Updates
// ══════════════════════════════════════════════════

function updateUI(state, extra) {
    if (!statusValue || !startBtn || !stopBtn) return;

    // Remove all status classes
    statusValue.className = 'status-value';

    switch (state) {
        case 'idle':
            statusValue.innerHTML = '<i class="fas fa-pause-circle"></i> Idle';
            statusValue.classList.add('idle');
            startBtn.disabled = false;
            stopBtn.disabled = true;
            startBtn.classList.remove('btn-disabled');
            stopBtn.classList.add('btn-disabled');
            if (liveBadge) liveBadge.classList.remove('live-active');
            _setResetDisabled(false);
            break;

        case 'connecting':
            statusValue.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Menghubungkan...';
            statusValue.classList.add('connecting');
            startBtn.disabled = true;
            stopBtn.disabled = false;
            startBtn.classList.add('btn-disabled');
            stopBtn.classList.remove('btn-disabled');
            _setResetDisabled(true);
            break;

        case 'loading_model':
            statusValue.innerHTML = '<i class="fas fa-cog fa-spin"></i> Memuat Model...';
            statusValue.classList.add('loading');
            startBtn.disabled = true;
            stopBtn.disabled = false;
            startBtn.classList.add('btn-disabled');
            stopBtn.classList.remove('btn-disabled');
            _setResetDisabled(true);
            break;

        case 'listening':
            statusValue.innerHTML = '<i class="fas fa-circle pulse-dot"></i> Listening';
            statusValue.classList.add('listening');
            startBtn.disabled = true;
            stopBtn.disabled = false;
            startBtn.classList.add('btn-disabled');
            stopBtn.classList.remove('btn-disabled');
            if (liveBadge) liveBadge.classList.add('live-active');
            _setResetDisabled(true);
            break;

        case 'stopping':
            statusValue.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Menghentikan...';
            statusValue.classList.add('stopping');
            startBtn.disabled = true;
            stopBtn.disabled = true;
            startBtn.classList.add('btn-disabled');
            stopBtn.classList.add('btn-disabled');
            _setResetDisabled(true);
            break;

        case 'stopped':
            statusValue.innerHTML = '<i class="fas fa-check-circle"></i> Selesai';
            statusValue.classList.add('stopped');
            startBtn.disabled = false;
            stopBtn.disabled = true;
            startBtn.classList.remove('btn-disabled');
            stopBtn.classList.add('btn-disabled');
            if (liveBadge) liveBadge.classList.remove('live-active');
            _setResetDisabled(false);
            break;

        case 'summarizing': {
            statusValue.innerHTML = '<i class="fas fa-brain fa-spin"></i> Membuat Ringkasan...';
            statusValue.classList.add('loading');
            startBtn.disabled = true;
            stopBtn.disabled = true;
            startBtn.classList.add('btn-disabled');
            stopBtn.classList.add('btn-disabled');
            if (liveBadge) liveBadge.classList.remove('live-active');
            _setResetDisabled(true);
            // Tampilkan panel ringkasan dengan indikator loading
            const sp = document.getElementById('summaryPanel');
            if (sp) {
                sp.style.display = 'block';
                const sc = document.getElementById('summaryContent');
                if (sc) sc.innerHTML = '<p class="transcript-placeholder"><i class="fas fa-brain fa-spin"></i> LexRank sedang menganalisis dan merangkum hasil transkripsi...</p>';
            }
            // Scroll ke panel
            if (sp) sp.scrollIntoView({ behavior: 'smooth', block: 'start' });
            break;
        }

        case 'summarize_done': {
            statusValue.innerHTML = '<i class="fas fa-star"></i> Ringkasan Siap';
            statusValue.classList.add('stopped');
            startBtn.disabled = false;
            stopBtn.disabled = true;
            startBtn.classList.remove('btn-disabled');
            stopBtn.classList.add('btn-disabled');
            _setResetDisabled(false);
            break;
        }

        case 'summarize_error': {
            statusValue.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Ringkasan Gagal';
            statusValue.classList.add('error');
            startBtn.disabled = false;
            stopBtn.disabled = true;
            startBtn.classList.remove('btn-disabled');
            stopBtn.classList.add('btn-disabled');
            _setResetDisabled(false);
            break;
        }

        case 'error':
            statusValue.innerHTML = `<i class="fas fa-exclamation-triangle"></i> Error`;
            statusValue.classList.add('error');
            startBtn.disabled = false;
            stopBtn.disabled = true;
            startBtn.classList.remove('btn-disabled');
            stopBtn.classList.add('btn-disabled');
            if (liveBadge) liveBadge.classList.remove('live-active');
            if (extra && transcriptContent) {
                transcriptContent.innerHTML = `<p class="transcript-error"><i class="fas fa-exclamation-circle"></i> ${escapeHtml(extra)}</p>`;
            }
            break;
    }
}


function showSavedNotification(filename) {
    // Tampilkan notifikasi file tersimpan di footnote area
    const footnote = document.querySelector('.footnote');
    if (footnote) {
        const saveInfo = footnote.querySelector('.save-info');
        if (saveInfo) {
            saveInfo.innerHTML = `<i class="fas fa-check-circle" style="color:#16a34a;"></i> Tersimpan: ${escapeHtml(filename)}`;
        }
    }
}


// ══════════════════════════════════════════════════
// Duration Timer
// ══════════════════════════════════════════════════

function startDurationTimer() {
    durationSeconds = 0;
    updateDurationDisplay();
    durationTimer = setInterval(() => {
        durationSeconds++;
        updateDurationDisplay();
    }, 1000);
}

function stopDurationTimer() {
    if (durationTimer) {
        clearInterval(durationTimer);
        durationTimer = null;
    }
}

function updateDurationDisplay() {
    if (!durationDisplay) return;
    const hrs = Math.floor(durationSeconds / 3600);
    const mins = Math.floor((durationSeconds % 3600) / 60);
    const secs = durationSeconds % 60;
    durationDisplay.textContent =
        String(hrs).padStart(2, '0') + ':' +
        String(mins).padStart(2, '0') + ':' +
        String(secs).padStart(2, '0');
}


// ══════════════════════════════════════════════════
// Helpers
// ══════════════════════════════════════════════════

function escapeHtml(text) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}

// ══════════════════════════════════════════════════
// Simpan Notulensi (PDF + Database)
// ══════════════════════════════════════════════════

// ══════════════════════════════════════════════════
// Reset Button Helper
// ══════════════════════════════════════════════════

function _setResetDisabled(disabled) {
    const resetBtn = document.getElementById('resetBtn');
    if (!resetBtn) return;
    if (disabled) {
        resetBtn.classList.add('btn-disabled');
        resetBtn.style.pointerEvents = 'none';
        resetBtn.style.opacity = '0.45';
    } else {
        resetBtn.classList.remove('btn-disabled');
        resetBtn.style.pointerEvents = '';
        resetBtn.style.opacity = '';
    }
}


// ══════════════════════════════════════════════════
// Simpan Notulensi — Alur Baru
// ══════════════════════════════════════════════════

/**
 * Dipanggil saat user klik "Simpan Notulen".
 * - Jika sedang LISTENING → otomatis stop, tunggu is_final, lalu request_summarize
 * - Jika sudah STOP       → langsung request_summarize ke server
 */
window.processSaveNotulensi = function() {
    const title = meetingNameInput ? meetingNameInput.value.trim() : '';
    if (!title) {
        alert('Harap masukkan nama rapat terlebih dahulu.');
        if (meetingNameInput) meetingNameInput.focus();
        return;
    }

    if (isListening) {
        // ── Kasus: Simpan Notulen saat masih listening ──
        // Set flag, lalu stop. handleTranscriptionUpdate akan memanggil
        // _doRequestSummarize secara otomatis setelah is_final diterima.
        pendingSave = true;

        const saveInfo = document.querySelector('.save-info');
        if (saveInfo) saveInfo.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Menghentikan sesi dan menyiapkan ringkasan...';

        stopListening();
        return;
    }

    // ── Kasus: Sudah stop, langsung summarize ──
    const text = lastFinalText || _getTranscriptText();
    if (!text) {
        alert('Tidak ada teks transkripsi untuk disimpan.');
        return;
    }

    _doRequestSummarize(text);
};


/**
 * Ambil teks bersih dari area transkripsi (fallback jika lastFinalText kosong).
 */
function _getTranscriptText() {
    const tc = document.getElementById('transcriptContent');
    if (!tc) return '';
    const raw = tc.innerText || '';
    // Abaikan placeholder
    if (raw.includes('Klik Start Listening') ||
        raw.includes('Mendengarkan...') ||
        raw.includes('Memuat model')) {
        return '';
    }
    return raw.trim();
}


/**
 * Kirim event request_summarize ke server via Socket.IO.
 * Server akan: save_to_db → LexRank → emit summarize_done
 * FIX: Jika socket terputus, lakukan reconnect dulu lalu kirim.
 */
function _doRequestSummarize(text) {
    if (!text || !text.trim()) {
        alert('Tidak ada teks transkripsi untuk disimpan.');
        return;
    }

    const title = meetingNameInput ? meetingNameInput.value.trim() : '';

    // Tampilkan panel + indikator loading
    const summaryPanel = document.getElementById('summaryPanel');
    if (summaryPanel) {
        summaryPanel.style.display = 'block';
        const sc = document.getElementById('summaryContent');
        if (sc) sc.innerHTML = '<p class="transcript-placeholder"><i class="fas fa-spinner fa-spin"></i> Sedang memproses ringkasan...</p>';
        const reportLink = document.getElementById('summaryReportLink');
        if (reportLink) reportLink.style.display = 'none';
    }

    const saveInfo = document.querySelector('.save-info');
    if (saveInfo) saveInfo.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sedang membuat ringkasan...';

    const payload = { text: text, judul_rapat: title };

    // FIX: Jika socket sudah disconnect/null, reconnect dulu
    if (!socket || !socket.connected) {
        console.warn('[Live] Socket terputus, mencoba reconnect untuk request_summarize...');
        if (saveInfo) saveInfo.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Reconnecting ke server...';

        _pendingSummarizePayload = payload;

        connectSocket()
            .then(() => {
                console.log('[Live] Reconnected. Mengirim request_summarize...');
                // Re-register handler summarize_done
                socket.off('summarize_done');
                socket.on('summarize_done', handleSummarizeDone);
                socket.emit('request_summarize', _pendingSummarizePayload);
                _pendingSummarizePayload = null;
            })
            .catch((err) => {
                console.error('[Live] Gagal reconnect:', err);
                if (saveInfo) saveInfo.innerHTML = '<i class="fas fa-exclamation-circle" style="color:red"></i> Gagal reconnect ke server';
                if (summaryPanel) {
                    const sc = document.getElementById('summaryContent');
                    if (sc) sc.innerHTML = '<p class="transcript-error"><i class="fas fa-exclamation-circle"></i> Gagal terhubung ke server. Pastikan server Python berjalan, lalu coba simpan lagi.</p>';
                }
                _pendingSummarizePayload = null;
            });
        return;
    }

    // Socket masih terhubung — langsung kirim
    socket.emit('request_summarize', payload);
}


/**
 * Expose resetTranscription sebagai window function agar bisa dipanggil dari PHP.
 * Reset DIBLOKIR saat isListening === true.
 */
window.resetTranscription = function() {
    if (isListening) {
        alert('Harap hentikan sesi live terlebih dahulu dengan mengklik "End Listening".');
        return;
    }
    // Reset transcript area
    if (transcriptContent) {
        transcriptContent.innerHTML = '<p class="transcript-placeholder"><i class="fas fa-microphone-slash"></i> Klik <strong>Start Listening</strong> untuk memulai transkripsi langsung.</p>';
    }
    // Reset duration timer
    const dur = document.getElementById('durationDisplay');
    if (dur) dur.textContent = '00:00:00';
    durationSeconds = 0;

    // Reset footnote
    const saveInfo = document.querySelector('.save-info');
    if (saveInfo) saveInfo.innerHTML = '<i class="fas fa-save"></i> auto-save aktif';

    // Sembunyikan summary panel
    const sp = document.getElementById('summaryPanel');
    if (sp) sp.style.display = 'none';

    // Reset state
    lastFinalText = '';
    pendingSave   = false;

    updateUI('idle');
};
