#!/usr/bin/env python3
"""make.fun entry for "Sum up 26 November's world news in one image".

Copies the committed news.png (a newspaper-style front page of
Thursday 26 November 2026) to /output/entry.png. Standard library only.
Running it twice writes identical bytes.
"""

import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "news.png")


def output_dir():
    """Writable directory for entry.png: /output in the grader, else ./output."""
    for candidate in ("/output", os.path.join(os.getcwd(), "output")):
        try:
            os.makedirs(candidate, exist_ok=True)
            return candidate
        except OSError:
            continue
    raise OSError("no writable output directory")


def file_sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    dst = os.path.join(output_dir(), "entry.png")
    shutil.copyfile(SRC, dst)
    print("wrote {} ({} bytes, sha256 {})".format(
        dst, os.path.getsize(dst), file_sha256(dst)))


if __name__ == "__main__":
    main()
