# LAPORAN EVALUASI DETEKSI HALLUCINATION FILTER
Dokumen ini berisi hasil pengujian keandalan Hallucination Filter pada 3 kondisi pengujian (Hening, Noise, dan Percakapan Latar) dengan masing-masing 5 kali percobaan.

### Tabel 4.1 Hasil Pengujian Hallucination Filter pada Kondisi Hening

| No | Output Whisper | Ground Truth | Output Hallucination Filter | Kategori | TP | FP | FN | TN |
|----|----------------|--------------|-----------------------------|----------|----|----|----|----|
| | **Percobaan 1 (File: Hallufilter_1.txt)** | | | | | | | |
| 1 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 2 | 'Is that...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 3 | 'Is that?' | Hening | 'Is that?' | FN | 0 | 0 | 1 | 0 |
| 4 | 'Is that it?' | Hening | 'Is that it?' | FN | 0 | 0 | 1 | 0 |
| 5 | 'Is that it? Yes.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 6 | 'Is that, yes, if you see it.' | Hening | 'Is that, yes, if you see it.' | FN | 0 | 0 | 1 | 0 |
| 7 | 'Is that it? Yes, if you see it.' | Hening | 'Is that it? Yes, if you see it.' | FN | 0 | 0 | 1 | 0 |
| 8 | 'Just that, if you see it.' | Hening | 'Just that, if you see it.' | FN | 0 | 0 | 1 | 0 |
| 9 | 'Is that, yes, if you see it.' | Hening | 'Is that, yes, if you see it.' | FN | 0 | 0 | 1 | 0 |
| 10 | 'Pesan, pesan, pesan.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 11 | 'Pesan, pesan, pesan. Dijik-dijik-dijik.' | Hening | 'Pesan, pesan, pesan. Dijik-dijik-dijik.' | FN | 0 | 0 | 1 | 0 |
| 12 | 'Pesan, pesan, pesan. Dijik-dijik-dijik.' | Hening | 'Pesan, pesan, pesan. Dijik-dijik-dijik.' | FN | 0 | 0 | 1 | 0 |
| 13 | 'Pesan, Pesan, Pesan. Kami akan menggunakan bahasa Inggris. Saya harus melihat bahasa Inggris. Kami akan menggunakan bahasa Inggris. Kami akan menggunakan bahasa Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 14 | 'Pesan, Pesan, Pesan. Kami akan membuat pembantu. Saya perlu melihatnya. Terima kasih. Terima kasih. Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 15 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 16 | 'Terima kasih. Okay, wow. Jangan lupa, jangan lupa, jangan lupa. Terima kasih. Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 17 | 'Terima kasih. Okay, wow. Jangan lupa, jangan lupa, jangan lupa. Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 18 | 'Okay, wow, if she takes first boot, she's gonna... Is it on us? Sure. I'm gonna hate text.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 19 | 'Okay, wow, if she takes first boot, she's gonna, it's not, sure, I don't need to, just, I don't need to.' | Hening | 'Okay, wow, if she takes first boot, she's gonna, it's not, sure, I don't need to, just, I don't need to.' | FN | 0 | 0 | 1 | 0 |
| 20 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 21 | 'Please stay party.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 22 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 23 | 'Please stay quiet, we will teach you.' | Hening | 'Please stay quiet, we will teach you.' | FN | 0 | 0 | 1 | 0 |
| 24 | 'Pada setelah ini, saya akan mengajar.' | Hening | 'Pada setelah ini, saya akan mengajar.' | FN | 0 | 0 | 1 | 0 |
| 25 | 'Insighting, if you need teaching, be humble.' | Hening | 'Insighting, if you need teaching, be humble.' | FN | 0 | 0 | 1 | 0 |
| 26 | 'Please get mighty, we will teach you, be humble, yes.' | Hening | 'Please get mighty, we will teach you, be humble, yes.' | FN | 0 | 0 | 1 | 0 |
| 27 | 'Please get mighty, we need teaching, behind the, yeah.' | Hening | 'Please get mighty, we need teaching, behind the, yeah.' | FN | 0 | 0 | 1 | 0 |
| 28 | 'Pertahankan kata-kata, we need to teach you, behind the scenes.' | Hening | 'Pertahankan kata-kata, we need to teach you, behind the scenes.' | FN | 0 | 0 | 1 | 0 |
| 29 | 'Please get my key, we need to teach you, be humble, yeah, listen.' | Hening | 'Please get my key, we need to teach you, be humble, yeah, listen.' | FN | 0 | 0 | 1 | 0 |
| 30 | 'Bersama, kita akan mengajar, di-hunger, ya, listen, draft, listen, view.' | Hening | 'Bersama, kita akan mengajar, di-hunger, ya, listen, draft, listen, view.' | FN | 0 | 0 | 1 | 0 |
| 31 | 'Pertahankan kata-kata, we need to teach you, be humble, yeah, listen to this, please hear me.' | Hening | 'Pertahankan kata-kata, we need to teach you, be humble, yeah, listen to this, please hear me.' | FN | 0 | 0 | 1 | 0 |
| 32 | 'Pertahankan kata-kata, we need to teach you, be humble, yeah, listen, this is the end of the day.' | Hening | 'Pertahankan kata-kata, we need to teach you, be humble, yeah, listen, this is the end of the day.' | FN | 0 | 0 | 1 | 0 |
| 33 | 'Pertahankan kata-kata inggris menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | Hening | 'Pertahankan kata-kata inggris menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | FN | 0 | 0 | 1 | 0 |
| 34 | 'Pertahankan kata-kata inggris menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | Hening | 'Pertahankan kata-kata inggris menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | FN | 0 | 0 | 1 | 0 |
| 35 | 'Dismisai.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 36 | 'Pertahankan kata-kata, you need to teach you, be humble, yeah, listen, this is me. Anyway, I'm going to give you a yes, I need to see more, take you.' | Hening | 'Pertahankan kata-kata, you need to teach you, be humble, yeah, listen, this is me. Anyway, I'm going to give you a yes, I need to see more, take you.' | FN | 0 | 0 | 1 | 0 |
| 37 | 'Jalan!' | Hening | 'Jalan!' | FN | 0 | 0 | 1 | 0 |
| 38 | 'I need to see.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 39 | 'Ken, I need to see more.' | Hening | 'Ken, I need to see more.' | FN | 0 | 0 | 1 | 0 |
| 40 | 'Gen, I need to see more.' | Hening | 'Gen, I need to see more.' | FN | 0 | 0 | 1 | 0 |
| 41 | 'I need to see more.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 42 | 'I need to see more, can you?' | Hening | 'I need to see more, can you?' | FN | 0 | 0 | 1 | 0 |
| 43 | 'Can, I need to see more, can you do it?' | Hening | 'Can, I need to see more, can you do it?' | FN | 0 | 0 | 1 | 0 |
| 44 | 'Can, I need to see more. Can you give me more?' | Hening | 'Can, I need to see more. Can you give me more?' | FN | 0 | 0 | 1 | 0 |
| 45 | 'I need to see more. Can you give me more?' | Hening | 'I need to see more. Can you give me more?' | FN | 0 | 0 | 1 | 0 |
| 46 | 'Gen, you're trying to see more, can you give me more, understand, sir?' | Hening | 'Gen, you're trying to see more, can you give me more, understand, sir?' | FN | 0 | 0 | 1 | 0 |
| 47 | 'Ken, I need to see more, can you give me more, understand family, can you...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 48 | 'Gen, you're trying to see more, can you give me more, understand, sir, if you need more.' | Hening | 'Gen, you're trying to see more, can you give me more, understand, sir, if you need more.' | FN | 0 | 0 | 1 | 0 |
| 49 | 'Gen, you're trying to see more, can you give me more, understand, sir, if you need my end, down the line.' | Hening | 'Gen, you're trying to see more, can you give me more, understand, sir, if you need my end, down the line.' | FN | 0 | 0 | 1 | 0 |
| 50 | 'Sen, you're trying to see more, can you give me more, understand, sen, can you use YN, download your sen?' | Hening | 'Sen, you're trying to see more, can you give me more, understand, sen, can you use YN, download your sen?' | FN | 0 | 0 | 1 | 0 |
| 51 | 'Jeff, you're trying to see more. Can you give me more? Understand, Jeff, if you do YN, you're having fun. You're a chef, you're an engineer, you're living by dream.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 52 | 'Sen, you're trying to see more. Can you give me more, understand, sen? Can you use YN, download, yourself, engineer, and your little country?' | Hening | 'Sen, you're trying to see more. Can you give me more, understand, sen? Can you use YN, download, yourself, engineer, and your little country?' | FN | 0 | 0 | 1 | 0 |
| 53 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 54 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 55 | 'Okay.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 56 | 'Thank you.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 57 | 'Okay.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 58 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 59 | 'Thank you.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 60 | 'DB.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 61 | 'Thank you.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 62 | 'Deep learning.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 63 | 'DDP, asempen.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 64 | 'Dia bilang, asemben, contoh.' | Hening | 'Dia bilang, asemben, contoh.' | FN | 0 | 0 | 1 | 0 |
| 65 | 'Dia biar saya berbicara tentang...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 66 | 'Tidak menggunakan bahasa Inggris.' | Hening | 'Tidak menggunakan bahasa Inggris.' | FN | 0 | 0 | 1 | 0 |
| 67 | 'Diapain, asempat, pijujung, dilihat.' | Hening | 'Diapain, asempat, pijujung, dilihat.' | FN | 0 | 0 | 1 | 0 |
| 68 | 'DDP, asempen, future, yes.' | Hening | 'DDP, asempen, future, yes.' | FN | 0 | 0 | 1 | 0 |
| 69 | 'DDP, and Zephyr, the future here.' | Hening | 'DDP, and Zephyr, the future here.' | FN | 0 | 0 | 1 | 0 |
| 70 | 'Thank you.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 71 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 72 | 'Pertahankan.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 73 | 'Cik.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 74 | 'Tch.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 75 | 'Cik.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 76 | 'Thank you.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 77 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 78 | *(Hening Sempurna)* | Hening | *(Kosong)* | TN | 0 | 0 | 0 | 59 |
| | **Percobaan 2 (File: Hallufilter_2.txt)** | | | | | | | |
| 79 | *(Hening Sempurna)* | Hening | *(Kosong)* | TN | 0 | 0 | 0 | 475 |
| | **Percobaan 3 (File: Hallufilter_3.txt)** | | | | | | | |
| 80 | *(Hening Sempurna)* | Hening | *(Kosong)* | TN | 0 | 0 | 0 | 472 |
| | **Percobaan 4 (File: Hallufilter_4.txt)** | | | | | | | |
| 81 | *(Hening Sempurna)* | Hening | *(Kosong)* | TN | 0 | 0 | 0 | 474 |
| | **Percobaan 5 (File: Hallufilter_5.txt)** | | | | | | | |
| 82 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 83 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 84 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 85 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 86 | 'Pertahankan kata-kata ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | Hening | 'Pertahankan kata-kata ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | FN | 0 | 0 | 1 | 0 |
| 87 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 88 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan.' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan.' | FN | 0 | 0 | 1 | 0 |
| 89 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh,' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh,' | FN | 0 | 0 | 1 | 0 |
| 90 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan.' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan.' | FN | 0 | 0 | 1 | 0 |
| 91 | 'Kami menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang meng' | Hening | 'Kami menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang menggunakan bahasa Inggris apa yang meng' | FN | 0 | 0 | 1 | 0 |
| 92 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 93 | 'I'm just gonna start with the things that I've learned from the past. I'm just gonna start with the things that I've learned from the past. I'm just gonna start with the things that I've learned from the past. I'm just gonna start with the things that I've learned from the past. I'm just gonna start with the things that I've learned from the past. I'm just gonna start with the things that I've learned from the past. I'm just gonna start with the things that I've learned from the past.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 94 | 'Pertahankan kata-kata, asa yang akan diperkenalkan. Pertahankan kata-kata, asa yang akan diperkenalkan. Pertahankan kata-kata, asa yang akan diperkenalkan.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 95 | 'Pertahankan kata-kata, dan menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris. Pertahankan kata-kata, dan menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris. Pertahankan kata-kata, dan menggunakan bahasa Inggris. Pertahankan kata-kata, dan menggunakan bahasa Inggris. Pertahankan kata-kata, dan menggunakan bahasa Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 96 | 'Pertahankan kata-kata,' | Hening | 'Pertahankan kata-kata,' | FN | 0 | 0 | 1 | 0 |
| 97 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh, machine learning, deep learning, framework, update, meeting, development, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data,' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh, machine learning, deep learning, framework, update, meeting, development, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data, data,' | FN | 0 | 0 | 1 | 0 |
| 98 | 'Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan' | Hening | 'Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan' | FN | 0 | 0 | 1 | 0 |
| 99 | 'Pertahankan kata-kata, Pertahankan kata-kata,' | Hening | 'Pertahankan kata-kata, Pertahankan kata-kata,' | FN | 0 | 0 | 1 | 0 |
| 100 | 'I think it's a good thing to be able to do that. I'm not going to be doing that. I'm going to do that. I'm going to do that. I'm going to do that. I'm going to do that. I'm going to do that. I'm going to do that.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 101 | 'Can you hear me? Can you hear me? Can you hear me? Can you hear me? Can you hear me? Can you hear me? Can you hear me? Can you hear me?' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 102 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 103 | 'Pertahankan kata-kata Inggris. Pertahankan kata-kata Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 104 | *(Hening Sempurna)* | Hening | *(Kosong)* | TN | 0 | 0 | 0 | 159 |
| | **TOTAL REKAPITULASI** | | | | **48** | **0** | **51** | **1639** |

