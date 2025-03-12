'''
import whisper

model = whisper.load_model("small")  # You can also use "small", "medium", or "large"
result = model.transcribe("audio.mp3")
print(result["text"])

'''

'''
import time
import whisper

model_name = "small"  # Change to "tiny", "base", "small", "medium", "large"

model = whisper.load_model(model_name)

start_time = time.time()
result = model.transcribe("audio.mp3")  # Replace with your file
end_time = time.time()

print("Transcription:", result["text"])
print(f"⏳ Time taken: {end_time - start_time:.2f} seconds")

'''

import time
import torch
import whisper

torch.set_num_threads(torch.get_num_threads())  # Use all CPU cores

model = whisper.load_model("medium")  # More accurate than "tiny" or "base"

start_time = time.time()
result = model.transcribe("audio.mp3", fp16=False, language="english",  task="transcribe")  # Force English
end_time = time.time()

print("Transcription:", result["text"])
print(f"⏳ Time taken: {end_time - start_time:.2f} seconds")
