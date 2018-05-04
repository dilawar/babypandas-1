#!/usr/bin/env bash
set -x
set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
for f in `find ./tests/*.py`; do
    python -m unittest $f
done
