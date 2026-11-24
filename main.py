#!/usr/bin/env python3
"""One Emoji, One Smile — write the chosen emoji to /output/entry.txt.

Chosen emoji: U+1F917 HUGGING FACE.

Why this one: a smiling face with open arms offering a hug. It is
unambiguously a smile, and the hug is an active offer of warmth to a
complete stranger — warm at first glance, understood at every age and
in every culture with no irony or in-joke, friendly without intimacy,
sarcasm or flirtation, and a deliberate pick rather than the default
smiley that first comes to mind. See PROGRESS.md for the full
shortlist reasoning against each rival.

Stdlib only. Deterministic: the same single emoji on every run.
"""

import os
import shutil

EMOJI = "\U0001F917"  # 🤗 Hugging Face


def clear_output_dir(output_dir):
    """Remove the CONTENTS of output_dir only; never the directory itself.

    The grader runs as a different uid, so deleting the mountpoint would
    throw EACCES. Clearing children is safe.
    """
    os.makedirs(output_dir, exist_ok=True)
    for name in os.listdir(output_dir):
        path = os.path.join(output_dir, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    clear_output_dir(output_dir)

    text = EMOJI
    # Validation guard: the gate requires UTF-8 text of 1-8 characters,
    # not only white space.
    assert 1 <= len(text) <= 8, "entry must be 1-8 characters"
    assert text.strip(), "entry must not be only white space"
    data = text.encode("utf-8")
    assert data.decode("utf-8") == text, "entry must round-trip as UTF-8"

    out_path = os.path.join(output_dir, "entry.txt")
    with open(out_path, "wb") as f:
        f.write(data)
    os.chmod(out_path, 0o644)

    # Re-read verification: confirm what landed on disk is exactly the
    # chosen emoji, byte for byte, before reporting success.
    with open(out_path, "rb") as f:
        written = f.read()
    assert written == data, "entry.txt on disk does not match the chosen emoji"
    assert written.decode("utf-8") == EMOJI
    print("wrote %s (%d bytes) to %s" % (EMOJI, len(written), out_path))


if __name__ == "__main__":
    main()
