@echo off
TITLE Whitebox Testing Runner
COLOR 0A

echo ========================================================
echo   WHITEBOX TESTING — NOTULENSI RAPAT
echo ========================================================
echo.

cd /d c:\laragon\www\notulensi_rapat\tests

echo [1/3] Memeriksa dan Menginstall Library dependensi...
call "c:\laragon\www\notulensi_rapat\.venv\Scripts\pip.exe" install "pytest<8.4.0" pytest-html-reporter numpy scipy scikit-learn requests
echo.

echo [2/3] Menjalankan 117 Whitebox Test Cases...
call "c:\laragon\www\notulensi_rapat\.venv\Scripts\python.exe" -m pytest whitebox/ -v --html-report=./whitebox/report.html
echo.

echo [3/3] Membuka laporan di browser...
if exist "whitebox\report.html" (
    echo [OK] File report.html berhasil dibuat!
    start whitebox\report.html
) else if exist "report.html" (
    echo [OK] File report.html berhasil dibuat!
    start report.html
) else (
    echo [ERR] File report.html belum terbentuk. Periksa pesan error di jendela terminal di atas.
)

echo.
echo ========================================================
echo   SELESAI!
echo ========================================================
echo.
pause
