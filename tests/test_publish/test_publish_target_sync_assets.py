from writhub.writhub import Writhub
from writhub.errors import *
from writhub.settings import ASSETS_DIR_PATTERNS

from pathlib import Path
import pytest


@pytest.fixture
def targetdir(tmpdir):
    xdir = Path(tmpdir).joinpath('targetouts')
    return xdir

@pytest.fixture
def content(tmpdir):
    ct = {'dir': Path(tmpdir).joinpath('testsrc'), 'paths': []}
    ct['dir'].mkdir(exist_ok=True, parents=True)

    for bname in ('assets/hello.jpg',
                'assets/dummy.md',
                'assets/_keepme.md',
                '000-hello.md',
                '100-world.md',):

        p = ct['dir'].joinpath(bname)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"# {bname}\nhey\n\n")
    return ct


@pytest.fixture
def hub(content, targetdir):
    hub = Writhub(mode='md', src_dir=content['dir'], output_path=targetdir)
    hub.publish()
    return hub


@pytest.fixture
def assetdir(hub):
    return hub.target_dir.joinpath('assets')



def test_has_src_and_target_assets_dir(hub, assetdir):
    assert hub.src_assets_dir() == hub.src_dir.joinpath('assets')
    assert hub.target_assets_dir() == assetdir

def test_assets_copied_over(hub, assetdir):
    assert assetdir.is_dir()

def test_has_no_assets_dirs(tmpdir):
    sdir = Path(tmpdir).joinpath('testnoassets')
    sdir.mkdir(exist_ok=True, parents=True)
    tdir = Path(tmpdir).joinpath('xxwhatev')
    for bname in ('000-hello.md', '100-world.md',):
        p = sdir.joinpath(bname)
        p.write_text(f"# {bname}\nhey\n\n")

    xhub = Writhub(mode='md', src_dir=sdir, output_path=tdir)
    assert xhub.src_assets_dir() is False
    assert xhub.target_assets_dir() is False
