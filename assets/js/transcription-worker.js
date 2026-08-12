/**
 * transcription-worker.js
 * =======================
 * SharedWorker yang mengelola:
 *  - Socket.IO client connection ke Whisper server
 *  - Audio buffer accumulation & periodic sending
 *  - Duration timer
 *  - State management (isListening, lastFinalText, pendingSave, dll.)
 *  - Broadcast status/transcription updates ke semua halaman terhubung
 *
 * SharedWorker hidup selama masih ada tab yang terbuka ke origin yang sama.
 * Dilengkapi grace period 8 detik saat semua port disconnect (page transition)
 * agar tidak terminate di tengah navigasi.
 */

// ══════════════════════════════════════════════════
// Import Socket.IO client di dalam Worker
// ══════════════════════════════════════════════════
importScripts('https://cdn.socket.io/4.7.5/socket.io.min.js');

// ══════════════════════════════════════════════════
// Config
// ══════════════════════════════════════════════════
const WHISPER_SERVER = 'http://localhost:5000';
const SEND_INTERVAL_MS = 2000;
// Grace period (ms) sebelum worker dianggap "abandoned" saat 0 port terhubung
const PORT_GRACE_PERIOD_MS = 8000;

// ══════════════════════════════════════════════════
// State
// ══════════════════════════════════════════════════
let socket = null;
let isListening = false;
let audioChunks = [];
let sendTimer = null;
let durationTimer = null;
let durationSeconds = 0;
let pendingSave = false;
let lastFinalText = '';
let lastTranscriptionData = null;
let currentStatus = 'idle';
let _pendingSummarizePayload = null;
let _currentJudulRapat = '';
let _currentSampleRate = 16000;
let lastSummarizeResult = null;

// ── Keep-alive: setInterval agar worker tidak di-GC oleh browser ──
let _keepAliveTimer = null;
// ── Grace period: timer sebelum worker dianggap abandoned (0 ports) ──
let _gracePeriodTimer = null;

// ══════════════════════════════════════════════════
// Connected Ports
// ══════════════════════════════════════════════════
const ports = new Set();
let audioWorkletPort = null;

// ══════════════════════════════════════════════════
// Keep-alive: Cegah worker di-GC saat 0 port selama grace period
// ══════════════════════════════════════════════════
function _startKeepAlive() {
    if (_keepAliveTimer) return;
    _keepAliveTimer = setInterval(() => {
        // Bersihkan port yang sudah mati
        for (const port of ports) {
            try {
                port.postMessage({ type: 'ping' });
            } catch (e) {
                ports.delete(port);
            }
        }
    }, 5000);
}

function _stopKeepAlive() {
    if (_keepAliveTimer) {
        clearInterval(_keepAliveTimer);
        _keepAliveTimer = null;
    }
}

// Selalu jalankan keep-alive agar worker tidak terminate
_startKeepAlive();


// ══════════════════════════════════════════════════
// SharedWorker onconnect
// ══════════════════════════════════════════════════
self.onconnect = function(e) {
    const port = e.ports[0];
    ports.add(port);

    // Batalkan grace period jika ada (tab baru sudah connect)
    if (_gracePeriodTimer) {
        clearTimeout(_gracePeriodTimer);
        _gracePeriodTimer = null;
    }

    port.onmessage = (event) => handlePortMessage(port, event.data);

    // Kirim state saat ini ke tab yang baru connect
    port.postMessage({ type: 'state_sync', state: getCurrentState() });

    if (lastTranscriptionData) {
        port.postMessage({ type: 'transcription_update', data: lastTranscriptionData });
    }
    if (lastSummarizeResult) {
        port.postMessage({ type: 'summarize_done', data: lastSummarizeResult });
    }

    port.start();
};


function getCurrentState() {
    return {
        isListening: isListening,
        durationSeconds: durationSeconds,
        currentStatus: currentStatus,
        lastFinalText: lastFinalText,
        judulRapat: _currentJudulRapat,
        pendingSave: pendingSave,
        workerAlive: true
    };
}


// ══════════════════════════════════════════════════
// Handle Messages from Pages
// ══════════════════════════════════════════════════
function handlePortMessage(port, msg) {
    switch (msg.type) {
        case 'start_listening':
            _currentJudulRapat = msg.judulRapat || '';
            _currentSampleRate = msg.sampleRate || 16000;
            doStartListening(port);
            break;

        case 'stop_listening':
            doStopListening();
            break;

        case 'audio_worklet_port':
            if (msg.port) {
                audioWorkletPort = msg.port;
                audioWorkletPort.onmessage = (e) => {
                    if (e.data.type === 'audio_chunk' && isListening) {
                        audioChunks.push(new Float32Array(e.data.data));
                    }
                };
                audioWorkletPort.start();
            }
            break;

        case 'audio_chunk_direct':
            if (isListening && msg.data) {
                audioChunks.push(new Float32Array(msg.data));
            }
            break;

        case 'request_summarize':
            doRequestSummarize(msg.text, msg.judulRapat);
            break;

        case 'process_save':
            doProcessSave(msg.judulRapat);
            break;

        case 'get_state':
            port.postMessage({ type: 'state_sync', state: getCurrentState() });
            if (lastTranscriptionData) {
                port.postMessage({ type: 'transcription_update', data: lastTranscriptionData });
            }
            if (lastSummarizeResult) {
                port.postMessage({ type: 'summarize_done', data: lastSummarizeResult });
            }
            break;

        case 'reset':
            doReset();
            break;

        case 'pong':
            // Respons keep-alive ping dari halaman — port ini masih hidup
            break;

        case 'disconnect':
            // Halaman memberitahu bahwa mereka akan unload
            ports.delete(port);
            _onPortDisconnect();
            break;
    }
}


