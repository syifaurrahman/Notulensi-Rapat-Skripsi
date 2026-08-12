/**
 * audio-processor-worklet.js
 * ==========================
 * AudioWorkletProcessor yang menangkap raw PCM 16kHz mono
 * dari microphone dan mengirim ke SharedWorker via MessagePort.
 *
 * Digunakan sebagai pengganti ScriptProcessorNode (deprecated)
 * dan lebih tahan terhadap background throttling.
 */

class AudioCaptureProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
        // Buffer untuk mengumpulkan sample sebelum dikirim
        this._buffer = [];
        this._bufferSize = 4096; // Kirim setiap 4096 samples
        this._workerPort = null;

        // Terima MessagePort dari main thread untuk komunikasi ke SharedWorker
        this.port.onmessage = (event) => {
            if (event.data.type === 'init') {
                this._workerPort = event.data.port;
            } else if (event.data.type === 'set_buffer_size') {
                this._bufferSize = event.data.size || 4096;
            }
        };
    }

    process(inputs, outputs, parameters) {
        const input = inputs[0];
        if (!input || input.length === 0) return true;

        const channelData = input[0]; // Mono channel
        if (!channelData || channelData.length === 0) return true;

        // Kumpulkan samples ke buffer
        for (let i = 0; i < channelData.length; i++) {
            this._buffer.push(channelData[i]);
        }

        // Kirim ke SharedWorker saat buffer penuh
        if (this._buffer.length >= this._bufferSize && this._workerPort) {
            const chunk = new Float32Array(this._buffer);
            this._workerPort.postMessage({
                type: 'audio_chunk',
                data: chunk.buffer
            }, [chunk.buffer]); // Transfer ownership untuk performa

            this._buffer = [];
        }

        return true; // Keep processor alive
    }
}

registerProcessor('audio-capture-processor', AudioCaptureProcessor);
