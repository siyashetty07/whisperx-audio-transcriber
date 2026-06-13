import os
import sys
import subprocess

python_exe = sys.executable

input_dir = "input"
output_dir = "output"

os.makedirs(output_dir, exist_ok=True)

wav_files = [
    f for f in os.listdir(input_dir)
    if f.lower().endswith(".wav")
]

if not wav_files:
    print("No WAV files found in input/")
    sys.exit(0)

for filename in wav_files:

    print("\n" + "=" * 50)
    print(f"Processing: {filename}")
    print("=" * 50)

    audio_path = os.path.join(
        input_dir,
        filename
    )

    base_name = os.path.splitext(
        filename
    )[0]

    diarized_json = os.path.join(
        output_dir,
        f"{base_name}_diarized.json"
    )

    clean_json = os.path.join(
        output_dir,
        f"{base_name}_clean.json"
    )

    transcript_txt = os.path.join(
        output_dir,
        f"{base_name}.txt"
    )

    print("\nStep 1/3: Transcribing...")

    subprocess.run(
        [
            python_exe,
            "src/transcribe_diarized.py",
            audio_path
        ],
        check=True
    )

    print("\nStep 2/3: Cleaning...")

    subprocess.run(
        [
            python_exe,
            "src/cleanup.py",
            diarized_json,
            clean_json
        ],
        check=True
    )

    print("\nStep 3/3: Exporting...")

    subprocess.run(
        [
            python_exe,
            "src/export.py",
            clean_json,
            transcript_txt
        ],
        check=True
    )

    print(f"\nFinished: {filename}")

print("\nAll files processed successfully!")