"""
Reliafy is now Brinkpy. This final release of Reliafy only tells users where to go.
Copyright (c) 2025 Cesar Carrasco. All rights reserved.
"""

import sys

MESSAGE = """\
Reliafy is now Brinkpy.

Reliafy is no longer maintained, and its commands no longer run.
Brinkpy is the same software under its new name, with new features and fixes.

Install Brinkpy:     pip install brinkpy
Then run:            brinkpy --help
Documentation:       https://brinkpy.app
"""


def main() -> int:
    print(MESSAGE, file=sys.stderr)
    return 1
