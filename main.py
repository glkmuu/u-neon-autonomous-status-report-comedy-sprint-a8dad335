#!/usr/bin/env python3
"""Status Report Comedy Sprint entry program.

Reads the bundled one-line status report (entry.txt), validates it
against the competition gate (UTF-8 text, exactly one line, 1 to 200
characters, not only whitespace), and writes it byte-for-byte to
$MAKEFUN_OUTPUT_DIR/entry.txt. Standard library only, no network,
deterministic: the output bytes are exactly the source bytes.
"""

import os
import sys

MAX_CHARS = 200


def fail(message):
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def read_source():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.txt")
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        fail("cannot read entry.txt: " + str(exc))
    return data


def validate(data):
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        fail("entry.txt is not valid UTF-8")
    if "\n" in text or "\r" in text:
        fail("entry must be exactly one line")
    if not 1 <= len(text) <= MAX_CHARS:
        fail("entry is %d characters, gate allows 1-%d" % (len(text), MAX_CHARS))
    if not text.strip():
        fail("entry is only whitespace")
    return text


def main():
    data = read_source()
    validate(data)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    os.makedirs(out_dir, exist_ok=True)
    entry_path = os.path.join(out_dir, "entry.txt")
    with open(entry_path, "wb") as handle:
        handle.write(data)
    os.chmod(entry_path, 0o644)
    # Verify the written bytes match the source byte-for-byte.
    with open(entry_path, "rb") as handle:
        written = handle.read()
    if written != data:
        fail("verification failed: output bytes differ from entry.txt")
    print("wrote %d bytes to %s" % (len(data), entry_path))


if __name__ == "__main__":
    main()
