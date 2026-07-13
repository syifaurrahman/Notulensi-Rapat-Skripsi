# Prompt Diagram Arsitektur — Sistem Notulensia (Ringkas & Bersih)

Create a **clean, professional system architecture diagram** for an academic thesis titled **"Automatic Meeting Minutes System (Notulensia)"**. The diagram should be **landscape orientation**, with a clear **left-to-right data flow**, minimal text per block, and a modern flat design style suitable for academic papers.

---

## VISUAL STYLE

- **Layout**: Landscape, left-to-right horizontal flow
- **Background**: Light grey (#F5F7FA)
- **Font**: Inter or Roboto, sans-serif, clean and minimal
- **Arrows**: Bold, dark (#1E293B), clear arrowheads showing data direction
- **Blocks**: Rounded rectangles with subtle drop shadows, max 2 lines text + 1 icon per block
- **Color per zone**:
  - Input: Sky blue (#BFDBFE)
  - Preprocessing: Emerald green (#A7F3D0)
  - ASR Whisper: Amber (#FDE68A)
  - Filters: Rose (#FECDD3)
  - Summarization: Teal (#99F6E4)
  - Output: Indigo (#C7D2FE)

---

## ZONE 1 — INPUT (2 lanes, stacked vertically on the far left)

**[TOP LANE]** — Live Audio Input
- Icons side by side: 🎤 **Microphone** and 🎛️ **Audio Interface**
- Label: `Live Recording`
- Small tag: `WebSocket / Socket.IO`

**[BOTTOM LANE]** — Upload File
- Icon: 📁
- Label: `Upload Video / Audio`
- Small tags: `MP4 · MP3 · WAV` and `REST API`

➜ Both lanes **merge with a single arrow** pointing into Zone 2

---

## ZONE 2 — AUDIO PREPROCESSING (grouped box, label: "Audio Preprocessing")

4 stacked blocks inside a faint green group box:

1. 🎵 **Audio Extraction** *(Upload only · FFmpeg)*
2. 🔇 **Noise Reduction** *(noisereduce · Spectral Gating)*
3. 📊 **Normalize & Resample** *(16kHz · Float32)*
4. ✂️ **Chunking** *(30s · 2s overlap · Upload only)*

> For the Live lane: add a small `VAD` badge on the side of this box instead of Chunking

➜ Arrow pointing RIGHT into Zone 3

---

## ZONE 3 — TRANSCRIPTION (1 large prominent block, center)

🤖 **Whisper ASR**
- `OpenAI Whisper Small`
- `Language: Indonesian (id)`
- `Speech → Text`

➜ Arrow pointing RIGHT into Zone 4

---

## ZONE 4 — TEXT FILTERS (grouped box, label: "Text Post-Processing")

3 stacked filter blocks:

1. 🛡️ **Hallucination Filter**
   - `phrase match · repetition · length check`

2. 🧹 **Word Filler Removal**
   - `eh, um, hmm, nah... → removed`

3. 🌐 **Code-Switching Correction**
   - `chess→CSS · larafel→Laravel · atml→HTML`

➜ Arrow pointing RIGHT into Zone 5

---

## ZONE 5 — SUMMARIZATION + OUTPUT (right side, split vertically)

**[TOP] Summarization** (grouped box, label: "Summarization"):

```
📈 LexRank  →  🧠 Ollama LLM (Llama 3.2:3b)
(Extractive)    (Abstractive · Local AI)
```
Small note on Ollama: *Fallback to LexRank if unavailable*

**[BOTTOM] Storage** (3 small blocks side by side):

- 🗄️ **MySQL DB** · `notulensi_hasil`
- 📂 **Transkrip** · `hasil/*.txt`
- 📝 **Ringkasan** · `LexRank + Ollama .txt`

**[FAR RIGHT] Web App**:

🖥️ **Web Application** *(PHP + Apache)*
- Dashboard · Live · Upload · Report · Model Performance

---

## LAYOUT RULES

1. Each block: **max 2 lines text + 1 icon**. No long sentences.
2. Zone 2 and Zone 4 must have a **visible group box** with label
3. The 2 input lanes **visually merge** before Zone 2
4. LexRank → Ollama shows a **top-to-bottom arrow** inside the Summarization box
5. Storage blocks are **horizontal**, below the Summarization box
6. Add a **small color legend** at the bottom-left corner

---

## SIMPLIFIED FLOW (for reference)

```
[🎤 Mic + 🎛️ Audio Interface]  ──┐
(Live · WebSocket)               ├──→ [Audio Preprocessing] ──→ [Whisper ASR] ──→ [Text Filters]
[📁 Upload MP4/MP3/WAV]   ───────┘    Noise Reduction  · Normalize             Hallucination · Filler · Code-Switch
(REST API)                            Resample · Chunking                                   │
                                      VAD (Live only)                                       ▼
                                                                              [LexRank Extractive]
                                                                                       │
                                                                                       ▼
                                                                              [Ollama Abstractive]
                                                                       ┌───────────────┼──────────────┐
                                                                       ▼               ▼              ▼
                                                                  [MySQL DB]     [Transkrip .txt] [Ringkasan .txt]
                                                                                       │
                                                                                       ▼
                                                                              [🖥️ Web Application]
```

**Priority**: Clean, readable, well-spaced. Suitable for A4 landscape or 16:9 slide. Do NOT overcrowd — use whitespace generously between zones.



