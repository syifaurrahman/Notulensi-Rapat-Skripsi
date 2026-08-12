# pull-ollama-model.ps1 — Script Windows untuk download model Ollama
# Jalankan SEKALI setelah docker compose up berhasil

Write-Host "Menunggu Ollama container siap..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host "Download model llama3.2:3b untuk summarization..." -ForegroundColor Cyan
docker exec notulensi_ollama ollama pull llama3.2:3b

Write-Host ""
Write-Host "Model berhasil didownload!" -ForegroundColor Green
Write-Host "Buka browser: http://localhost" -ForegroundColor Green
