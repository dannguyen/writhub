from writhub.writhub import Writhub
from writhub.writhub import WRITHUB_PROJECT_HEADER
from writhub.collaters.collater import DEFAULT_COLLATION_MARKER
from writhub.errors import *

from pathlib import Path
import pytest


@pytest.fixture
def srcdir(tmpdir):
    xdir = Path(tmpdir).joinpath('testsrc')
    xdir.mkdir(exist_ok=True, parents=True)
    return xdir

@pytest.fixture
def content(srcdir):
    f1 = srcdir.joinpath('000-hello.md')
    f1.write_text("# Hello\n\n## lorem\n\nipsum")
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

def test_publish_has_expected_attrs(hub):
    assert type(hub.collated_text) is str
    assert hub.published is True

    assert hub.mode == 'md'
    assert hub.src_dir == hub.target_dir
    assert hub.target_path.name == 'index.md'

def test_publish_has_expected_target_index_md(hub):
    assert hub.target_path.exists()
    txt = hub.target_path.read_text()
    assert '# Hello' in txt
    assert len(txt) > 10

def test_publish_has_meta_header_in_first_line(hub):
    txt = hub.target_path.read_text()
    line = txt.splitlines()[0]
    assert len(WRITHUB_PROJECT_HEADER) == len(line)


def test_publish_has_default_collation_markers_on_each_page(hub):
    with open(hub.target_path) as targ:
        for cpath in hub.content_list:
            opener = next(line for line in targ if str(cpath) in line )
            assert f'<!---{DEFAULT_COLLATION_MARKER}' in opener

            closer = next(line for line in targ if str(cpath) in line )
            assert f'<!---/{DEFAULT_COLLATION_MARKER}' in closer


@pytest.mark.skip(reason="Need to rework writhub and its publish")
def test_publish_page_has_toc():
    pass


@pytest.mark.skip(reason="Need to rework writhub and its publish")
def test_publish_synced_assets():
    pass

