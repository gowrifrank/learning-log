"""Rebuild every PDF (cheat sheet + study pack, A4 and phone).

Usage:  python build_pdfs.py
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / "cheatsheet"))
sys.path.insert(0, str(REPO / "study-pack"))

import build_cheatsheet
import build_study_pack

build_cheatsheet.build()
build_study_pack.build()
