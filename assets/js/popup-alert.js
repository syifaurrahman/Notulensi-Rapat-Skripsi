/**
 * assets/js/popup-alert.js
 * Komponen popup toast notification — dipakai di semua halaman.
 *
 * Cara pakai dari PHP:
 *   showPopup('Pesan Anda', 'success');  // success | error | warning
 */

function showPopup(message, type = 'success', duration = 3500) {
    // Hapus popup yang sudah ada
    const existing = document.getElementById('custom-popup');
    if (existing) existing.remove();

    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️'
    };

    const colors = {
        success: { bg: '#ecfdf5', border: '#6ee7b7', text: '#065f46', icon: '#10b981' },
        error: { bg: '#fef2f2', border: '#fca5a5', text: '#991b1b', icon: '#ef4444' },
        warning: { bg: '#fffbeb', border: '#fcd34d', text: '#92400e', icon: '#f59e0b' }
    };

    const c = colors[type] || colors.success;

    const popup = document.createElement('div');
    popup.id = 'custom-popup';
    popup.innerHTML = `
        <div style="
            position: fixed;
            top: 24px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 99999;
            background: ${c.bg};
            border: 1.5px solid ${c.border};
            color: ${c.text};
            border-radius: 16px;
            padding: 16px 20px;
            min-width: 300px;
            max-width: 440px;
            box-shadow: 0 12px 32px -8px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            font-weight: 500;
            animation: popupSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        ">
            <span style="font-size: 1.4rem; flex-shrink:0;">${icons[type] || icons.success}</span>
            <span style="flex:1; line-height:1.4;">${message}</span>
            <button onclick="this.closest('#custom-popup').remove()" style="
                background: none; border: none; cursor: pointer;
                color: ${c.text}; font-size: 1.1rem; padding: 2px 4px;
                opacity: 0.6; transition: opacity 0.2s; flex-shrink:0;
            " onmouseenter="this.style.opacity=1" onmouseleave="this.style.opacity=0.6">✕</button>
        </div>
        <style>
            @keyframes popupSlideIn {
                from { opacity: 0; transform: translateX(-50%) translateY(-20px) scale(0.95); }
                to   { opacity: 1; transform: translateX(-50%) translateY(0) scale(1); }
            }
            @keyframes popupSlideOut {
                from { opacity: 1; transform: translateX(-50%) translateY(0) scale(1); }
                to   { opacity: 0; transform: translateX(-50%) translateY(-20px) scale(0.95); }
            }
        </style>
    `;

    document.body.appendChild(popup);

    // Auto-dismiss
    setTimeout(() => {
        const el = document.getElementById('custom-popup');
        if (el) {
            el.querySelector('div').style.animation = 'popupSlideOut 0.35s ease forwards';
            setTimeout(() => el.remove(), 350);
        }
    }, duration);
}
