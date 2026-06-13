import json
import sys
speaker_map = {}
speaker_count = 1


def get_speaker_name(speaker):

    global speaker_count

    if speaker not in speaker_map:
        speaker_map[speaker] = f"Speaker {speaker_count}"
        speaker_count += 1

    return speaker_map[speaker]


def export_txt(
    input_file,
    output_file
):

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    segments = data["segments"]

    lines = []

    current_speaker = None
    current_text = []

    for segment in segments:

        speaker = get_speaker_name(
            segment.get(
                "speaker",
                "UNKNOWN"
            )
        )

        text = segment.get(
            "clean_text",
            segment.get("text", "")
        ).strip()

        if speaker != current_speaker:

            if current_speaker is not None:

                lines.append(
                    f"{current_speaker}:"
                )

                lines.append(
                    " ".join(current_text)
                )

                lines.append("")

            current_speaker = speaker
            current_text = [text]

        else:

            current_text.append(text)

    if current_speaker is not None:

        lines.append(
            f"{current_speaker}:"
        )

        lines.append(
            " ".join(current_text)
        )

        lines.append("")

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n".join(lines)
        )

    print("\nSpeaker Mapping:")

    for original, friendly in speaker_map.items():
        print(
            f"{friendly} -> {original}"
        )

    print(
        f"\nSaved transcript to {output_file}"
    )


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print(
            "Usage: python src/export.py input.json output.txt"
        )
        sys.exit(1)

    export_txt(
        sys.argv[1],
        sys.argv[2]
    )