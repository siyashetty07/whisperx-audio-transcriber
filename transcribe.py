import whisperx
import json

audio_file = "input/sample.wav"
device = "cpu"

print("Loading model...")

model = whisperx.load_model(
    "base",
    device=device,
    compute_type="int8"
)

print("Transcribing...")

result = model.transcribe(audio_file)

with open("output/transcript.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("Saved to output/transcript.json")

full_text = " ".join(
    segment["text"]
    for segment in result["segments"]
)

print("\nTranscript:\n")
print(full_text)