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
max_depth = args.max_depth
file_counts = {}
for current_dir, subdirs, file_names in os.walk(start_dir):
    depth = len(Path(current_dir).relative_to(start_dir).parts)
    rel = Path(current_dir).relative_to(start_dir)
    parts = rel.parts
    if max_depth is not None:
        if depth >= max_depth:
            subdirs.clear()  
        if len(parts) >= max_depth:     
            parts = parts[:max_depth]

    new_fold = dist_dir.joinpath(*parts)
    new_fold.mkdir(parents=True, exist_ok=True)

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
        shutil.copy2(src_path, new_fold / new_name)