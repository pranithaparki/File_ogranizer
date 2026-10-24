# File & Downloads Organizer

A Python script that automatically sorts messy folders (like Downloads) into categories such as Images, Documents, Archives and more. It uses only the standard library (`os`, `shutil`), so there is nothing to install.

## Features

- Sorts files by type into folders
- Dry-run mode to preview before moving anything
- Undo the last run
- Watch mode to keep organizing automatically
- Never overwrites files (duplicates become `photo (1).png`)
- Skips unfinished downloads

## Usage

```bash
python organizer.py --dry-run          # preview only
python organizer.py                    # organize ~/Downloads
python organizer.py "C:\my\folder"     # organize a specific folder
python organizer.py --undo             # revert the last run
python organizer.py --watch            # keep running
```

## Example

```text
photo.png      →  Images/photo.png
report.pdf     →  Documents/report.pdf
setup.exe      →  Installers/setup.exe
archive.zip    →  Archives/archive.zip
```

## Customize

Edit the `CATEGORIES` dictionary in `organizer.py` to add your own file types and folders.

## Tech Stack

Python (os, shutil, pathlib, argparse)