/**
 * Dipanggil saat port disconnect (halaman unload).
 * Mulai grace period: tunggu PORT_GRACE_PERIOD_MS ms sebelum
 * reset state jika tidak ada port baru yang connect.
 */
function _onPortDisconnect() {
    // Bersihkan port mati dari Set
    for (const port of ports) {
        try {
            port.postMessage({ type: 'ping' });
        } catch (e) {
            ports.delete(port);
        }
    }

    if (ports.size === 0 && isListening) {
        console.log('[Worker] Semua port disconnect, memulai grace period...');
        // Selama grace period, worker tetap jalan dan socket tetap terhubung
        // Sesi akan tetap berjalan di server
        _gracePeriodTimer = setTimeout(() => {
            // Setelah grace period, jika masih 0 port dan tidak ada sesi penting:
            // Worker dibiarkan idle — jangan stop sesi
            // (Sesi bisa di-resume saat halaman notulensi.php dibuka lagi)
            console.log('[Worker] Grace period selesai, masih menunggu koneksi...');
            _gracePeriodTimer = null;
        }, PORT_GRACE_PERIOD_MS);
    }
}


// ══════════════════════════════════════════════════
// Broadcast ke semua tab
// ══════════════════════════════════════════════════
function broadcast(message) {
    const deadPorts = [];
    for (const port of ports) {
        try {
            port.postMessage(message);
        } catch (e) {
            deadPorts.push(port);
        }
    }
    deadPorts.forEach(p => ports.delete(p));
}


// ══════════════════════════════════════════════════
// Socket.IO Connection
// ══════════════════════════════════════════════════
function connectSocket() {
    if (socket && socket.connected) return Promise.resolve();

    return new Promise((resolve, reject) => {
        // Jika socket exists tapi disconnected, destroy dulu
        if (socket) {
            try { socket.destroy(); } catch(e) {}
            socket = null;
        }

        socket = io(WHISPER_SERVER, {
            transports: ['websocket', 'polling'],
            reconnection: true,
            reconnectionAttempts: Infinity, // Selalu coba reconnect
            reconnectionDelay: 1000,
            reconnectionDelayMax: 5000,
            timeout: 10000
        });

        let resolved = false;

        socket.on('connect', () => {
            console.log('[Worker] ✓ Connected to Whisper server');
            if (!resolved) { resolved = true; resolve(); }
        });

        socket.on('connect_error', (err) => {
            console.error('[Worker] ✗ Connection error:', err.message);
            if (!resolved) {
                resolved = true;
                updateStatus('error', 'Tidak bisa terhubung ke server Whisper.');
                reject(err);
            }
        });

        socket.on('disconnect', (reason) => {
            console.log('[Worker] Disconnected:', reason);
            if (isListening && reason !== 'io client disconnect') {
                updateStatus('error', 'Koneksi terputus. Mencoba reconnect...');
            }
        });

        socket.on('reconnect', (attempt) => {
            console.log('[Worker] Reconnected after', attempt, 'attempts');
            if (isListening) {
                socket.emit('start_listening', {
                    sampleRate: _currentSampleRate,
                    judul_rapat: _currentJudulRapat
                });
                updateStatus('listening');
            }
        });

        socket.on('status_update', handleStatusUpdate);
        socket.on('transcription_update', handleTranscriptionUpdate);
        socket.on('model_ready', handleModelReady);
        socket.on('summarize_done', handleSummarizeDone);

        setTimeout(() => {
            if (!resolved && !socket.connected) {
                resolved = true;
                reject(new Error('Connection timeout'));
            }
        }, 10000);
    });
}


// ══════════════════════════════════════════════════
// Start / Stop Listening
// ══════════════════════════════════════════════════
async function doStartListening(originPort) {
    if (isListening) return;

    updateStatus('connecting');

    try {
        await connectSocket();

        socket.emit('start_listening', {
            sampleRate: _currentSampleRate,
            judul_rapat: _currentJudulRapat
        });

        isListening = true;
        audioChunks = [];
        durationSeconds = 0;
        lastFinalText = '';
        lastTranscriptionData = null;
        lastSummarizeResult = null;

        if (sendTimer) clearInterval(sendTimer);
        sendTimer = setInterval(sendAudioChunks, SEND_INTERVAL_MS);

        if (durationTimer) clearInterval(durationTimer);
        durationTimer = setInterval(() => {
            durationSeconds++;
            broadcast({ type: 'duration_update', seconds: durationSeconds });
            // Broadcast state lengkap setiap 5 detik agar sessionStorage bisa di-update
            if (durationSeconds % 5 === 0) {
                broadcast({ type: 'state_persist', state: getCurrentState() });
            }
        }, 1000);

        updateStatus('connecting');

    } catch (err) {
        console.error('[Worker] Failed to start:', err);
        isListening = false;
        updateStatus('error', err.message || 'Gagal memulai.');
    }
}


