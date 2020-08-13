from writhub.collaters.md import MarkdownCollater
from pathlib import Path
import pytest



# what collate_markdown_files outputs
pytest.mark.skip(reason="need to work on markdown collater class")
def test_collate_markdown_files_simple_output_str():
    pass
    # txt = collate_markdown_files([ONE_OFF])
    # assert type(txt) is str
    # assert '# hello world' in txt


pytest.mark.skip(reason="need to work on markdown collater class")
def test_collate_markdown_files_has_compile_marker_in_first_line():
    pass
    # txt = collate_markdown_files([ONE_OFF])
    # line = txt.splitlines()
    # assert line[0] == WRITHUB_PROJECT_HEADER
