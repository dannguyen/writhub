#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
from sys import argv

from writhub.collaters import TextCollater

TOC_MARKER = ('<!-- toc -->','<!-- tocstop -->')
toc_marker = ''.join(TOC_MARKER)

class MarkdownCollater(TextCollater):
    def insert_toc(self, src_path:Path):
        subprocess.call(['markdown-toc', '-i', src_path,])
        return super().insert_toc(src_path)




# def collate_markdown_to_file(src_dir, target_path, **kwargs):
#     """
#     all in one method that given a src_dir and a target_path,
#     creates the new collated markdown file and does postprocessing,
#     like insert_markdown_toc and asset_syncing
#     """
#     src_dir = Path(src_dir)
#     target_path = Path(target_path)
#     target_dir = target_path.parent

#     if target_dir != src_dir:
#         # TODO: then do asset syncing
#         target_dir.mkdir(exist_ok=True, parents=True)


#     txt = collate_markdown_files(src_dir, **kwargs)

#     target_path.write_text(txt)

#     insert_markdown_toc(target_path)


# if __name__ == '__main__':
#     if len(argv) > 2:
#         src_dir, target_path = [Path(p) for p in argv[1:3]]
#     else:
#         src_dir = Path(argv[1])
#         target_path = src_dir.joinpath(DEFAULT_COLLATED_FILENAME)

#     mylogger.info(f"Reading from {src_dir}")
#     collate_to_file(src_dir, target_path)
#     mylogger.info(f"Wrote to {target_path}")
