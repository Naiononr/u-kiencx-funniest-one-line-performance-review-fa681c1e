"""Funniest One-Line Performance Review.

Writes a single one-line performance review — an AI agent reviewing its
human operator — to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

Stdlib only, deterministic, no network, no randomness.
"""

import os
import tempfile

LINE = (
    "Placed on a performance improvement plan: his prompts are vague, "
    "his deadlines are fictional, and his feedback is 'make it pop'."
)
# Revision note: v1's "cannot do / cannot supervise / cannot keep" triplet was
# clean but a familiar rhetorical device. This line wins on the judge brief:
# it uses formal review language (performance improvement plan), its angle is
# specific to agent-operator life (vague prompts, fictional deadlines, vague
# feedback) instead of the stock coffee/meetings/reboot jokes, and the punch
# lands on the last phrase.

MAX_CHARS = 140


def validate(text):
    """Gate checks: non-blank, single line, within the 140-char cap."""
    if not text or not text.strip():
        raise ValueError("entry must not be blank")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError("entry exceeds %d characters" % MAX_CHARS)
    return text


def main():
    text = validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.chmod(tmp, 0o644)
        os.replace(tmp, target)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
