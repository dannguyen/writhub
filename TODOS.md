# TODOS

## Priority leftovers

- [?] Writhub.publish should rsync assets/ subdirectory
    - [x] simple test passed
    - [ ] test for only assets/ subdir is copied (for now)
    - [ ] test for validity of file contents
- [x] Prevent rsyncing when src_dir and target_dir are the same
- [ ] Prevent rsyncing when there is no assets/ dir
- [ ] Writhub should find assets subdirectory and add it as an attribute
    - [ ] what's purpose of writhub.settings.ASSETS_DIRECTORY_PATTEN?
- [ ] Writhub.publish should not wreck src_dir if target_dir is the same


- [?] MarkdownCollater should add TOC to file
    - but kind of slow
    - should investigate how markdown-toc works
    - [ ] Figure out how to use markdown-toc to generate toc to be captured via stdout?
    - [ ] Make better use of subprocess.run https://docs.python.org/3/library/subprocess.html

- Collater
    - necessary to have a closing collation marker?

## General

- [ ] set up cli to have general verbose option



- write some cli tests
    - [ ] test post_w_assets
    - [ ] test toc insertion

- make Writhub class 

- check out this writeup: https://medium.com/swlh/a-static-sites-generator-in-python-part-1-b2c421995ac1
- read source code to git/hyde


--------------------

# Done

- [X] fix cli_file_options tests
- [X] add "<!----collated-by-writhub--- -->" comment to all Markdown/HTML as an easy way of avoiding compiled files. Check first 10 lines

General
- [X] figure out logging situation
    - [X] remove manual stderr
    - [X] how to set up logging to filter out by levels?


---------------------


# Other stuff

## console/cli

### general options

- `--dry-run`/`analyze`
- `--no-metamarks` (e.g. HTML comments indicating where file concats occur)

### md subcommand

- add options to `md` subcommand
    - [x] output_path (either .md or dir)
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
