#!/usr/bin/env python3
"""Automated File & Downloads Organizer (os + shutil only).

Usage:
  python organizer.py                       # organize ~/Downloads
  python organizer.py /path/to/folder       # organize a specific folder
  python organizer.py --dry-run             # preview, move nothing
  python organizer.py --watch --interval 30 # keep organizing every 30s
  python organizer.py --undo                # revert the last run
"""
import argparse, json, os, shutil, time
from pathlib import Path

CATEGORIES = {
    "Images":      {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".heic"},
    "Videos":      {".mp4", ".mkv", ".mov", ".avi", ".webm"},
    "Audio":       {".mp3", ".wav", ".flac", ".m4a", ".ogg"},
    "Documents":   {".pdf", ".doc", ".docx", ".txt", ".md", ".ppt", ".pptx", ".odt", ".epub"},
    "Spreadsheets": {".xls", ".xlsx", ".csv", ".ods"},
    "Archives":    {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code":        {".py", ".js", ".html", ".css", ".json", ".java", ".cpp", ".c", ".sh", ".ts"},
    "Installers":  {".exe", ".msi", ".apk", ".dmg", ".deb"},
}
SKIP_SUFFIXES = {".crdownload", ".part", ".tmp", ".download"}  # unfinished downloads
LOG_NAME = ".organizer_log.json"


def category_for(path: Path) -> str:
    ext = path.suffix.lower()
    return next((c for c, exts in CATEGORIES.items() if ext in exts), "Others")


def unique_target(target: Path) -> Path:
    """photo.png -> photo (1).png if it already exists."""
    if not target.exists():
        return target
    n = 1
    while (cand := target.with_name(f"{target.stem} ({n}){target.suffix}")).exists():
        n += 1
    return cand


def organize(folder: Path, dry_run=False) -> list:
    moves = []
    for entry in sorted(os.scandir(folder), key=lambda e: e.name):
        p = Path(entry.path)
        if not entry.is_file() or p.name.startswith(".") or p.suffix.lower() in SKIP_SUFFIXES:
            continue
        dest_dir = folder / category_for(p)
        dest = unique_target(dest_dir / p.name)
        print(f"{'[dry] ' if dry_run else ''}{p.name}  →  {dest_dir.name}/{dest.name}")
        if not dry_run:
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(p), str(dest))
            moves.append({"from": str(p), "to": str(dest)})
    if moves:
        (folder / LOG_NAME).write_text(json.dumps(moves, indent=2))
    if not dry_run:
        print(f"Moved {len(moves)} file(s)")
    return moves


def undo(folder: Path):
    log = folder / LOG_NAME
    if not log.exists():
        return print("Nothing to undo.")
    for m in reversed(json.loads(log.read_text())):
        src, dst = Path(m["to"]), Path(m["from"])
        if src.exists():
            shutil.move(str(src), str(unique_target(dst)))
            print(f"Restored {dst.name}")
    log.unlink()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", nargs="?", default=str(Path.home() / "Downloads"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--interval", type=int, default=30)
    ap.add_argument("--undo", action="store_true")
    a = ap.parse_args()
    folder = Path(a.folder).expanduser()
    if not folder.is_dir():
        raise SystemExit(f"Not a folder: {folder}")
    if a.undo:
        return undo(folder)
    try:
        while True:
            organize(folder, a.dry_run)
            if not a.watch:
                break
            time.sleep(a.interval)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
