import base64
import re
import sys
from pathlib import Path


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python VPNtoBase64EachLine.py input.txt [output.txt]")
        sys.exit(1)

    input_file = Path(sys.argv[1])

    if len(sys.argv) == 3:
        output_file = Path(sys.argv[2])
    else:
        output_file = input_file.with_name(
            input_file.stem + "-base64" + input_file.suffix
        )

    if not input_file.is_file():
        print(f"Error: input file not found: {input_file}")
        sys.exit(1)

    data = input_file.read_text(encoding="utf-8")

    # Handle all common line separators:
    # LF, CRLF, CR, NEL, Unicode Line Separator, Unicode Paragraph Separator.
    lines = re.split(r"\r\n|\r|\n|\x85|\u2028|\u2029", data)

    # Remove empty lines and surrounding whitespace.
    lines = [line.strip() for line in lines if line.strip()]

    encoded_lines = []

    for line in lines:
        encoded = base64.b64encode(
            line.encode("utf-8")
        ).decode("ascii")

        encoded_lines.append(encoded)

    output_file.write_text(
        "\n".join(encoded_lines) + ("\n" if encoded_lines else ""),
        encoding="ascii",
        newline="\n",
    )

    print(f"Input entries : {len(lines)}")
    print(f"Output entries: {len(encoded_lines)}")
    print(f"Output file   : {output_file}")

    if len(lines) != len(encoded_lines):
        print("ERROR: entry count mismatch!")
        sys.exit(1)

    # Round-trip verification.
    decoded_lines = []

    for encoded in encoded_lines:
        decoded = base64.b64decode(encoded).decode("utf-8")
        decoded_lines.append(decoded)

    if decoded_lines != lines:
        print("ERROR: Base64 round-trip verification failed!")
        sys.exit(1)

    print("OK: Base64 round-trip verification passed.")

    # Check for duplicates.
    unique_count = len(set(lines))

    print(f"Unique entries: {unique_count}")

    if unique_count != len(lines):
        print(
            f"WARNING: {len(lines) - unique_count} duplicate entries found."
        )


if __name__ == "__main__":
    main()
