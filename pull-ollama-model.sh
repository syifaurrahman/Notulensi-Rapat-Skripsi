#!/bin/bash
# ============================================================
# pull-ollama-model.sh — Script untuk download model Ollama
# Jalankan SEKALI setelah docker compose up berhasil
# ============================================================

echo "⏳ Menunggu Ollama container siap..."
sleep 5

echo "📥 Download model llama3.2:3b untuk summarization..."
docker exec notulensi_ollama ollama pull llama3.2:3b

echo ""
echo "✅ Model berhasil didownload!"
echo "🌐 Buka browser: http://localhost"
