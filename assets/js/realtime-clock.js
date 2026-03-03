/**
 * realtime-clock.js
 * Update elemen #realtime-clock setiap detik dengan
 * format: Kamis, 20 Feb 2026 · 02:15:30 WIB
 */

const HARI  = ['Minggu','Senin','Selasa','Rabu','Kamis','Jumat','Sabtu'];
const BULAN = ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des'];

function updateClock() {
    const el = document.getElementById('realtime-clock');
    if (!el) return;

    const now = new Date();

    const hari    = HARI[now.getDay()];
    const tgl     = now.getDate();
    const bulan   = BULAN[now.getMonth()];
    const tahun   = now.getFullYear();
    const jam     = String(now.getHours()).padStart(2, '0');
    const menit   = String(now.getMinutes()).padStart(2, '0');
    const detik   = String(now.getSeconds()).padStart(2, '0');

    el.textContent = `${hari}, ${tgl} ${bulan} ${tahun}  ·  ${jam}:${menit}:${detik} WIB`;
}

// Jalankan langsung agar tidak ada delay 1 detik
updateClock();
setInterval(updateClock, 1000);
