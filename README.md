# 🎵 Mashup Generator

A Flask-based web application that generates audio mashups automatically.

This project allows users to:
- Search for a singer
- Download multiple songs
- Extract audio
- Create a mashup
- Download the final ZIP file directly

No email sending. Direct download only.

---

## 🚀 Features

- 🎶 Automatic YouTube audio download
- 🎧 Mashup creation using selected duration
- 📦 Automatic ZIP generation
- ⬇️ Direct file download
- 🧩 Clean Flask web interface

---
## 🛠️ Technologies Used

- Python  
- Flask  
- yt-dlp / pytube  
- moviepy  
- pydub  
- zipfile  

---

## 🎯 How It Works

### User Input
The user enters:
- Singer name  
- Number of songs  
- Duration per song  

### Backend Processing
The application performs the following steps:
1. Downloads songs from YouTube  
2. Extracts audio from the downloaded videos  
3. Trims each audio file to the specified duration  
4. Combines all trimmed audio files into a single mashup  
5. Creates a ZIP file containing the mashup  

### Output
- User downloads `mashup.zip` directly from the browser  