function doStopListening() {
    if (!isListening && !socket) return;

    isListening = false;

    sendAudioChunks();

    if (socket && socket.connected) {
        socket.emit('stop_listening');
    }

    if (sendTimer) { clearInterval(sendTimer); sendTimer = null; }
    if (durationTimer) { clearInterval(durationTimer); durationTimer = null; }

    updateStatus('stopping');
    broadcast({ type: 'audio_stopped' });
}


// ══════════════════════════════════════════════════
// Audio Streaming
// ══════════════════════════════════════════════════
function sendAudioChunks() {
    if (!socket || !socket.connected || audioChunks.length === 0) return;

    const totalLength = audioChunks.reduce((sum, chunk) => sum + chunk.length, 0);
    const combined = new Float32Array(totalLength);
    let offset = 0;
    for (const chunk of audioChunks) {
        combined.set(chunk, offset);
        offset += chunk.length;
    }

    socket.emit('audio_data', combined.buffer);
    audioChunks = [];
}


// ══════════════════════════════════════════════════
// Server Event Handlers
// ══════════════════════════════════════════════════
function handleStatusUpdate(data) {
    switch (data.status) {
        case 'loading_model': updateStatus('loading_model'); break;
        case 'listening':     updateStatus('listening');     break;
        case 'stopped':
            updateStatus('stopped');
            if (data.saved_path) {
                broadcast({ type: 'file_saved', filename: data.saved_path.split(/[/\\]/).pop() });
            }
            break;
        case 'summarizing': updateStatus('summarizing', data.db_id); break;
        case 'error':       updateStatus('error', data.message);      break;
    }
}


function handleTranscriptionUpdate(data) {
    lastTranscriptionData = data;

    if (data.is_final) {
        lastFinalText = data.text || '';
        if (pendingSave) {
            pendingSave = false;
            doRequestSummarize(lastFinalText, _currentJudulRapat);
        }
    }

    broadcast({ type: 'transcription_update', data: data });

    // Broadcast state untuk disimpan di sessionStorage
    broadcast({ type: 'state_persist', state: getCurrentState() });
}


function handleModelReady(data) {
    updateStatus('listening');
}


function handleSummarizeDone(data) {
    lastSummarizeResult = data;
    updateStatus(data.status === 'success' ? 'summarize_done' : 'summarize_error');
    broadcast({ type: 'summarize_done', data: data });
}


// ══════════════════════════════════════════════════
// Status Management
// ══════════════════════════════════════════════════
function updateStatus(status, extra) {
    currentStatus = status;
    broadcast({ type: 'status_update', status: status, extra: extra || null });
}


// ══════════════════════════════════════════════════
// Save & Summarize
// ══════════════════════════════════════════════════
function doProcessSave(judulRapat) {
    _currentJudulRapat = judulRapat || _currentJudulRapat;

    if (isListening) {
        pendingSave = true;
        broadcast({ type: 'save_status', message: 'Menghentikan sesi dan menyiapkan ringkasan...' });
        doStopListening();
        return;
    }

    const text = lastFinalText;
    if (!text) {
        broadcast({ type: 'save_error', message: 'Tidak ada teks transkripsi untuk disimpan.' });
        return;
    }

    doRequestSummarize(text, _currentJudulRapat);
}


function doRequestSummarize(text, judulRapat) {
    if (!text || !text.trim()) {
        broadcast({ type: 'save_error', message: 'Tidak ada teks transkripsi untuk disimpan.' });
        return;
    }

    const payload = { text: text, judul_rapat: judulRapat || _currentJudulRapat };
    broadcast({ type: 'save_status', message: 'Sedang membuat ringkasan...' });

    if (!socket || !socket.connected) {
        _pendingSummarizePayload = payload;
        connectSocket()
            .then(() => {
                socket.emit('request_summarize', _pendingSummarizePayload);
                _pendingSummarizePayload = null;
            })
            .catch((err) => {
                broadcast({ type: 'save_error', message: 'Gagal reconnect ke server' });
                _pendingSummarizePayload = null;
            });
        return;
    }

    socket.emit('request_summarize', payload);
}


// ══════════════════════════════════════════════════
// Reset
// ══════════════════════════════════════════════════
function doReset() {
    if (isListening) {
        broadcast({ type: 'reset_blocked', message: 'Harap hentikan sesi live terlebih dahulu.' });
        return;
    }

    durationSeconds = 0;
    lastFinalText = '';
    lastTranscriptionData = null;
    lastSummarizeResult = null;
    pendingSave = false;
    currentStatus = 'idle';

    broadcast({ type: 'state_sync', state: getCurrentState() });
    broadcast({ type: 'reset_done' });
}
