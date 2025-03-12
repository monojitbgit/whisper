#1g0sWtaMi13VLZXbA1k3uxKyrZmeqPu2PfZygljrb6cM

import os
import time
import torch
import whisper
import gspread
from google.oauth2.service_account import Credentials

# 🔹 1. Authenticate Google Sheets API
GOOGLE_SHEETS_CREDENTIALS = "credentials.json"  # Ensure this file exists

scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(GOOGLE_SHEETS_CREDENTIALS, scopes=scopes)
gc = gspread.authorize(creds)

# 🔹 2. Open the Google Sheet
SPREADSHEET_ID = "1g0sWtaMi13VLZXbA1k3uxKyrZmeqPu2PfZygljrb6cM"  # Replace with actual Sheet ID
SHEET_NAME = "Data"
worksheet = gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# 🔹 3. Get All Audio Files in Local "audio/" Folder
audio_folder = "audio"
audio_files = [f for f in os.listdir(audio_folder) if f.endswith((".mp3", ".wav", ".m4a"))]

print(f"🔍 Found {len(audio_files)} audio files.")

# 🔹 4. Write File Names to Google Sheets (C2:C)
file_names = [[file] for file in audio_files]  # Convert list to Google Sheets format
worksheet.update("C2", file_names)  # Write all file names to column C starting from C2

print("✅ File names successfully written to Google Sheets.")

# 🔹 5. Load Whisper Model
torch.set_num_threads(torch.get_num_threads())  # Use all CPU cores
model = whisper.load_model("medium")  # Use "medium" for better accuracy

# 🔹 6. Transcribe Each Audio File
transcriptions = []
for file in audio_files:
    file_path = os.path.join(audio_folder, file)
    print(f"🎙 Transcribing: {file_path}")
    
    start_time = time.time()
    result = model.transcribe(file_path, fp16=False, language="english", task="transcribe")
    transcriptions.append([result["text"]])  # Convert to list format for Google Sheets
    
    end_time = time.time()
    print(f"✅ Transcribed {file} in {end_time - start_time:.2f} seconds")

# 🔹 7. Write Transcriptions Back to Google Sheets (D2:D)
worksheet.update("D2", transcriptions)  # Write transcriptions in column D

print("✅ All transcriptions saved in Google Sheets!")
