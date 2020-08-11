#!/usr/bin/env python3
import click
from pathlib import Path
from writhub.writhub import COMPILE_HEADER, DEFAULT_COLLATED_FILENAME

from writhub.foo.md import collate_markdown_files, gather_markdown_paths

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
    click.echo(COMPILE_HEADER)


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
    srcpaths = gather_markdown_paths(src_dir)
    click.echo(f"Found {len(srcpaths)} in {src_dir}")
    click.echo([str(s) for s in srcpaths])

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

    txt = collate_markdown_files(src_dir, ignore_output_filename=output_filename)

    # target_path = src_dir + output_filename
    click.echo(f"Collating to {target_path}")

    target_path.write_text(txt)

if __name__ == '__main__':
    main()
