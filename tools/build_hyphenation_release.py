"""Build the standalone Finnish hyphenation package for GitHub sharing."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from build_hyphenation import ROOT, OUTPUT, read_patterns, render


ARCHIVE = ROOT / "Affinity-suomi-tavutus.zip"
PACKAGE = "Affinity-suomi-tavutus"
FILES = {
    "README.md": ROOT / "TAVUTUS-JULKAISU.md",
    "LICENSE": ROOT / "LICENSE",
    "hyph_fi_FI.dic": OUTPUT,
    "hyphenation_patterns.txt": ROOT / "hyphenation_patterns.txt",
    "tools/build_hyphenation.py": ROOT / "tools/build_hyphenation.py",
    "tools/build_hyphenation_release.py": ROOT / "tools/build_hyphenation_release.py",
}


def main():
    expected = render(read_patterns()).encode("utf-8")
    if OUTPUT.read_bytes() != expected:
        raise ValueError("Rebuild hyph_fi_FI.dic before packaging")
    with ZipFile(ARCHIVE, "w", ZIP_DEFLATED) as package:
        for name, path in FILES.items():
            package.write(path, f"{PACKAGE}/{name}")
    with ZipFile(ARCHIVE) as package:
        if package.testzip() is not None:
            raise ValueError("The release ZIP failed its integrity check")
        for name, path in FILES.items():
            if package.read(f"{PACKAGE}/{name}") != path.read_bytes():
                raise ValueError(f"Incorrect packaged file: {name}")
    print(f"{ARCHIVE.name}: {ARCHIVE.stat().st_size} bytes, {len(FILES)} files")


if __name__ == "__main__":
    main()
