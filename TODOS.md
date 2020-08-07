# TODOS

## General

- figure out logging situation

## console/cli

### general options

- `--dry-run`/`analyze`
- `--no-metamarks` (e.g. HTML comments indicating where file concats occur)

### md subcommand

- add options to `md` subcommand
    - output_filename
    - output_dir
    - --dry-run
- cleanup and refactor `md` command, maybe into console/md


```sh
# given a subdir full of md, produces a SRC_DIR/index.md with TOC
# won't overwrite existing index.md unless --overwrite
$ writhub md [SRC_DIR]

# assume that --src-dir is where the compiled markdown file goes
# option to specify exact  --output-filename
$ writhub md [SRC_DIR] --output-filename notindex.md

# specifying a different --output-dir will result in not just
# a index.md being created in that directory, but the subdirs/assets folder
# being rsynced
$ writhub md [SRC_DIR] --output-dir /tmp/else/where
```



## foo/md

- Handle TOC insertion
- rsyncing of subdirectories when output_dir is set
    - should `md` command rsync everything from src_dir into output_dir? Why not




## Diagnostics

- does compiled markdown file have TOC?
