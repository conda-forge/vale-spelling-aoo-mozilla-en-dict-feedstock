import os
import sys
from pathlib import Path
import shutil

VERSION = Path(os.environ["PKG_VERSION"])
SRC = Path(os.environ["SRC_DIR"])
PREFIX = Path(os.environ["PREFIX"])
PKGS = os.environ["VALE_PKGS"].split("")
LICENSE = SRC / "LICENSE"

OUT = PREFIX / "share/vale/styles"
DICPATH =  PREFIX / "share/hunspell/"

META_JSON_TEMPLATE = """{{
    "author": "Marco A.G. Pinto",
    "description": "Vale-compatible English Dictionaries Project (AOO+Mozilla+others) ({locale})",
    "sources": ["https://github.com/marcoagpinto/aoo-mozilla-en-dict"],
    "url": "https://github.com/marcoagpinto/aoo-mozilla-en-dict",
    "lang": "{{ locale }}",
    "license": "LGPL-3.0-or-later",
    "license_files": ["LICENSE"],
    "version": "{version}",
    "vale_version": ">=1.0.0",
}}"""

RULE_YML_TEMPLATE = """
---
extends: spelling
level: warning
message: "Did you really mean '%s'?"
custom: true
action:
  name: suggest
dicpath: {dicpath}
dictionaries:
  - {locale}
"""

TEMPLATES = {
    "meta.json": META_JSON_TEMPLATE,
    "Spelling.yml": RULE_YML_TEMPLATE,
}

def write_config():
    for pkg in PKGS:
        l10n = pkg.split("-")[-1].upper()
        dic = next(p for p in SRC.glob(f"en_{l10n} */*.dic"))
        ctx = {"locale": dic.stem, "version": VERSION, "dicpath": DICPATH}
        out_dir = OUT / pkg
        out_dir.mkdir(parents=True)
        for filename, template in TEMPLATES.items():
            shutil.copy2(LICENSE, out_dir / LICENSE.name)
            path = out_dir / filename
            print("\n-----------", path, "-----------")
            text = template.format(**ctx)
            print(text)
            path.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(write_config())
