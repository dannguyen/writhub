#!/usr/bin/env python3
import click
from pathlib import Path
from writhub.writhub import COMPILE_HEADER, DEFAULT_COLLATED_FILENAME

from writhub.foo.md import collate_markdown_to_file, gather_markdown_paths
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
    mylogger.info('compile header:', COMPILE_HEADER)
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
    src_dir = Path(src_dir)
    click.echo(f"Processing {src_dir}")

    # TK: this is just debug info/ remove gather_markdown_paths
    srcpaths = gather_markdown_paths(src_dir)
    mylogger.info(f"Found {len(srcpaths)} in {src_dir}")
    mylogger.debug([str(s) for s in srcpaths])

    if not output_path:
        # then output dir is the src_dir
        output_filename = DEFAULT_COLLATED_FILENAME
        target_path = src_dir.joinpath(output_filename)
    else:
        output_path = Path(output_path)
        if '.md' not in output_path.name: # then --output-path points to a directory
            output_path = output_path.joinpath(DEFAULT_COLLATED_FILENAME)

        target_path = output_path
        output_filename = output_path.name

    # txt = collate_markdown_files(src_dir, ignore_output_filename=output_filename)
    # target_path = src_dir + output_filename
    # target_path.write_text(txt)

    click.echo(f"Collating to {target_path}")
    collate_markdown_to_file(src_dir, target_path, ignore_output_filename=output_filename)

if __name__ == '__main__':
    main()
