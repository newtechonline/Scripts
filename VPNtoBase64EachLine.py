import base64
import sys
from pathlib import Path


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python base64_each_line.py input.txt [output.txt]")
        sys.exit(1)

    input_file = Path(sys.argv[1])

    if len(sys.argv) == 3:
        output_file = Path(sys.argv[2])
    else:
        output_file = input_file.with_name(input_file.stem + "-base64" + input_file.suffix)

    if not input_file.is_file():
        print(f"Error: input file not found: {input_file}")
        sys.exit(1)

    input_count = 0
    output_count = 0

    with input_file.open("r", encoding="utf-8", newline="") as src, \
         output_file.open("w", encoding="ascii", newline="\n") as dst:

        for raw_line in src:
            line = raw_line.rstrip("\r\n")

            if not line.strip():
                continue

            encoded = base64.b64encode(line.encode("utf-8")).decode("ascii")
            dst.write(encoded + "\n")

            input_count += 1
            output_count += 1

    print(f"Input entries : {input_count}")
    print(f"Output entries: {output_count}")
    print(f"Output file   : {output_file}")

    if input_count != output_count:
        print("ERROR: entry count mismatch!")
        sys.exit(1)

    print("OK: every input line was encoded exactly once.")


if __name__ == "__main__":
    main()
