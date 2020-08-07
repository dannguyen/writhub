#!/usr/bin/env python3
import click
from pathlib import Path

from writhub.foo.md import collate_markdown_files, DEFAULT_COLLATED_FILENAME, gather_markdown_paths

@click.group()
def main():
    """
    whats up, this is the main function :)
    """
    click.secho("The main foo", bg='black', fg='blue')


@main.command()
def foo():
    """
    foo this is for foos!
    """
    click.secho("FOO", fg="red", bg="white")


@main.command()
@click.argument("src-dir", nargs=1, type=click.Path(exists=True, file_okay=False))
def md(src_dir):
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


    output_filename = DEFAULT_COLLATED_FILENAME

    txt = collate_markdown_files(src_dir, ignore_output_filename=output_filename)

    # target_path = src_dir + output_filename
    target_path = src_dir.joinpath(output_filename)
    click.echo(f"Collating to {target_path}")

    target_path.write_text(txt)

if __name__ == '__main__':
    main()
