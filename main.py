#!/usr/bin/env python3
"""Entrypoint: copy the pre-rendered entry.png to $MAKEFUN_OUTPUT_DIR."""
import os, shutil

src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
print("wrote", os.path.join(out_dir, "entry.png"))
