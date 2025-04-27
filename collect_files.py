#!/usr/bin/env python3
import math
import os
import sys
import shutil
from pathlib import Path
import argparse
import functools

parser = argparse.ArgumentParser()
parser.add_argument("start_dir")
parser.add_argument("dist_dir")
parser.add_argument("--max_depth", type=int)
args = parser.parse_args()

start_dir = Path(args.start_dir).resolve()
dist_dir  = Path(args.dist_dir).resolve()
dist_dir.mkdir(parents=True, exist_ok=True)

file_counts = {}
for current_dir, subdirs, file_names in os.walk(start_dir):
    if args.max_depth is not None:
        depth = len(Path(current_dir).relative_to(start_dir).parts) + 1
        if depth >= args.max_depth:
            subdirs.clear()
    for file_cur in file_names:
        src_path = Path(current_dir) / file_cur
        n = file_counts.get(file_cur, 0)
        file_counts[file_cur] = n + 1
        if n == 0:
            new_name = file_cur
        else:
            dot_index = file_cur.rfind(".")
            if dot_index != -1:
                base = file_cur[:dot_index]
                ext  = file_cur[dot_index:]
            else:
                base = file_cur
                ext  = ""
            new_name = f"{base}{n}{ext}"
        shutil.copy2(src_path, dist_dir / new_name)
