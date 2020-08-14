#!/usr/bin/env python3
import click
from pathlib import Path
from writhub.writhub import WRITHUB_PROJECT_HEADER, DEFAULT_COLLATED_FILENAME
from writhub.writhub import Writhub

from writhub.collaters.md import MarkdownCollater
from writhub.mylog import mylogger




@click.group()
def main():
    """
    Welcome to writhub
    """
    pass

@main.command()
def foo():
    """
    foo this is for foos!
    """
    mylogger.info("Welcome to writhub – a test")
    mylogger.info('compile header:', WRITHUB_PROJECT_HEADER)
    mylogger.debug("A debug message")
    mylogger.info("Info for you")
    mylogger.warning("Warning for this")
    mylogger.critical("Critical oops")
    mylogger.error("An error appears!")

    def _fubar(txt:str) -> int:
        val = len(str(txt))
        print("You gave me", txt, 'but i give you', val)
        return val

    _fubar(9)

@main.command()
@click.argument("src-dir", nargs=1, type=click.Path(exists=True, file_okay=False))
@click.option("--output-path", "-o", type=click.Path(file_okay=True, dir_okay=True), default=None)
def md(src_dir, output_path=None):
    """
    Convert a SRC_DIR directory of *.md files into one big Markdown file

    Example:

        $ writhub md tests/samples/post
    """

    # TK: this is just debug info/ remove gather_markdown_paths
    mylogger.info(f"Processing {src_dir}")
    hub = Writhub(mode='md', src_dir=src_dir, output_path=output_path)


    mylogger.info(f"Found {len(hub.content_list)} files")
    for i, p in enumerate(hub.content_list):
        mylogger.debug(f"{i}: {p}")


#   collate_markdown_to_file(src_dir, target_path, ignore_output_filename=output_filename)
    hub.publish()
    mylogger.info(f"Publishing to {hub.target_dir}")
    mylogger.info(f"Collated file is at: {hub.target_path}")


if __name__ == '__main__':
    main()
