#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
from sys import argv, stderr

from writhub.writhub import COMPILE_HEADER, DEFAULT_COLLATED_FILENAME, IGNORE_DIR_PATTERNS, IGNORE_FILE_PATTERNS




def collate_markdown_files(src, ignore_output_filename=DEFAULT_COLLATED_FILENAME, options={}):
    """
    src_path <Path or list of paths>

    returns a text string consisting of the concatenated content of
        valid *.md files found in `src_dir`

    TODO: have an option to not insert file break comments
    TODO: ignore_output_filename edge cases handled/tested
    """
    if type(src) is list:
        src_paths = src
    elif issubclass(type(src), Path):
        if src.is_dir():
            src_paths = gather_markdown_paths(src)
        else:
            raise ValueError(f"src argument, {src}, must point to a directory, not a file/non-directory")
    else:
        raise ValueError(f"Expected src argument to be directory or list, not {type(src)}")

    txt = f"{COMPILE_HEADER}\n"
    for path in src_paths:
        txt += f"\n<!-- [writhub-collation]: {path}  -->\n"
        txt += path.read_text()
        txt += f"\n<!-- [/writhub-collation]: {path}  -->\n"

    return txt


def insert_markdown_toc(src_path):
    subprocess.call(['markdown-toc', '-i', src_path,])



def gather_markdown_paths(src_dir):
    """
    TODO: right now, only the parent directory is checked for ignored dir patterns
    """
    src_dir = Path(src_dir)

    mdpaths = []
    for path in src_dir.glob('*.md'):
        if (any(re.match(rx, path.name) for rx in IGNORE_FILE_PATTERNS)
            or any(re.match(rx, path.parent.name) for rx in IGNORE_DIR_PATTERNS)
            ):
            pass
        else:
            mdpaths.append(path)


    return sorted(mdpaths)



def collate_to_file(src_dir, target_path, options={}):
    """
    all in one method that given a src_dir and a target_path,
    creates the new collated markdown file and does postprocessing,
    like insert_markdown_toc and asset_syncing
    """
    src_dir = Path(src_dir)
    target_path = Path(target_path)
    target_dir = target_path.parent

    if target_dir != src_dir:
        # TODO: then do asset syncing
        target_dir.mkdir(exist_ok=True, parents=True)


    txt = collate_markdown_files(src_dir, options=options)

    target_path.write_text(txt)

    insert_markdown_toc(target_path)


if __name__ == '__main__':
    if len(argv) > 2:
        src_dir, target_path = [Path(p) for p in argv[1:3]]
    else:
        src_dir = Path(argv[1])
        target_path = src_dir.joinpath(DEFAULT_COLLATED_FILENAME)

    stderr.write(f"Reading from {src_dir} \n")
    collate_to_file(src_dir, target_path)
    stderr.write(f"Wrote to {target_path} \n")
