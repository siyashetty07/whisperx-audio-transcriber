import os
import json
import whisperx
from dotenv import load_dotenv
from whisperx.diarize import assign_word_speakers
from whisperx.diarize import DiarizationPipeline
import sys
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

device = "cpu"

audio_file = sys.argv[1]
if len(sys.argv) < 2:
    print(
        "Usage: python src/transcribe_diarized.py input/audio.wav"
    )
    sys.exit(1)
base_name = os.path.splitext(
    os.path.basename(audio_file)
)[0]
output_json = (
    f"output/{base_name}_diarized.json"
)
print("Loading ASR model...")

model = whisperx.load_model(
    "base",
    device=device,
    compute_type="int8"
)

print("Transcribing...")

result = model.transcribe(audio_file)

print("Loading alignment model...")

model_a, metadata = whisperx.load_align_model(
    language_code=result["language"],
    device=device
)

result = whisperx.align(
    result["segments"],
    model_a,
    metadata,
    audio_file,
    device
)

print("Running speaker diarization...")

diarize_model = DiarizationPipeline(
    token=HF_TOKEN,
    device=device
)

diarize_segments = diarize_model(audio_file)

result = assign_word_speakers(
    diarize_segments,
    result
)

with open(
    output_json,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        result,
        f,
        indent=2,
        ensure_ascii=False
    )

print(
    f"Saved {output_json}"
)