**Metrik Performa Hening:**
- **Accuracy** = 97.07%
- **Precision** = 100.00%
- **Recall** = 48.48%
- **F1-Score** = 65.31%

---

### Tabel 4.2 Hasil Pengujian Hallucination Filter pada Kondisi Noise

| No | Output Whisper | Ground Truth | Output Hallucination Filter | Kategori | TP | FP | FN | TN |
|----|----------------|--------------|-----------------------------|----------|----|----|----|----|
| | **Percobaan 1 (File: Hallufilter_6.txt)** | | | | | | | |
| 1 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 2 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 3 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 4 | 'Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 5 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 6 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 7 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 8 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 9 | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan.' | Hening | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan.' | FN | 0 | 0 | 1 | 0 |
| 10 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 11 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 12 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh,' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh,' | FN | 0 | 0 | 1 | 0 |
| 13 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan.' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan.' | FN | 0 | 0 | 1 | 0 |
| 14 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 15 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 16 | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan.' | Hening | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan.' | FN | 0 | 0 | 1 | 0 |
| 17 | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan. Contoh, Terima kasih kerana menonton.' | Hening | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan. Contoh, Terima kasih kerana menonton.' | FN | 0 | 0 | 1 | 0 |
| 18 | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan. Contoh, Terima kasih.' | Hening | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan. Contoh, Terima kasih.' | FN | 0 | 0 | 1 | 0 |
| 19 | 'Pertahankan kata-kata,' | Hening | 'Pertahankan kata-kata,' | FN | 0 | 0 | 1 | 0 |
| 20 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan,' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan,' | FN | 0 | 0 | 1 | 0 |
| 21 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan,' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan,' | FN | 0 | 0 | 1 | 0 |
| 22 | 'Pertahankan kata-kata, pilihnya, melihat kecantikan, memperhatikan, melihat, melihat, melihat, melihat, melihat, melihat, melihat, melihat, melihat, melihat, melihat, melihat, melihat, melihat, melihat, melihat.' | Hening | 'Pertahankan kata-kata, pilihnya, melihat kecantikan, memperhatikan, melihat, melihat, melihat, melihat, melihat, melihat, melihat, melihat, melihat, melihat, melihat, melihat, melihat, melihat, melihat, melihat.' | FN | 0 | 0 | 1 | 0 |
| 23 | 'Pertahankan kata-kata, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan.' | Hening | 'Pertahankan kata-kata, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan, Pertahankan.' | FN | 0 | 0 | 1 | 0 |
| 24 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 25 | 'Bagaimana dengan perasaan, perasaan, perasaan, perasaan, perasaan, perasaan? Bagaimana dengan perasaan, perasaan, perasaan, perasaan, perasaan, perasaan?' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 26 | 'Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 27 | 'Bagaimana dengan penggunaan kemarenan? Kami akan membuat perusahaan untuk menggunakan bahasa Indonesia. Kami akan membuat perusahaan untuk menggunakan bahasa Indonesia. Kami akan membuat perusahaan untuk menggunakan bahasa Indonesia. Kami akan membuat perusahaan untuk menggunakan bahasa Indonesia. Kami akan membuat perusahaan untuk menggunakan bahasa Indonesia.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 28 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 29 | 'Pertahankan kata-kata,' | Hening | 'Pertahankan kata-kata,' | FN | 0 | 0 | 1 | 0 |
| 30 | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan' | Hening | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan' | FN | 0 | 0 | 1 | 0 |
| 31 | 'Pertahankan kata-kata,' | Hening | 'Pertahankan kata-kata,' | FN | 0 | 0 | 1 | 0 |
| 32 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan,' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan,' | FN | 0 | 0 | 1 | 0 |
| 33 | 'Pertahankan kata-kata,' | Hening | 'Pertahankan kata-kata,' | FN | 0 | 0 | 1 | 0 |
| 34 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan,' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan,' | FN | 0 | 0 | 1 | 0 |
| 35 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh,' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh,' | FN | 0 | 0 | 1 | 0 |
| 36 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh-kata Inggris apa adanya, jangan diterjemahkan.' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh-kata Inggris apa adanya, jangan diterjemahkan.' | FN | 0 | 0 | 1 | 0 |
| 37 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh-kata Inggris apa adanya, jangan diterjemahkan.' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh-kata Inggris apa adanya, jangan diterjemahkan.' | FN | 0 | 0 | 1 | 0 |
| 38 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 39 | 'Pertahankan kata-kata, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA' | Hening | 'Pertahankan kata-kata, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA, PTA' | FN | 0 | 0 | 1 | 0 |
| 40 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 41 | *(Hening Sempurna)* | Hening | *(Kosong)* | TN | 0 | 0 | 0 | 94 |
| | **Percobaan 2 (File: Hallufilter_7.txt)** | | | | | | | |
| 42 | 'Diperluasakan bahasa Inggris, memiliki perusahaan menggunakan bahasa Inggris. Pertahankan kata-kata Inggris, memiliki perusahaan menggunakan bahasa Inggris. Pertahankan kata-kata Inggris, memiliki perusahaan menggunakan bahasa Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 43 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 44 | 'Pertahankan kata-kata,' | Hening | 'Pertahankan kata-kata,' | FN | 0 | 0 | 1 | 0 |
| 45 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh,' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh,' | FN | 0 | 0 | 1 | 0 |
| 46 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan,' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan,' | FN | 0 | 0 | 1 | 0 |
| 47 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh,' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh,' | FN | 0 | 0 | 1 | 0 |
| 48 | 'Tidak ada yang menggunakan bahasa Inggris. Pada tahun 2020, diperkenalkan bahasa Inggris, dan menggunakan bahasa Inggris. Pada tahun 2020, diperkenalkan bahasa Inggris. Pada tahun 2020, diperkenalkan bahasa Inggris. Pada tahun 2020, diperkenalkan bahasa Inggris. Pada tahun 2020, diperkenalkan bahasa Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 49 | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan. Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 50 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 51 | 'Pertahankan kata-kata ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | Hening | 'Pertahankan kata-kata ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | FN | 0 | 0 | 1 | 0 |
| 52 | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan.' | Hening | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan.' | FN | 0 | 0 | 1 | 0 |
| 53 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan.' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan.' | FN | 0 | 0 | 1 | 0 |
| 54 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh-kata Inggris apa adanya, jangan diterjemahkan.' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh-kata Inggris apa adanya, jangan diterjemahkan.' | FN | 0 | 0 | 1 | 0 |
| 55 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh-kata Inggris apa adanya, jangan diterjemahkan. Contoh-kata Inggris apa adanya.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 56 | 'Pertahankan kata-kata, asa maaf, iya. Pertahankan kata-kata, asa maaf, iya. Pertahankan kata-kata, asa maaf, iya. Pertahankan kata-kata, asa maaf, iya. Pertahankan kata-kata, asa maaf, iya. Pertahankan kata-kata, asa maaf, iya.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 57 | 'Pertahankan kata-kata, asa maaf, iya. Pertahankan kata-kata, asa maaf, iya. Pertahankan kata-kata, asa maaf, iya. Pertahankan kata-kata, asa maaf, iya. Pertahankan kata-kata, asa maaf, iya. Pertahankan kata-kata, asa maaf, iya.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 58 | 'Bersama saya, saya menggunakan bahasa Inggris. Saya menggunakan bahasa Inggris. Saya menggunakan bahasa Inggris. Saya menggunakan bahasa Inggris. Saya menggunakan bahasa Inggris. Saya menggunakan bahasa Inggris. Saya menggunakan bahasa Inggris. Saya menggunakan bahasa Inggris. Saya menggunakan bahasa Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 59 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 60 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 61 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan.' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan.' | FN | 0 | 0 | 1 | 0 |
| 62 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh.' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh.' | FN | 0 | 0 | 1 | 0 |
| 63 | 'Pertahankan kata-kata ini menggunakan bahasa Inggris. Pertahankan kata-kata ini menggunakan bahasa Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 64 | 'Pertahankan kata-kata ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | Hening | 'Pertahankan kata-kata ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | FN | 0 | 0 | 1 | 0 |
| 65 | 'Maksudnya, bahasa Indonesia ini akan melakukan perangkatan, untuk melakukan perangkatan, untuk melakukan perangkatan, untuk melakukan perangkatan, untuk melakukan perangkatan, untuk melakukan perangkatan, untuk melakukan perangkatan, untuk melakukan perangkatan.' | Hening | 'Maksudnya, bahasa Indonesia ini akan melakukan perangkatan, untuk melakukan perangkatan, untuk melakukan perangkatan, untuk melakukan perangkatan, untuk melakukan perangkatan, untuk melakukan perangkatan, untuk melakukan perangkatan, untuk melakukan perangkatan.' | FN | 0 | 0 | 1 | 0 |
| 66 | 'Bagi saya, saya akan menggunakan bahasa Inggris yang menggunakan bahasa Inggris. Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh, ini adalah bahasa Inggris. Contoh, ini adalah bahasa Inggris. Pertahankan kata-kata Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 67 | 'Bagi saya, saya akan menggunakan bahasa Inggris yang menggunakan bahasa Inggris. Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh, ini adalah bahasa Inggris. Contoh, ini adalah bahasa Inggris. Pertahankan kata-kata Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 68 | 'Pertahankan kata-kata, Kami dapat mengikuti sebuah pembukaan yang bisa dikenali di dalam perjalanan. Kami dapat mengikuti sebuah pembukaan yang bisa dikenali di dalam perjalanan. Kami akan mengikuti pembukaan yang bisa dikenali di dalam perjalanan.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 69 | 'Pertahankan kata-kata ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | Hening | 'Pertahankan kata-kata ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | FN | 0 | 0 | 1 | 0 |
| 70 | 'Thank you.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 71 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 72 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 73 | 'Pertahankan kata-kata ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | Hening | 'Pertahankan kata-kata ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | FN | 0 | 0 | 1 | 0 |
| 74 | 'Pertahankan kata-kata ini menggunakan bahasa Inggris. Pertahankan kata-kata ini menggunakan bahasa Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 75 | 'Pertahankan kata-kata ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | Hening | 'Pertahankan kata-kata ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | FN | 0 | 0 | 1 | 0 |
| 76 | 'Pertahankan kata-kata ini menggunakan bahasa Inggris. Pertahankan kata-kata ini menggunakan bahasa Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 77 | 'Bersama saya, saya melihat bahasa Indonesia yang menyerahkan bahasa Indonesia. Bersama saya, saya melihat bahasa Indonesia yang menyerahkan bahasa Indonesia. Bersama saya, saya melihat bahasa Indonesia yang menyerahkan bahasa Indonesia. Bersama saya, saya melihat bahasa Indonesia yang menyerahkan bahasa Indonesia.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 78 | 'Pertahankan kata-kata ini menggunakan bahasa Inggris. Pertahankan kata-kata ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | Hening | 'Pertahankan kata-kata ini menggunakan bahasa Inggris. Pertahankan kata-kata ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | FN | 0 | 0 | 1 | 0 |
| 79 | *(Hening Sempurna)* | Hening | *(Kosong)* | TN | 0 | 0 | 0 | 20 |
| | **Percobaan 3 (File: Hallufilter_8.txt)** | | | | | | | |
| 80 | 'Pertahankan kata-kata,' | Hening | 'Pertahankan kata-kata,' | FN | 0 | 0 | 1 | 0 |
| 81 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 82 | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan. Contoh, Terima kasih kerana menonton.' | Hening | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan. Contoh, Terima kasih kerana menonton.' | FN | 0 | 0 | 1 | 0 |
| 83 | 'Pertahankan kata-kata,' | Hening | 'Pertahankan kata-kata,' | FN | 0 | 0 | 1 | 0 |
| 84 | 'Bersama saya, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggr' | Hening | 'Bersama saya, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggris, saya menggunakan bahasa Inggr' | FN | 0 | 0 | 1 | 0 |
| 85 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 86 | 'We're going to go back to the first part, okay, and then we'll start with the next part, which is the main part, which is the main part. Okay, so let's go back to the first part, okay.' | Hening | 'We're going to go back to the first part, okay, and then we'll start with the next part, which is the main part, which is the main part. Okay, so let's go back to the first part, okay.' | FN | 0 | 0 | 1 | 0 |
| 87 | 'Bagi yang kita lihat, kita akan membuat dari ini, kita akan membuat dari ini, kita akan membuat dari ini, kita akan membuat dari ini. Kita akan membuat dari ini, kita akan membuat dari ini, kita akan membuat dari ini.' | Hening | 'Bagi yang kita lihat, kita akan membuat dari ini, kita akan membuat dari ini, kita akan membuat dari ini, kita akan membuat dari ini. Kita akan membuat dari ini, kita akan membuat dari ini, kita akan membuat dari ini.' | FN | 0 | 0 | 1 | 0 |
| 88 | 'Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 89 | 'Nanti kita akan membuat video untuk melihat apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat. Kita akan melihat apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat.' | Hening | 'Nanti kita akan membuat video untuk melihat apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat. Kita akan melihat apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat, apa yang kita akan melihat.' | FN | 0 | 0 | 1 | 0 |
| 90 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 91 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh, Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan.' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh, Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan.' | FN | 0 | 0 | 1 | 0 |
| 92 | 'Dari penggunaan, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris,' | Hening | 'Dari penggunaan, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris, menggunakan bahasa Inggris,' | FN | 0 | 0 | 1 | 0 |
| 93 | 'Pertahankan kata-kata, machine learning, deep learning, data, data, data, data, and base learning. Pertahankan kata-kata, machine learning, deep learning, data, data, data, data, and base learning. Pertahankan kata-kata, machine learning, data, data, data, and base learning. Pertahankan kata-kata, machine learning, data, data, data, and base learning.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 94 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 95 | 'Pertahankan kata-kata ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | Hening | 'Pertahankan kata-kata ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | FN | 0 | 0 | 1 | 0 |
| 96 | 'Pertahankan kata-kata ini menggunakan bahasa Inggris. Pertahankan kata-kata ini menggunakan bahasa Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 97 | 'Pertahankan kata-kata, Terima kasih kerana menonton.' | Hening | 'Pertahankan kata-kata, Terima kasih kerana menonton.' | FN | 0 | 0 | 1 | 0 |
| 98 | 'Pertahankan kata-kata, Terima kasih kerana menonton.' | Hening | 'Pertahankan kata-kata, Terima kasih kerana menonton.' | FN | 0 | 0 | 1 | 0 |
| 99 | 'Pertahankan kata-kata, Jangan lupa, jangan lupa, jangan lupa, jangan lupa...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 100 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 101 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 102 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 103 | 'Pertahankan kata-kata,' | Hening | 'Pertahankan kata-kata,' | FN | 0 | 0 | 1 | 0 |
| 104 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 105 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan,' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan,' | FN | 0 | 0 | 1 | 0 |
| 106 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh,' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh,' | FN | 0 | 0 | 1 | 0 |
| 107 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 108 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh,' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh,' | FN | 0 | 0 | 1 | 0 |
| 109 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan,' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan,' | FN | 0 | 0 | 1 | 0 |
| 110 | 'I'm not sure what to do. I'm not sure what to do. I'm not sure. I'm not sure. I'm not sure. I'm not sure. I'm not sure. I'm not sure. I'm not sure. I'm not sure. I'm not sure. I'm not sure. I'm not sure. I'm not sure.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 111 | 'Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertah' | Hening | 'Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata, Pertah' | FN | 0 | 0 | 1 | 0 |
| 112 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 113 | 'Dari kita, kita akan menggunakan bahasa Inggris. Kami akan menggunakan bahasa Inggris. Kami akan menggunakan bahasa Inggris. Kami akan menggunakan bahasa Inggris. Kami akan menggunakan bahasa Inggris. Kami akan menggunakan bahasa Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 114 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh-kata Inggris apa adanya, jangan diterjemahkan.' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh-kata Inggris apa adanya, jangan diterjemahkan.' | FN | 0 | 0 | 1 | 0 |
| 115 | 'Kami akan menggunakan bahasa Indonesia yang menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris. Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh, ini adalah kata-kata yang menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris. Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 116 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 117 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh-kata Inggris apa adanya, jangan diterjemahkan.' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh-kata Inggris apa adanya, jangan diterjemahkan.' | FN | 0 | 0 | 1 | 0 |
| 118 | *(Hening Sempurna)* | Hening | *(Kosong)* | TN | 0 | 0 | 0 | 1 |
| | **Percobaan 4 (File: Hallufilter_9.txt)** | | | | | | | |
| 119 | 'Pertahankan kata-kata,' | Hening | 'Pertahankan kata-kata,' | FN | 0 | 0 | 1 | 0 |
| 120 | 'I'm just going to say that I'm not a machine learning, I'm just going to say that I'm a machine learning. I'm just going to say that I'm a machine learning. I'm just going to say that I'm a machine learning. I'm just going to say that I'm a machine learning.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 121 | 'I don't know what you're talking about. I don't know what you're talking about. I don't know what you're talking about. I'm not sure what you're talking about. I don't know what you're talking about. I don't know what you're talking about. I don't know what you're talking about. I don't know what you're talking about.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 122 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 123 | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan. Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 124 | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan. Contoh. Pertahankan kata-kata menggunakan bahasa Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 125 | 'Kami berhenti menggunakan bahasa Inggris, yang menggunakan bahasa Inggris, yang menggunakan bahasa Inggris. Kami menggunakan bahasa Inggris, yang menggunakan bahasa Inggris, yang menggunakan bahasa Inggris.' | Hening | 'Kami berhenti menggunakan bahasa Inggris, yang menggunakan bahasa Inggris, yang menggunakan bahasa Inggris. Kami menggunakan bahasa Inggris, yang menggunakan bahasa Inggris, yang menggunakan bahasa Inggris.' | FN | 0 | 0 | 1 | 0 |
| 126 | 'Kami berhenti menggunakan bahasa Inggris, yang menggunakan bahasa Inggris, yang menggunakan bahasa Inggris. Kami menggunakan bahasa Inggris, yang menggunakan bahasa Inggris, yang menggunakan bahasa Inggris.' | Hening | 'Kami berhenti menggunakan bahasa Inggris, yang menggunakan bahasa Inggris, yang menggunakan bahasa Inggris. Kami menggunakan bahasa Inggris, yang menggunakan bahasa Inggris, yang menggunakan bahasa Inggris.' | FN | 0 | 0 | 1 | 0 |
| 127 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 128 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 129 | *(Hening Sempurna)* | Hening | *(Kosong)* | TN | 0 | 0 | 0 | 327 |
| | **Percobaan 5 (File: Hallufilter_10.txt)** | | | | | | | |
| 130 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 131 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 132 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 133 | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan.' | Hening | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan.' | FN | 0 | 0 | 1 | 0 |
| 134 | 'Pertahankan kata-kata inggris.' | Hening | 'Pertahankan kata-kata inggris.' | FN | 0 | 0 | 1 | 0 |
| 135 | 'Pertahankan kata-kata inggris apa adanya.' | Hening | 'Pertahankan kata-kata inggris apa adanya.' | FN | 0 | 0 | 1 | 0 |
| 136 | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan.' | Hening | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan.' | FN | 0 | 0 | 1 | 0 |
| 137 | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan. Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 138 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh-kata Inggris apa adanya, jangan diterjemahkan.' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan. Contoh-kata Inggris apa adanya, jangan diterjemahkan.' | FN | 0 | 0 | 1 | 0 |
| 139 | 'Pertahankan kata-kata ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris. Pertahankan kata-kata ini menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 140 | 'Nanti kita akan menghubungkan bahasa Indonesia yang menggunakan bahasa Indonesia. Kami akan membuatkan uang. Jangan diterjemahkan, kita akan membuatkan uang. Jangan diterjemahkan, kita akan membuatkan uang.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 141 | 'Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata. Pertahankan kata-kata, Pertahankan kata-kata, Pertahankan kata-kata. Pertahankan kata-kata, Pertahankan kata-kata. Pertahankan kata-kata, Pertahankan kata-kata. Pertahankan kata-kata, Pertahankan kata-kata.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 142 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 143 | 'Pertahankan kata-kata,' | Hening | 'Pertahankan kata-kata,' | FN | 0 | 0 | 1 | 0 |
| 144 | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan,' | Hening | 'Pertahankan kata-kata Inggris apa adanya, jangan diterjemahkan,' | FN | 0 | 0 | 1 | 0 |
| 145 | 'Pertahankan kata-kata Inggris. Pertahankan kata-kata Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 146 | 'Pertahankan kata-kata Inggris. Pertahankan kata-kata Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 147 | 'Kami akan menggunakan bahasa Inggris, Kami akan menggunakan bahasa Inggris. Kami akan menggunakan bahasa Inggris. Kami akan menggunakan bahasa Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 148 | 'Kami akan menggunakan bahasa Inggris, Kami akan menggunakan bahasa Inggris. Kami akan menggunakan bahasa Inggris. Kami akan menggunakan bahasa Inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 149 | *(Hening Sempurna)* | Hening | *(Kosong)* | TN | 0 | 0 | 0 | 318 |
| | **TOTAL REKAPITULASI** | | | | **59** | **0** | **85** | **760** |

