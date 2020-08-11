from writhub.foo.md import *
from writhub.writhub import COMPILE_HEADER
from pathlib import Path
import pytest

ONE_OFF = Path('./tests/samples/oneoff/000-hi.md')

def test_foo_hasnt_been_renamed_yet_tk():
    assert Path('./writhub/foo/md.py').exists()

###############
# what collate_markdown_files accepts as input
def test_default_output_filename_is_in_ignore_list():
    assert DEFAULT_COLLATED_FILENAME in IGNORE_FILE_PATTERNS

def test_collate_markdown_files_accepts_pathdir():
    collate_markdown_files(Path("/tmp"))

    with pytest.raises(ValueError) as err:
        """does not accept string"""
        collate_markdown_files("/tmp")

def test_collate_markdown_files_accepts_list():
    txt = collate_markdown_files([ONE_OFF])


def test_collate_markdown_files_does_not_accept_filename():
    with pytest.raises(ValueError) as err:
        collate_markdown_files(ONE_OFF)

    assert "must point to a directory" in str(err.value)


###############
# what collate_markdown_files outputs
def test_collate_markdown_files_simple_output_str():
    txt = collate_markdown_files([ONE_OFF])
    assert type(txt) is str
    assert '# hello world' in txt

def test_collate_markdown_files_has_compile_marker_in_first_line():
    txt = collate_markdown_files([ONE_OFF])
    line = txt.splitlines()
    assert line[0] == COMPILE_HEADER
