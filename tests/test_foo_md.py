from writhub.foo.md import *
from pathlib import Path
import pytest

def test_foo_hasnt_been_renamed_yet_tk():
    assert Path('./writhub/foo/md.py').exists()


def test_default_output_filename_is_in_ignore_list():
    assert DEFAULT_COLLATED_FILENAME in IGNORE_FILE_PATTERNS



def test_collate_markdown_files_accepts_list_or_pathdir():
    collate_markdown_files(Path("/tmp"))
    collate_markdown_files([Path("./writhub/__init__.py")])

    with pytest.raises(ValueError) as err:
        collate_markdown_files("/tmp")

def test_collate_markdown_files_does_not_accept_filename():
    with pytest.raises(ValueError) as err:
        collate_markdown_files(Path("./writhub/__init__.py"))

    assert "must point to a directory" in str(err.value)