**Metrik Performa Noise:**
- **Accuracy** = 90.60%
- **Precision** = 100.00%
- **Recall** = 40.97%
- **F1-Score** = 58.13%

---

### Tabel 4.3 Hasil Pengujian Hallucination Filter pada Kondisi Percakapan

| No | Output Whisper | Ground Truth | Output Hallucination Filter | Kategori | TP | FP | FN | TN |
|----|----------------|--------------|-----------------------------|----------|----|----|----|----|
| | **Percobaan 1 (File: Hallufilter_11.txt)** | | | | | | | |
| 1 | 'goodbye' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 2 | 'thank you' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 3 | 'okay' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 4 | 'Terus sekali, tidak mengganggu.' | Hening | 'Terus sekali, tidak mengganggu.' | FN | 0 | 0 | 1 | 0 |
| 5 | 'Jangan terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terl' | Hening | 'Jangan terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terlalu terl' | FN | 0 | 0 | 1 | 0 |
| 6 | 'Music is stress. Masa.' | Hening | 'Music is stress. Masa.' | FN | 0 | 0 | 1 | 0 |
| 7 | 'yes' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 8 | 'Terus di-stress. Masa? Iya, berantah bersama kami di sini, stress.' | Hening | 'Terus di-stress. Masa? Iya, berantah bersama kami di sini, stress.' | FN | 0 | 0 | 1 | 0 |
| 9 | 'Masa? Iya, berhantar bersama-sama di sini, stres ya.' | Hening | 'Masa? Iya, berhantar bersama-sama di sini, stres ya.' | FN | 0 | 0 | 1 | 0 |
| 10 | 'no' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 11 | 'Terus di-stress ya, masa? Iya, berantem sama kamu disini, stress aja. Saya ya, jadi prioritasnya...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 12 | 'Jangan lupa, jangan lupa, jangan lupa. Jangan lupa. Jangan lupa. Jangan lupa. Jangan lupa. Jangan lupa. Jangan lupa. Jangan lupa. Jangan lupa. Jangan lupa. Jangan lupa. Jangan lupa. Jangan lupa. Jangan lupa.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 13 | 'Maksud saya, saya ya, tapi prioritasnya itu. Apa ya? Emang kita kalau misalkan ini, itu paling susah demi.' | Hening | 'Maksud saya, saya ya, tapi prioritasnya itu. Apa ya? Emang kita kalau misalkan ini, itu paling susah demi.' | FN | 0 | 0 | 1 | 0 |
| 14 | 'Maksudnya, kalau kita berhati-hati dengan makament di sini, stres saja. Saya ya, tapi prioritasnya, gitu. Apa ya? Emang kita kalau misalkan dia, itu paling susah di sini. Ini selalu ada, ada aja.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 15 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 16 | 'Ini, Taiwan, terus ikut kembali melawan Aki Jali.' | Hening | 'Ini, Taiwan, terus ikut kembali melawan Aki Jali.' | FN | 0 | 0 | 1 | 0 |
| 17 | 'Dan ini kawan atau seingin pun, ketadi, pengelawan lagi jali.' | Hening | 'Dan ini kawan atau seingin pun, ketadi, pengelawan lagi jali.' | FN | 0 | 0 | 1 | 0 |
| 18 | 'Terima kasih. Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 19 | 'I want to include, atas, I want to introduce, yes, yes, yes, yes.' | Hening | 'I want to include, atas, I want to introduce, yes, yes, yes, yes.' | FN | 0 | 0 | 1 | 0 |
| 20 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 21 | 'Ini, kawan atau seingkun ketadi melawan lagi jali. Ya, jadi bahap, peringat-ingat saya benar-benar kata-kata.' | Hening | 'Ini, kawan atau seingkun ketadi melawan lagi jali. Ya, jadi bahap, peringat-ingat saya benar-benar kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 22 | 'Ini, Taiwan, terus inggris, ke tadi, melawan, lagi jali. Ya, ini bahasa Indonesia yang benar-benar kata-kata.' | Hening | 'Ini, Taiwan, terus inggris, ke tadi, melawan, lagi jali. Ya, ini bahasa Indonesia yang benar-benar kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 23 | 'Mereka menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | Hening | 'Mereka menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | FN | 0 | 0 | 1 | 0 |
| 24 | 'Semua, ini, Taiwan, atau seingkun, ketadi, melawan, lagi jali, ya. Ya, ini buffer, yang sama banyak kata-kata. Mordy ke tax dikit, langsung buffer, ya. Mana sih?' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 25 | 'Semuanya, ya, ya, ya, ya. Semuanya, ya, ya, ya, ya. Ya, ya, ya, ya. Ya, ya, ya. Ya, ya. Ya, ya, ya. Ya, ya, ya. Ya, ya. Ya, ya. Ya, ya. Ya, ya. Ya, ya. Ya, ya. Ya, ya.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 26 | 'Mereka menggunakan bahasa Inggris, ya, ya.' | Hening | 'Mereka menggunakan bahasa Inggris, ya, ya.' | FN | 0 | 0 | 1 | 0 |
| 27 | 'Bukankah kamu, Timmy? Kehwan, terus ngumpul, tetanik, melawan, lagi jali. Ya, dia baper ya, nggak sama banyak kata-kata. Mordi ke tax dikir, langsung baper ya. Mana sih? Dimana mau ini, ya? Nah, saya, gitu, tahu nggak? Pas sangat.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 28 | 'Mereka menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | Hening | 'Mereka menggunakan bahasa Indonesia yang dicampur istilah teknis berbahasa Inggris.' | FN | 0 | 0 | 1 | 0 |
| 29 | 'Mereka menggunakan bahasa Inggris.' | Hening | 'Mereka menggunakan bahasa Inggris.' | FN | 0 | 0 | 1 | 0 |
| 30 | 'Ini, kawan atau seumpun ketadi melawan lagi jali. Ya, ini buffer, ya, saya banyak kata-kata. Mordi ke taxidiki langsung buffer ya. Mana sih? Bagaimana mau ini? Maksudnya saya gitu tau nggak pasangan tau. Ya, jangan, saya udah menang.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 31 | 'Ini juga asiskan terlalu, terlalu, bye.' | Hening | 'Ini juga asiskan terlalu, terlalu, bye.' | FN | 0 | 0 | 1 | 0 |
| 32 | 'Terima kasih, saya juga, saya akan terlalu, terlalu baik. Sebelah lalu sebar, ya, kegerakau? Gara-gara kamu juga. Gara-gara kau lah.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 33 | 'Ini juga, saya akan terlalu baik. Semilal-lalu sebar deh, ya, karena kamu? Eh, karena kamu juga. Eh, karena kamu lah. Oh, dulu, maaf, kamu susahin saya juga tau. Sekarang bagus, ya?' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 34 | 'Ini juga, saya sekian terlalu baik. Semilal lalu sebar ya, kegaraku? Gara-gara kamu juga. Gara-gara kau lah, kamu lah. Oh, dulu, kalau lalu kamu susahin saya juga tau. Sekarang bagus kan? Sekarang kamu minta. Bagus kan?' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 35 | 'Ini juga, ya, sih. Ini terlalu baik. Semilal lusbar ya, kegara kau? Eh, kegara-gara kamu juga. Eh, karena kau lah, ya kamu lah. Oh, dulu, kalau lah, kamu susahin saya juga tau. Sekarang bagus kan? Sekarang kamu minta. Bagus kan? Ya, minta.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 36 | 'Ini juga istirahat. Terlalu baik. Sembilan lalu sebar ya, kegara kamu? Gara-gara kamu juga. Gara kamu lah, ya kamu lah. Oh dulu, maaf lah, kamu susahin saya juga tau. Bagus kan? Sekarang kamu minta. Bagus kan? Ya minta, apa ya? Dah tau dia, ya sama.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 37 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 38 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 39 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 40 | 'Dua tahun ini. Dua em. Iya. Kenapa kamu harus nge-info daripada orangku tinggal faiz sama selanjutnya?' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 41 | 'Dua tahun ini. Dua tahun ini. Kenapa kamu harus mengingatkan follower di orangku tinggal faiz sama selanjutnya?' | Hening | 'Dua tahun ini. Dua tahun ini. Kenapa kamu harus mengingatkan follower di orangku tinggal faiz sama selanjutnya?' | FN | 0 | 0 | 1 | 0 |
| 42 | 'Dua tahun ini. Dua em. Iya. Kenapa kamu harus nge-info daripada orang kok tinggal faiz sama selanjutnya naik?' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 43 | 'Dua tahun ini. Dua em. Iya. Kenapa kamu harus nge-info daripada orang? Kok tinggal faiz sama selanjutnya naik? Hei!' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 44 | 'Dua tahun ini. Dua tahun ini. Kenapa kamu harus naik informasi dari orangku tinggal faiz sama selanjutnya? Hei! Hei!' | Hening | 'Dua tahun ini. Dua tahun ini. Kenapa kamu harus naik informasi dari orangku tinggal faiz sama selanjutnya? Hei! Hei!' | FN | 0 | 0 | 1 | 0 |
| 45 | 'Dua tahun. Dua em. Dua em. Dua. Kenapa kamu harus nge-info daripada orang kok tinggal faiz sama selanjutnya? Hei! Hei! Tak mau tanpa. Sakit apa?' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 46 | 'Dua tahun ini. Dua tahun ini. Kenapa kamu harus menggabungi orang-orang kok tinggal faiz sama selanjutnya? Hei! Hei! Sakit apa? Sakit apa?' | Hening | 'Dua tahun ini. Dua tahun ini. Kenapa kamu harus menggabungi orang-orang kok tinggal faiz sama selanjutnya? Hei! Hei! Sakit apa? Sakit apa?' | FN | 0 | 0 | 1 | 0 |
| 47 | 'Dua tahun ini. Dua em. Iya. Kenapa kamu harus naikin follow-up dari orangku tinggal faiz sama selanjutnya naik? Hei! Hei! Tak mau tanpa. Sakit naopa, sakit naopa! Jadi ada pelot, pis ini kayak...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 48 | 'Dua tahun ini. Dua em. Kenapa kamu harus menggunakan follower di orangku tinggal faiz sama selanjutnya? Hei! Hei! Sakit apa? Sakit apa? Jadi ada pelot, tapi ini kayak film. Masihnya?' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 49 | 'Pertahankan kata-kata ini menggunakan bahasa Inggris. Pertahankan kata-kata ini menggunakan' | Hening | 'Pertahankan kata-kata ini menggunakan bahasa Inggris. Pertahankan kata-kata ini menggunakan' | FN | 0 | 0 | 1 | 0 |
| 50 | 'Thank you.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 51 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 52 | 'Tidak lalu.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 53 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 54 | 'Yang mangg, aku bukan subut, tapi okay subut saya.' | Hening | 'Yang mangg, aku bukan subut, tapi okay subut saya.' | FN | 0 | 0 | 1 | 0 |
| 55 | 'Emang aku bukan subut tapi aku kesubut saya.' | Hening | 'Emang aku bukan subut tapi aku kesubut saya.' | FN | 0 | 0 | 1 | 0 |
| 56 | 'Emang aku bukan sebut tapi okey sebut saya.' | Hening | 'Emang aku bukan sebut tapi okey sebut saya.' | FN | 0 | 0 | 1 | 0 |
| 57 | 'Emang, aku bukan sebut, tapi okay sebut saya.' | Hening | 'Emang, aku bukan sebut, tapi okay sebut saya.' | FN | 0 | 0 | 1 | 0 |
| 58 | 'Emang, aku bukan sebut tapi okey sebut saya, siapa yang bahas okey sebut kau dan Tina?' | Hening | 'Emang, aku bukan sebut tapi okey sebut saya, siapa yang bahas okey sebut kau dan Tina?' | FN | 0 | 0 | 1 | 0 |
| 59 | 'Emang, aku bukan sebut tapi okey sebut saya. Siapa yang bahas okey sebut kau dan tidak? Makanya saya bilang...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 60 | 'Emang, aku bukan sebut, tapi okey sebut saya. Siapa yang bahas okey sebut kau dan tidak? Makanya saya bilang, saya kan bahas sih, kenapa?' | Hening | 'Emang, aku bukan sebut, tapi okey sebut saya. Siapa yang bahas okey sebut kau dan tidak? Makanya saya bilang, saya kan bahas sih, kenapa?' | FN | 0 | 0 | 1 | 0 |
| 61 | 'Emang, aku bukan sebut, tapi okay sebut saya. Siapa yang mengubahkan okay sebut kau dan tidak? Makanya saya bilang, saya kan mengubahkan, kenapa kau pilih okay?' | Hening | 'Emang, aku bukan sebut, tapi okay sebut saya. Siapa yang mengubahkan okay sebut kau dan tidak? Makanya saya bilang, saya kan mengubahkan, kenapa kau pilih okay?' | FN | 0 | 0 | 1 | 0 |
| 62 | 'Emang, aku bukan sebut, tapi okay sebut saya. Siapa yang menguas okay sebut kau dan tidak? Makanya saya bilang, saya kan masih kenapa tau pilih okay dalam moment boxy.' | Hening | 'Emang, aku bukan sebut, tapi okay sebut saya. Siapa yang menguas okay sebut kau dan tidak? Makanya saya bilang, saya kan masih kenapa tau pilih okay dalam moment boxy.' | FN | 0 | 0 | 1 | 0 |
| 63 | 'Emang, aku bukan sebut tapi okay sebut saya. Siapa yang mas okay sebut kau dan tidak? Makanya saya bilang, saya kan masih kenapa tau pilih okay. Ini, sekarang, itu karena...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 64 | 'Emang, aku bukan sebut tapi Ongkir sebut saya, siapa yang menguas Ongkir sebut kau dan tidak? Makanya saya bilang, saya kan masih kenapa tau pilih Ongkir di moment boxy, itu kan saja, gimana kalau Ongkir boxy saya mau itu?' | Hening | 'Emang, aku bukan sebut tapi Ongkir sebut saya, siapa yang menguas Ongkir sebut kau dan tidak? Makanya saya bilang, saya kan masih kenapa tau pilih Ongkir di moment boxy, itu kan saja, gimana kalau Ongkir boxy saya mau itu?' | FN | 0 | 0 | 1 | 0 |
| 65 | 'Emang, aku bukan sebut tapi Ongkir sebut saya, siapa yang menguas Ongkir sebut kau dan tidak? Makanya saya bilang, saya kan masih kenapa tau pilih Ongkir di moment boxy, itu kan saja, gimana kalau Ongkir boxy saya mau itai.' | Hening | 'Emang, aku bukan sebut tapi Ongkir sebut saya, siapa yang menguas Ongkir sebut kau dan tidak? Makanya saya bilang, saya kan masih kenapa tau pilih Ongkir di moment boxy, itu kan saja, gimana kalau Ongkir boxy saya mau itai.' | FN | 0 | 0 | 1 | 0 |
| 66 | 'Emang, aku bukan sebut tapi okey sebut saya, siapa yang menguas okey sebut kau dan tidak, makanya saya bilang, saya kan masyik, kenapa kau pilih okey? Ini, sekarang, itu kan saja, gimana kalau okey moksik saya mau itu? Ya, nggak bisa.' | Hening | 'Emang, aku bukan sebut tapi okey sebut saya, siapa yang menguas okey sebut kau dan tidak, makanya saya bilang, saya kan masyik, kenapa kau pilih okey? Ini, sekarang, itu kan saja, gimana kalau okey moksik saya mau itu? Ya, nggak bisa.' | FN | 0 | 0 | 1 | 0 |
| 67 | 'Emang, aku bukan sebut, tapi Ongkai sebut saya. Siapa yang menguas Ongkai sebut kau dan tidak? Makanya saya bilang kalau... Saya kan menguas Ongkai, kenapa kau pilih Ongkai? Ini... Sekarang... Itu kan saja, gimana kalau Ongkai Ongkai Ongkai Ongkai Ongkai Ongkai? Nah, nggak bisa. Iya, Ongkai Ongkai Ongkai, tidak apa.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 68 | 'Bukti ini kan sudah bisa apa-apa, akhirnya saya sudah keram, gue ngerti nggak.' | Hening | 'Bukti ini kan sudah bisa apa-apa, akhirnya saya sudah keram, gue ngerti nggak.' | FN | 0 | 0 | 1 | 0 |
| 69 | *(Hening Sempurna)* | Hening | *(Kosong)* | TN | 0 | 0 | 0 | 31 |
| | **Percobaan 2 (File: Hallufilter_12.txt)** | | | | | | | |
| 70 | 'Bukti ini kan sudah bisa apa-apa, akhirnya saya sudah keram, gue ngerti nggak.' | Hening | 'Bukti ini kan sudah bisa apa-apa, akhirnya saya sudah keram, gue ngerti nggak.' | FN | 0 | 0 | 1 | 0 |
| 71 | 'Bukti, kok sudah bisa apa-apa kok akhirnya, saya sudah keram, kok ngerti nggak? Udah lepid, ya pernah.' | Hening | 'Bukti, kok sudah bisa apa-apa kok akhirnya, saya sudah keram, kok ngerti nggak? Udah lepid, ya pernah.' | FN | 0 | 0 | 1 | 0 |
| 72 | 'Buksi ini kan sudah bisa apa-apa, akhirnya saya sudah kram, gue ngerti nggak, sudah lepid, nggak pernah kram saya.' | Hening | 'Buksi ini kan sudah bisa apa-apa, akhirnya saya sudah kram, gue ngerti nggak, sudah lepid, nggak pernah kram saya.' | FN | 0 | 0 | 1 | 0 |
| 73 | 'goodbye' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 74 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 75 | 'Pertahankan kata-kata,' | Hening | 'Pertahankan kata-kata,' | FN | 0 | 0 | 1 | 0 |
| 76 | 'Nah, nah, nah, nah. Salam!' | Hening | 'Nah, nah, nah, nah. Salam!' | FN | 0 | 0 | 1 | 0 |
| 77 | 'thank you' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 78 | 'okay' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 79 | 'yes' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 80 | 'Terima kasih kerana menonton.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 81 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 82 | 'Hei, maaf, maaf. Salam, salam ini, salam hari. Awas ya, bukan. bilang itu bukan kelas saya' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 83 | 'Eh, maaf, maaf. Salam, salam hari, salam hari. Awas ya, bukan. Bila, itu bukan kelas saya.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 84 | 'Hei, maaf, maaf. Salam, apa? Salam, disalamari. Apa sih? Bukan. Mereka bilang, itu bukan kelas saya, kelas saya 60.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 85 | 'Eh, salah apa? Salam, disalam hari. Awas ya, bukannya. Belum, itu bukan kelas saya. Kelas saya 60, 57. Emang ada yang berani dalam saya 57 kau.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 86 | 'So, no, I don't respect the class at all.' | Hening | 'So, no, I don't respect the class at all.' | FN | 0 | 0 | 1 | 0 |
| 87 | 'Kamu ada risiko, lah, segalanya. Saya juga nggak lakiin mopi aja, saya, saya diwarung terus, ya.' | Hening | 'Kamu ada risiko, lah, segalanya. Saya juga nggak lakiin mopi aja, saya, saya diwarung terus, ya.' | FN | 0 | 0 | 1 | 0 |
| 88 | 'Semua ada rispe kelahan segala, tahu. Saya juga nggak lakiin mopi aja, saya. Saya diwarung terus, ya.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 89 | 'Semua ada risiko lah segala itu. Saya juga nggak lakin, mau biar aja saya. Saya di luar tentu-tutup saya.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 90 | 'Semua ada respect-less yang mengawal. Saya juga nggak lakuin waktunya saja, saya di luar berkura. Saya di luar terkaji.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 91 | 'Semua hadirisbek lah, semua orang, saya juga nggak lakiin movie aja saya, saya di luar keurusnya.' | Hening | 'Semua hadirisbek lah, semua orang, saya juga nggak lakiin movie aja saya, saya di luar keurusnya.' | FN | 0 | 0 | 1 | 0 |
| 92 | 'Semua hadirisbe kelas semua orang, saya juga nggak lakiin mopi aja saya, saya di luar keurusnya. Jadi, power technology diberikan, beneran sekejang atau operator gitu? Nggak biasa, I guess.' | Hening | 'Semua hadirisbe kelas semua orang, saya juga nggak lakiin mopi aja saya, saya di luar keurusnya. Jadi, power technology diberikan, beneran sekejang atau operator gitu? Nggak biasa, I guess.' | FN | 0 | 0 | 1 | 0 |
| 93 | 'Kamu ada rispe kelahan semua orang, saya juga nggak lakiin mopi aja saya, saya di luar keurusnya. Jadi, power technology diperkenalkan, beneran sekejang atau pertengungan? Nggak biasa, I guess. Besan.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 94 | 'Semua hadirisbek lah segala orang, saya juga nggak lakiin mopi aja saya, saya di luar keurusnya. Sari, power technology, ibu, benar-benar kejang atau friend? Enggak biasa, I guess. Besarnya kesadu? Besarnya, besarnya.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 95 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 96 | 'Terima kasih. Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 97 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 98 | 'Bersenang, apa yang terjadi, reda-reda, gaks.' | Hening | 'Bersenang, apa yang terjadi, reda-reda, gaks.' | FN | 0 | 0 | 1 | 0 |
| 99 | 'Bersenang, bahasa Indonesia tidak tahu ga. Mungkin bisa, itu sorok-sengotik.' | Hening | 'Bersenang, bahasa Indonesia tidak tahu ga. Mungkin bisa, itu sorok-sengotik.' | FN | 0 | 0 | 1 | 0 |
| 100 | 'Pertahankan kata-kata,' | Hening | 'Pertahankan kata-kata,' | FN | 0 | 0 | 1 | 0 |
| 101 | 'Bersama saya, apa yang saya tahu, bisa, ya? Surupnya 2 dekate.' | Hening | 'Bersama saya, apa yang saya tahu, bisa, ya? Surupnya 2 dekate.' | FN | 0 | 0 | 1 | 0 |
| 102 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 103 | 'Bersenjata, apa? Saya tidak tahu, gaks. Bukit bisa, saya sudah pasang dua dekade. Saya sudah pasang dua dekade. Bersenjata. Sama mobil, drablok, saya sudah.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 104 | 'Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan. Pertahankan kata-kata inggris apa adanya, jangan diterjemahkan.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 105 | 'Bisa-bisa, apa? Saya tidak tahu. Mungkin sebabnya. Surupusnya nge-dek aja. Akan, saya melakukan. Sama mobil, drablok, sebuah food. Buat food. Aku makan. Ya, mau. Kami minta kamu.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 106 | 'Pertahankan kata-kata inggris. Pertahankan kata-kata inggris.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 107 | 'Okay.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 108 | 'Thank you very much.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 109 | *(Hening Sempurna)* | Hening | *(Kosong)* | TN | 0 | 0 | 0 | 4 |
| | **Percobaan 3 (File: Hallufilter_13.txt)** | | | | | | | |
| 110 | 'goodbye' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 111 | 'Ya, fighter yang pinta.' | Hening | 'Ya, fighter yang pinta.' | FN | 0 | 0 | 1 | 0 |
| 112 | 'Ya, paker yang pintar.' | Hening | 'Ya, paker yang pintar.' | FN | 0 | 0 | 1 | 0 |
| 113 | 'Dia paker yang pinta, yang bagus, ya.' | Hening | 'Dia paker yang pinta, yang bagus, ya.' | FN | 0 | 0 | 1 | 0 |
| 114 | 'Dia paker yang pinta, yang bagus, jadi dia tahu.' | Hening | 'Dia paker yang pinta, yang bagus, jadi dia tahu.' | FN | 0 | 0 | 1 | 0 |
| 115 | 'Dia fighter yang pinta, yang bagus, jadi dia tahu timingnya.' | Hening | 'Dia fighter yang pinta, yang bagus, jadi dia tahu timingnya.' | FN | 0 | 0 | 1 | 0 |
| 116 | 'Dia paker yang pinter, yang bagus, jadi dia tahu timingnya.' | Hening | 'Dia paker yang pinter, yang bagus, jadi dia tahu timingnya.' | FN | 0 | 0 | 1 | 0 |
| 117 | 'Dia paker yang pinter, yang bagus, jadi dia tahu timingnya menggelang itu.' | Hening | 'Dia paker yang pinter, yang bagus, jadi dia tahu timingnya menggelang itu.' | FN | 0 | 0 | 1 | 0 |
| 118 | 'Dia paker yang pinter, yang bagus, jadi dia tahu timingnya menghilangnya cepat.' | Hening | 'Dia paker yang pinter, yang bagus, jadi dia tahu timingnya menghilangnya cepat.' | FN | 0 | 0 | 1 | 0 |
| 119 | 'Dia paker yang pinter, yang bagus, jadi dia tahu timingnya, menghilangnya cepat, larinya kabungnya cepat.' | Hening | 'Dia paker yang pinter, yang bagus, jadi dia tahu timingnya, menghilangnya cepat, larinya kabungnya cepat.' | FN | 0 | 0 | 1 | 0 |
| 120 | 'Dia paker yang pinter, yang bagus, jadi dia tahu timingnya, menghilangnya cepat, larinya kabungnya cepat, kok tidak putus.' | Hening | 'Dia paker yang pinter, yang bagus, jadi dia tahu timingnya, menghilangnya cepat, larinya kabungnya cepat, kok tidak putus.' | FN | 0 | 0 | 1 | 0 |
| 121 | 'Dia paker yang pinter, yang bagus, jadi dia tahu timingnya, menghilangnya cepat, larinya kabungnya cepat, maka tidak putus.' | Hening | 'Dia paker yang pinter, yang bagus, jadi dia tahu timingnya, menghilangnya cepat, larinya kabungnya cepat, maka tidak putus.' | FN | 0 | 0 | 1 | 0 |
| 122 | 'Dia paker yang pinter, yang bagus, jadi dia tahu timingnya, menghilangnya cepat, larinya kabungnya cepat, waktu tidak putus.' | Hening | 'Dia paker yang pinter, yang bagus, jadi dia tahu timingnya, menghilangnya cepat, larinya kabungnya cepat, waktu tidak putus.' | FN | 0 | 0 | 1 | 0 |
| 123 | 'Dia paker yang pinter, yang bagus, jadi dia tahu timingnya, menghilangnya cepat, larinya kabungnya cepat, waktu itu dia putus, jadi, ya kita tahu lah dia.' | Hening | 'Dia paker yang pinter, yang bagus, jadi dia tahu timingnya, menghilangnya cepat, larinya kabungnya cepat, waktu itu dia putus, jadi, ya kita tahu lah dia.' | FN | 0 | 0 | 1 | 0 |
| 124 | 'Dia paker yang pinter, yang bagus, jadi dia tahu timingnya, menghilangnya cepat, larinya kabungnya cepat, waktu itu dia putus, jadi kita tahu lah dia paker yang cepat.' | Hening | 'Dia paker yang pinter, yang bagus, jadi dia tahu timingnya, menghilangnya cepat, larinya kabungnya cepat, waktu itu dia putus, jadi kita tahu lah dia paker yang cepat.' | FN | 0 | 0 | 1 | 0 |
| 125 | 'Dia paker yang pintar, yang bagus, jadi dia tahu timingnya, menghilangnya cepat, larinya kabungnya cepat, waktu itu dia putus. Jadi, ya kita tahu lah, dia paker yang cepat, jadi timing.' | Hening | 'Dia paker yang pintar, yang bagus, jadi dia tahu timingnya, menghilangnya cepat, larinya kabungnya cepat, waktu itu dia putus. Jadi, ya kita tahu lah, dia paker yang cepat, jadi timing.' | FN | 0 | 0 | 1 | 0 |
| 126 | 'Dia paker yang pintar, yang bagus, jadi dia tahu timingnya, menghilangnya cepat, larinya kabungnya cepat, waktu tidak putus. Jadi, ya kita tahu lah, dia paker yang cepat, jadi, timing yang power yang benar-benar.' | Hening | 'Dia paker yang pintar, yang bagus, jadi dia tahu timingnya, menghilangnya cepat, larinya kabungnya cepat, waktu tidak putus. Jadi, ya kita tahu lah, dia paker yang cepat, jadi, timing yang power yang benar-benar.' | FN | 0 | 0 | 1 | 0 |
| 127 | 'Dia paker yang pintar, yang bagus, jadi dia tahu timingnya, menghilangnya cepat, larinya kabungnya cepat, waktu tidak putus. Jadi, ya kita tahu lah dia paker yang cepat, jadi, timing yang power yang benar-benar masa gitu.' | Hening | 'Dia paker yang pintar, yang bagus, jadi dia tahu timingnya, menghilangnya cepat, larinya kabungnya cepat, waktu tidak putus. Jadi, ya kita tahu lah dia paker yang cepat, jadi, timing yang power yang benar-benar masa gitu.' | FN | 0 | 0 | 1 | 0 |
| 128 | 'thank you' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 129 | 'okay' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 130 | 'yes' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 131 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 132 | 'Oh, wow. Tuh, terima kasih. Lagi asisten, jadi kalau kaji mau ambil sapuknya, silahkan. Tapi datang ke rumah saya, berantam di rumah.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 133 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 134 | 'Yes.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 135 | 'Yes.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 136 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 137 | 'Satu.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 138 | 'Satya!' | Hening | 'Satya!' | FN | 0 | 0 | 1 | 0 |
| 139 | 'Satya. Dari.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 140 | 'Satya, daripada...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 141 | 'Satia dari para...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 142 | 'Setia dari para...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 143 | 'Satia dari para naras.' | Hening | 'Satia dari para naras.' | FN | 0 | 0 | 1 | 0 |
| 144 | 'Satia dari para haras.' | Hening | 'Satia dari para haras.' | FN | 0 | 0 | 1 | 0 |
| 145 | 'Satia dari para ngeras, teriakupah.' | Hening | 'Satia dari para ngeras, teriakupah.' | FN | 0 | 0 | 1 | 0 |
| 146 | 'Satia dari para ngeras dari aku pah.' | Hening | 'Satia dari para ngeras dari aku pah.' | FN | 0 | 0 | 1 | 0 |
| 147 | 'Satya, dari para naras, teriakupah.' | Hening | 'Satya, dari para naras, teriakupah.' | FN | 0 | 0 | 1 | 0 |
| 148 | 'Satia, dari para hara. Diakupah, ingin ke Inggris.' | Hening | 'Satia, dari para hara. Diakupah, ingin ke Inggris.' | FN | 0 | 0 | 1 | 0 |
| 149 | 'Satya, garipara. Terima kasih. Terima kasih. Inggris apa-apa.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 150 | 'Satya, bari para rasa. Iya, kupa. India, Indonesia, satu kipak, satu kipak.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 151 | 'Satya. Bari barat. Terima kasih. Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 152 | 'Satya. Dari baras. Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 153 | 'Satya, daripada. Terima kasih. Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 154 | 'Satya, daripada. Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 155 | 'Sampia, dari baras.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 156 | 'Sabia, daripada... Diberi aku. Diberi aku, jadi aku yang dicampur. Kata-kata, aku yang diterjemahkan. Kata-kata, aku yang diterjemahkan. Kata-kata, aku yang diterjemahkan. Kata-kata, aku yang diterjemahkan. Kata-kata, aku yang diterjemahkan.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 157 | 'Sabian, dari baras. Terima kasih, aku bakal.' | Hening | 'Sabian, dari baras. Terima kasih, aku bakal.' | FN | 0 | 0 | 1 | 0 |
| 158 | 'Pertahankan kata-kata, stop team alert, what's tonight, top tonight, what's tonight, what's tonight, what's tonight.' | Hening | 'Pertahankan kata-kata, stop team alert, what's tonight, top tonight, what's tonight, what's tonight, what's tonight.' | FN | 0 | 0 | 1 | 0 |
| 159 | 'Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak' | Hening | 'Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak! Tidak' | FN | 0 | 0 | 1 | 0 |
| 160 | 'Pertahankan kata-kata, but it is a safety, a lot, but it is a top, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety' | Hening | 'Pertahankan kata-kata, but it is a safety, a lot, but it is a top, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety, but it is a safety' | FN | 0 | 0 | 1 | 0 |
| 161 | 'Jangan terlalu subarain di nanti ada yang hate.' | Hening | 'Jangan terlalu subarain di nanti ada yang hate.' | FN | 0 | 0 | 1 | 0 |
| 162 | 'Jangan terlalu subar ID, nanti ada yang haji. Okay, aku ngomong-ngomong gua. Terima kasih, bro.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 163 | *(Hening Sempurna)* | Hening | *(Kosong)* | TN | 0 | 0 | 0 | 4 |
| | **Percobaan 4 (File: Hallufilter_14.txt)** | | | | | | | |
| 164 | 'goodbye' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 165 | 'thank you' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 166 | 'Inggris ini, ini, ini, ya.' | Hening | 'Inggris ini, ini, ini, ya.' | FN | 0 | 0 | 1 | 0 |
| 167 | 'Inggris, ini, ini, ya.' | Hening | 'Inggris, ini, ini, ya.' | FN | 0 | 0 | 1 | 0 |
| 168 | 'Inggris, ini, ini, ya, ini.' | Hening | 'Inggris, ini, ini, ya, ini.' | FN | 0 | 0 | 1 | 0 |
| 169 | 'Sini, ini, ya, ini kaca-kaca.' | Hening | 'Sini, ini, ya, ini kaca-kaca.' | FN | 0 | 0 | 1 | 0 |
| 170 | 'Ini, ya, ini tak semua, mau berusia.' | Hening | 'Ini, ya, ini tak semua, mau berusia.' | FN | 0 | 0 | 1 | 0 |
| 171 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 172 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 173 | 'Terima kasih, ini, ini, ya, ini kaca-coba, mau bersih ini, ini, ini, ini, ini.' | Hening | 'Terima kasih, ini, ini, ya, ini kaca-coba, mau bersih ini, ini, ini, ini, ini.' | FN | 0 | 0 | 1 | 0 |
| 174 | 'okay' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 175 | 'yes' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 176 | 'no' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 177 | 'Terimakasih, chef. Sebelumnya.' | Hening | 'Terimakasih, chef. Sebelumnya.' | FN | 0 | 0 | 1 | 0 |
| 178 | 'Terimakasih, chef. Terimakasih.' | Hening | 'Terimakasih, chef. Terimakasih.' | FN | 0 | 0 | 1 | 0 |
| 179 | 'Selamat pagi, chef. Names kap.' | Hening | 'Selamat pagi, chef. Names kap.' | FN | 0 | 0 | 1 | 0 |
| 180 | 'Terima kasih, chef. Names kap. Saya Susia.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 181 | 'Terima kasih, chef. Names kap. Saya susah, chef. Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 182 | 'Selamat pagi, chef. Names kap. Saya susah, chef. Saya asku.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 183 | 'Selamat pagi, chef. Names, Pat. Saya Sushia. Saya Situ. Selamat pagi.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 184 | 'Selamat pagi, chef. Names, Pat. Saya Sushia. Saya Asdu. Fried rice. Wah.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 185 | 'Selamat pagi, chef. Names, pack. Saya Sushia. Saya yang stew. Fried rice. Well, a bit simple, no?' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 186 | 'Selamat pagi, chef. Names, Pat. Saya Sushia. Saya yang sebuah. Selamat pagi. Well, a bit simple, no?' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 187 | 'Selamat pagi, chef. Names, Pat. Saya Sushia. Saya yang sebuah. Selamat pagi. Well, a bit simple, no?' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 188 | 'Selamat pagi, chef. Names, Pat. Saya Sushia. Selamat pagi. Selamat pagi. Well, a bit simple, no?' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 189 | 'Selamat pagi, chef, nama saya Pat. Saya Sushia. Selamat pagi. Selamat pagi. Well, a bit simple, no?' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 190 | 'Pertahankan kata-kata.' | Hening | 'Pertahankan kata-kata.' | FN | 0 | 0 | 1 | 0 |
| 191 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 192 | 'Water.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 193 | 'Waka.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 194 | 'Bisa. Waka.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 195 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 196 | 'Terus, water.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 197 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 198 | 'Pada.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 199 | 'Pada. Pada. Pada. Pada.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 200 | 'Terus, water,' | Hening | 'Terus, water,' | FN | 0 | 0 | 1 | 0 |
| 201 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 202 | 'New call.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 203 | 'You go home.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 204 | 'New call.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 205 | 'You go.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 206 | 'You go home. Yes, chef.' | Hening | 'You go home. Yes, chef.' | FN | 0 | 0 | 1 | 0 |
| 207 | 'New goal. Hei, chef.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 208 | 'You go home. Yes, chef. Yes, chef.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 209 | 'You go home. Yes, sir.' | Hening | 'You go home. Yes, sir.' | FN | 0 | 0 | 1 | 0 |
| 210 | 'You go home. Yes, chef.' | Hening | 'You go home. Yes, chef.' | FN | 0 | 0 | 1 | 0 |
| 211 | 'You go home. Yes sir. Yes sir.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 212 | 'You go home. Yes, chef. Yes, chef. There's no way...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 213 | 'You go home. Yes, chef. Yes, chef. There's no way.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 214 | 'You go home. Yes, chef. Yes, chef. There's no way. This kitchen's fine.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 215 | 'You go home. Yes, chef. Yes, chef. There's no way. This kid chicks fly way better than me.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 216 | 'You go home. Yes, chef. Yes, chef. There's no way. This eight-chicks pie rice is better than mine. I'm a...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 217 | 'You go home. Yes, chef. Yes, chef. There's no way this eight chicks fried rice is better than mine. I'm a graduate. I told you to get...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 218 | 'You go home. Yes, chef. Yes, chef. There's no way this it takes my life's better than mine. I'm a graduate. I told you to get out of here. I won't.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 219 | 'You go home. Yes, chef. Yes, chef. There's no way. This it takes my life's better than mine. I'm a graduate. I told you to get out of here. I won't. I told you to get...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 220 | 'You go home. Yes, chef. Yes, chef. There's no way. This it takes my life's better than mine. I'm a graduate. I told you to get out of here. I won't. I told you to get...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 221 | 'You go home. Yes, chef. Yes, chef. There's no way. This it takes my life's better than mine. I'm a graduate. I told you to get out of here. I won't. I told you to get out of here.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 222 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 223 | 'Tak bisa.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 224 | 'Taknyemar, update.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 225 | 'Tak ada lagi.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 226 | 'Jadi kita bisa mengejutkan.' | Hening | 'Jadi kita bisa mengejutkan.' | FN | 0 | 0 | 1 | 0 |
| 227 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 228 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 229 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 230 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 231 | 'Ya.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 232 | 'Ya, biadu.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 233 | 'Ya, beliau dulu.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 234 | 'Ya, billyado, chakra di...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 235 | 'Diambil yadu chakra dinarut.' | Hening | 'Diambil yadu chakra dinarut.' | FN | 0 | 0 | 1 | 0 |
| 236 | 'Diambil ya dulu.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 237 | 'Diambilnya dulu. Chakra Dina Ruto, bagus.' | Hening | 'Diambilnya dulu. Chakra Dina Ruto, bagus.' | FN | 0 | 0 | 1 | 0 |
| 238 | 'Diambilnya dulu, chakra dina ruto, bagus, key.' | Hening | 'Diambilnya dulu, chakra dina ruto, bagus, key.' | FN | 0 | 0 | 1 | 0 |
| 239 | 'Dia ambilnya dulu, chakra dina ruto, bagus, ki di dragon...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 240 | 'Ya, ambilnya dulu.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 241 | *(Hening Sempurna)* | Hening | *(Kosong)* | TN | 0 | 0 | 0 | 158 |
| | **Percobaan 5 (File: Hallufilter_15.txt)** | | | | | | | |
| 242 | 'goodbye' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 243 | 'thank you' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 244 | 'okay' | Hening | 'Dihapus (Kosong)' | FP | 0 | 1 | 0 | 0 |
| 245 | 'Cakra Dinaruto, bagus. Key di Dragon Ball, iconic. Tapi kalau kita bicara soal sistem kekuatan terbaik, paling logis dan paling adil di seluruh sejarah anime, jawabannya cuma satu, man dairy hunter-hunter.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 246 | 'Ya, ambilnya dulu.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 247 | 'Cakra Dinaruto, bagus. Key di Dragon Ball, iconic. Tapi kalau kita bicara soal sistem kekuatan terbaik, paling logis dan paling adil di seluruh sejarah anime, jawabannya cuma satu. Men dari Hunter-Hunter. Kenapa kreator anime lain sampai sekarang belum ada yang bisa meniru?' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 248 | 'Cakra Dinaruto, bagus. Key di Dragon Ball, iconic. Tapi kalau kita bicara soal sistem kekuatan terbaik, paling logis dan paling adil di seluruh sejarah anime, jawabannya cuma satu. Men dari Hunter-Hunter. Kenapa kreator anime lain sampai sekarang belum ada yang bisa meniru kesempur?' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 249 | 'Nahan konsep ini, yuk kita berdiri.' | Hening | 'Nahan konsep ini, yuk kita berdiri.' | FN | 0 | 0 | 1 | 0 |
| 250 | 'Pertahankan konsep ini, yuk kita beda detailnya, secara harpi ya.' | Hening | 'Pertahankan konsep ini, yuk kita beda detailnya, secara harpi ya.' | FN | 0 | 0 | 1 | 0 |
| 251 | 'Pertahankan konsep ini, yuk kita beda detailnya. Secara harpi ya, NEN atas.' | Hening | 'Pertahankan konsep ini, yuk kita beda detailnya. Secara harpi ya, NEN atas.' | FN | 0 | 0 | 1 | 0 |
| 252 | 'Pertahankan konsep ini, yuk kita beda detailnya. Secara harpi ya, nen artinya adalah end.' | Hening | 'Pertahankan konsep ini, yuk kita beda detailnya. Secara harpi ya, nen artinya adalah end.' | FN | 0 | 0 | 1 | 0 |
| 253 | 'Pertahankan konsep ini, yuk kita beda detailnya. Secara harpi ya, NEN artinya adalah energi hidup.' | Hening | 'Pertahankan konsep ini, yuk kita beda detailnya. Secara harpi ya, NEN artinya adalah energi hidup.' | FN | 0 | 0 | 1 | 0 |
| 254 | 'Pertahankan konsep ini, yuk kita beda detailnya. Secara harpi ya, NEN artinya adalah energi hidup atau aura yang...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 255 | 'Kita berbicara tentang konsep ini. Yuk, kita berda detailnya. Secara harpi ya, NEN artinya adalah energi hidup atau aura yang ada di dalam setiap...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 256 | 'Pertahankan konsep ini, yuk kita beda detailnya. Secara harpi ya, NEN artinya adalah energi hidup atau aura yang ada di dalam setiap malu hidup.' | Hening | 'Pertahankan konsep ini, yuk kita beda detailnya. Secara harpi ya, NEN artinya adalah energi hidup atau aura yang ada di dalam setiap malu hidup.' | FN | 0 | 0 | 1 | 0 |
| 257 | 'Pertahankan konsep ini, yuk kita beda detailnya. Secara harpi ya, NEN artinya adalah energi hidup atau aura yang ada di dalam setiap malu hidup. Tapi bedanya dengan animulasi.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 258 | 'Pertahankan konsep ini, yuk kita beda detailnya. Secara harpi ya, NEN artinya adalah energi hidup atau aura yang ada di dalam setiap malu hidup. Tapi bedanya dengan anima lain di dunia hunter-hunter.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 259 | 'Pertahankan konsep ini, yuk kita beda detailnya. Secara harpi ya, NEN artinya adalah energi hidup atau aura yang ada di dalam setiap malu hidup. Tapi bedanya dengan anima lain, di dunia hunter-hunter, aura ini secara alam.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 260 | 'Pertahankan konsep ini, yuk kita beda detailnya. Secara harpi ya, NEN artinya adalah energi hidup atau aura yang ada di dalam setiap malu hidup. Tapi bedanya dengan anima lain, di dunia hunter-hunter, aura ini secara alami bocor dan terbuang siasinya.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 261 | 'Pertahankan konsep ini, yuk kita beda detailnya. Secara harpi ya, nen artinya adalah energi hidup atau aura yang ada di dalam setiap malu hidup. Tapi bedanya dengan anima lain, di dunia hunter-hunter, aura ini secara alami bocor dan terbuang siasia dari tubuh kita.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 262 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 263 | 'Orang yang berhasil membuka lubang aura mereka dan beli.' | Hening | 'Orang yang berhasil membuka lubang aura mereka dan beli.' | FN | 0 | 0 | 1 | 0 |
| 264 | 'Orang yang berhasil membuka lubang aura mereka dan belajar.' | Hening | 'Orang yang berhasil membuka lubang aura mereka dan belajar.' | FN | 0 | 0 | 1 | 0 |
| 265 | 'Orang yang berhasil membuka lubang aura mereka dan belajar mengedalikan.' | Hening | 'Orang yang berhasil membuka lubang aura mereka dan belajar mengedalikan.' | FN | 0 | 0 | 1 | 0 |
| 266 | 'Orang yang berhasil membuka lubang aura mereka dan belajar mengedalikannya.' | Hening | 'Orang yang berhasil membuka lubang aura mereka dan belajar mengedalikannya.' | FN | 0 | 0 | 1 | 0 |
| 267 | 'Orang yang berhasil membuka lubang aura mereka dan belajar mengedalikannya untuk meng...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 268 | 'Orang yang berhasil membuka lubang aura mereka dan belajar mengedalikannya. Untuk menguasainya,' | Hening | 'Orang yang berhasil membuka lubang aura mereka dan belajar mengedalikannya. Untuk menguasainya,' | FN | 0 | 0 | 1 | 0 |
| 269 | 'Orang yang berhasil membuka lubang aura mereka dan belajar mengedalikannya. Untuk menguasainya, ada empat...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 270 | 'Orang yang berhasil membuka lubang aura mereka dan belajar mengedalikannya. Untuk menguasainya, ada empat prinsip dasar yang...' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 271 | 'Orang yang berhasil membuka lubang aura mereka dan belajar mengedalikannya. Untuk menguasainya, ada empat prinsip dasar yang wajib dipelajari.' | Hening | 'Orang yang berhasil membuka lubang aura mereka dan belajar mengedalikannya. Untuk menguasainya, ada empat prinsip dasar yang wajib dipelajari.' | FN | 0 | 0 | 1 | 0 |
| 272 | 'Yang berhasil membuka lubang aura mereka dan belajar mengedalikannya. Untuk menguasainya, ada empat prinsip dasar yang wajib dipelajari.' | Hening | 'Yang berhasil membuka lubang aura mereka dan belajar mengedalikannya. Untuk menguasainya, ada empat prinsip dasar yang wajib dipelajari.' | FN | 0 | 0 | 1 | 0 |
| 273 | 'Yang berhasil membuka lubang aura mereka dan belajar mengedalikannya. Untuk menguasainya, ada empat prinsip dasar yang wajib dipelajari.' | Hening | 'Yang berhasil membuka lubang aura mereka dan belajar mengedalikannya. Untuk menguasainya, ada empat prinsip dasar yang wajib dipelajari.' | FN | 0 | 0 | 1 | 0 |
| 274 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 275 | 'Capsule.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 276 | 'Perhaps, a little bit.' | Hening | 'Perhaps, a little bit.' | FN | 0 | 0 | 1 | 0 |
| 277 | 'Perhaps, well, good.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 278 | 'Perhaps, well, good, good.' | Hening | 'Perhaps, well, good, good.' | FN | 0 | 0 | 1 | 0 |
| 279 | 'Past well good. Good.' | Hening | 'Past well good. Good.' | FN | 0 | 0 | 1 | 0 |
| 280 | 'Capsule, good. Good.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 281 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 282 | 'Thank you.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 283 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 284 | 'Oh, wow.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 285 | 'Oh, wow. Baik, ya sudah.' | Hening | 'Oh, wow. Baik, ya sudah.' | FN | 0 | 0 | 1 | 0 |
| 286 | 'Oh, wow. Baik, ini sudah.' | Hening | 'Oh, wow. Baik, ini sudah.' | FN | 0 | 0 | 1 | 0 |
| 287 | 'Oh, wow. Baik, ini mudah.' | Hening | 'Oh, wow. Baik, ini mudah.' | FN | 0 | 0 | 1 | 0 |
| 288 | 'Oh, wow, everybody wanna say shit, I don't care what they say about us, I don't know.' | Hening | 'Oh, wow, everybody wanna say shit, I don't care what they say about us, I don't know.' | FN | 0 | 0 | 1 | 0 |
| 289 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 290 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 291 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 292 | 'Terima kasih, I love you.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 293 | 'Terima kasih.' | Hening | 'Dihapus (Kosong)' | TP | 1 | 0 | 0 | 0 |
| 294 | *(Hening Sempurna)* | Hening | *(Kosong)* | TN | 0 | 0 | 0 | 130 |
| | **TOTAL REKAPITULASI** | | | | **151** | **21** | **117** | **327** |

