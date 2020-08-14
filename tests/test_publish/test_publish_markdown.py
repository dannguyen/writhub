from writhub.writhub import Writhub
from writhub.writhub import WRITHUB_PROJECT_HEADER
from writhub.collaters.collater import DEFAULT_COLLATION_MARKER
from writhub.collaters.md import toc_marker
from writhub.errors import *

from pathlib import Path
import pytest
import re

@pytest.fixture
def srcdir(tmpdir):
    xdir = Path(tmpdir).joinpath('testsrc')
    xdir.mkdir(exist_ok=True, parents=True)
    return xdir

@pytest.fixture
def content(srcdir):
    f1 = srcdir.joinpath('000-hello.md')
    f1.write_text(f"{toc_marker}\n\n# Hello\n\n## lorem\n\nipsum")
    f2 = srcdir.joinpath('999-omega.md')
    f2.write_text("## End\n\nThe end\n\n### Omega\nalpha")

    return {'dir': srcdir, 'paths': [f1, f2]}

@pytest.fixture
def _writhub(content):
    """output_path not defined, i.e. target_dir is the same as src_dir"""
    return Writhub(mode='md', src_dir=content['dir'],)

@pytest.fixture
def hub(_writhub):
    _writhub.publish()
    return _writhub


@pytest.fixture
def pubtext(hub):
    return hub.target_path.read_text()

def test_publish_has_expected_attrs(hub):
    assert type(hub.collated_text) is str
    assert hub.published is True

    assert hub.mode == 'md'
    assert hub.src_dir == hub.target_dir
    assert hub.target_path.name == 'index.md'

def test_publish_markdown_has_meta(pubtext):
    line = pubtext.splitlines()[0]
    assert WRITHUB_PROJECT_HEADER == line
    assert re.search(f'<!---{DEFAULT_COLLATION_MARKER}.+?000-hello.md', pubtext)



def test_publish_file_has_markdown_toc(pubtext):
    assert '- [Hello](#hello)' in pubtext
