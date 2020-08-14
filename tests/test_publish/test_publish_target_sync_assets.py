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


def test_assets_copied_over(hub, assetdir):
    assert assetdir.is_dir()