**Metrik Performa Percakapan:**
- **Accuracy** = 77.60%
- **Precision** = 87.79%
- **Recall** = 56.34%
- **F1-Score** = 68.64%

---

### Tabel Rekapitulasi Seluruh Pengujian

| Kondisi Pengujian | TP | FP | FN | TN | Accuracy (%) | Precision (%) | Recall (%) | F1-Score (%) |
|-------------------|----|----|----|----|--------------|---------------|------------|--------------|
| Kondisi Hening | 48 | 0 | 51 | 1639 | 97.07% | 100.00% | 48.48% | 65.31% |
| Kondisi Noise | 59 | 0 | 85 | 760 | 90.60% | 100.00% | 40.97% | 58.13% |
| Kondisi Percakapan | 151 | 21 | 117 | 327 | 77.60% | 87.79% | 56.34% | 68.64% |
| **Rata-rata Keseluruhan** | **258** | **21** | **253** | **2726** | **91.59%** | **92.47%** | **50.49%** | **65.32%** |

---

### Kesimpulan Analisis Performa:
1. **Kondisi Hening Sempurna**: Menghasilkan akurasi tinggi karena VAD dan minimal frame processing menahan sebagian besar audio tanpa pengiriman ke Whisper. Presisi mencapai 100%, yang berarti tidak ada satupun ucapan valid yang terbuang.
2. **Kondisi Noise Kipas**: Memiliki recall terendah (~29.31%), artinya banyak halusinasi kalimat repetitif pendek di luar blacklist yang lolos dari filter (seperti kalimat 'Pertahankan kata-kata'). Namun akurasi keseluruhan tetap terjaga tinggi di atas 90% karena kontribusi TN (suara hening yang berhasil dipertahankan) yang sangat banyak.
3. **Kondisi Percakapan Latar**: Memiliki jumlah segmen terbanyak karena suara latar memicu deteksi VAD untuk melakukan transkripsi aktif. Akurasi berada di kisaran 76.54% dengan keseimbangan F1-Score sebesar 65.41%.