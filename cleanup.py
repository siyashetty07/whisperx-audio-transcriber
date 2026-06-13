import sys
from openai import AzureOpenAI
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY")
)

SYSTEM_PROMPT = """
You are a professional transcript editor.

Rules:
- Fix punctuation.
- Fix capitalization.
- Correct obvious speech recognition mistakes.
- Preserve the original speaker's intent, style, and tone.
-Transcribe it smartly preserving the meaning.
- Do not change meaning.
- Do not summarize.
- Do not add information that was not spoken.
- Return only the corrected text.
"""


def clean_segment(text):

    for attempt in range(3):

        try:

            response = client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                temperature=0
            )

            cleaned = response.choices[0].message.content
            return cleaned.strip()

        except Exception as e:

            print(
                f"Attempt {attempt + 1}/3 failed: {e}"
            )

            if attempt == 2:
                print(
                    "Using original text."
                )
                return text

            time.sleep(2)


def clean_transcript(
    input_file,
    output_file
):

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    segments = data.get(
        "segments",
        []
    )

    total = len(segments)

    print(
        f"Found {total} segments"
    )

    for i, segment in enumerate(
        segments,
        start=1
    ):

        original_text = segment.get(
            "text",
            ""
        )

        print(
            f"Cleaning segment {i}/{total}"
        )

        cleaned_text = clean_segment(
            original_text
        )

        segment[
            "clean_text"
        ] = cleaned_text

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"\nSaved cleaned transcript to:\n{output_file}"
    )


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print(
            "Usage: python src/cleanup.py input.json output.json"
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    clean_transcript(
        input_file,
        output_file
    )