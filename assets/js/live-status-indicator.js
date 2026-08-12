/**
 * live-status-indicator.js
 * ========================
 * Script kecil yang dimuat di SEMUA halaman (via sidebar.php).
 * Menghubungkan ke SharedWorker transcription-worker.js dan:
 *  - Menampilkan badge "🔴 LIVE" di sidebar nav saat sesi live aktif
 *  - Menyembunyikan badge saat sesi selesai
 *
 * Tidak mengganggu halaman notulensi.php — hanya read-only status.
 */

(function () {
    'use strict';

    // Jangan jalankan jika SharedWorker tidak didukung
    if (typeof SharedWorker === 'undefined') return;

    let worker = null;
    let isLive = false;

    // ── CSS untuk badge LIVE di sidebar ──
    function injectStyles() {
        if (document.getElementById('live-indicator-styles')) return;
        const style = document.createElement('style');
        style.id = 'live-indicator-styles';
        style.textContent = `
            .nav-live-badge {
                display: none;
                align-items: center;
                gap: 4px;
                font-size: 0.6rem;
                font-weight: 700;
                color: #ff4d4d;
                background: rgba(255, 77, 77, 0.12);
                padding: 2px 7px;
                border-radius: 6px;
                margin-left: auto;
                letter-spacing: 0.04em;
                animation: livePulseIndicator 1.8s ease-in-out infinite;
                flex-shrink: 0;
            }
            .nav-live-badge.active {
                display: inline-flex;
            }
            .nav-live-badge i {
                font-size: 0.45rem;
                animation: liveDotPulse 1.2s ease-in-out infinite;
            }
            @keyframes livePulseIndicator {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.65; }
            }
            @keyframes liveDotPulse {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.4; transform: scale(0.7); }
            }

            /* Top bar persistent indicator */
            .live-top-indicator {
                display: none;
                align-items: center;
                gap: 6px;
                font-size: 0.72rem;
                font-weight: 600;
                color: #ff4d4d;
                background: rgba(255, 77, 77, 0.08);
                border: 1px solid rgba(255, 77, 77, 0.2);
                padding: 4px 12px;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.2s;
                animation: livePulseIndicator 1.8s ease-in-out infinite;
            }
            .live-top-indicator:hover {
                background: rgba(255, 77, 77, 0.15);
                border-color: rgba(255, 77, 77, 0.4);
            }
            .live-top-indicator.active {
                display: inline-flex;
            }
            .live-top-indicator i.fa-circle {
                font-size: 0.4rem;
            }
        `;
        document.head.appendChild(style);
    }

    // ── Inject badge ke sidebar nav item "Live" ──
    function injectSidebarBadge() {
        // Cari nav-sub-item yang href-nya menuju notulensi (Live)
        const liveLink = document.querySelector('a.nav-sub-item[href*="notulensi"]');
        if (!liveLink) return null;

        // Cek apakah badge sudah ada
        let badge = liveLink.querySelector('.nav-live-badge');
        if (badge) return badge;

        badge = document.createElement('span');
        badge.className = 'nav-live-badge';
        badge.innerHTML = '<i class="fas fa-circle"></i> LIVE';
        liveLink.appendChild(badge);

        return badge;
    }

    // ── Inject badge ke top-bar (visible di semua halaman saat live) ──
    function injectTopBarIndicator() {
        const topBar = document.querySelector('.top-bar');
        if (!topBar) return null;

        let indicator = document.getElementById('liveTopIndicator');
        if (indicator) return indicator;

        indicator = document.createElement('a');
        indicator.id = 'liveTopIndicator';
        indicator.className = 'live-top-indicator';
        indicator.href = 'notulensi';
        indicator.innerHTML = '<i class="fas fa-circle"></i> LIVE <i class="fas fa-broadcast-tower"></i>';
        indicator.title = 'Sesi live transcription sedang berjalan — klik untuk kembali';

        // Sisipkan sebelum header-date
        const headerDate = topBar.querySelector('.header-date');
        if (headerDate) {
            topBar.insertBefore(indicator, headerDate);
        } else {
            topBar.appendChild(indicator);
        }

        return indicator;
    }

    function updateIndicators(live) {
        isLive = live;

        const sidebarBadge = injectSidebarBadge();
        const topIndicator = injectTopBarIndicator();

        if (sidebarBadge) {
            sidebarBadge.classList.toggle('active', live);
        }

        // Hanya tampilkan top indicator jika BUKAN di halaman notulensi
        const isNotulensiPage = window.location.pathname.includes('notulensi') &&
                                !window.location.pathname.includes('notulensi_upload');
        if (topIndicator) {
            topIndicator.classList.toggle('active', live && !isNotulensiPage);
        }
    }

    // ── Connect ke SharedWorker ──
    function connectToWorker() {
        try {
            // Resolve path relatif ke assets/js/
            const basePath = document.querySelector('script[src*="live-status-indicator"]');
            let workerUrl = 'assets/js/transcription-worker.js';

            // Jika script dimuat dari subdirectory, coba detect path
            if (basePath) {
                const src = basePath.getAttribute('src');
                workerUrl = src.replace('live-status-indicator.js', 'transcription-worker.js');
            }

            worker = new SharedWorker(workerUrl, { name: 'transcription-engine' });

            worker.port.onmessage = (event) => {
                const msg = event.data;

                if (msg.type === 'state_sync') {
                    updateIndicators(msg.state.isListening);
                } else if (msg.type === 'status_update') {
                    const liveStatuses = ['connecting', 'loading_model', 'listening'];
                    updateIndicators(liveStatuses.includes(msg.status));
                } else if (msg.type === 'audio_stopped') {
                    updateIndicators(false);
                }
            };

            worker.port.start();

            // Request current state
            worker.port.postMessage({ type: 'get_state' });

        } catch (e) {
            console.warn('[LiveIndicator] SharedWorker not available:', e);
        }
    }

    // ── Init ──
    document.addEventListener('DOMContentLoaded', () => {
        injectStyles();
        connectToWorker();
    });

})();
