from writhub.writhub import Writhub
from writhub.errors import *

from pathlib import Path
import pytest


@pytest.fixture
def targetdir(tmpdir):
    xdir = Path(tmpdir).joinpath('testoutput')
    return xdir


@pytest.fixture
def content(tmpdir):
    ct = {'dir': Path(tmpdir).joinpath('testsrc'), 'paths': []}
    ct['dir'].mkdir(exist_ok=True, parents=True)

    for bname in ('000-hello.md', '100-world.md', '200.md',
                '200-stuff/320-alpha.md', '200-stuff/999-omega.md',
                '400-zeta.md'):

        p = ct['dir'].joinpath(bname)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"# {bname}\n\n\n")


    return ct


@pytest.fixture
def hub(content, targetdir):
    return Writhub(mode='md', src_dir=content['dir'], output_path=targetdir)

def test_writhub_content_list_first_hello(hub):
    fpath = hub.content_list[0]
    assert fpath.name == '000-hello.md'

@pytest.mark.skip(reason="Need to do this with a different src_dir/targetdir fixture setup")
def target_path_not_in_file_inventory():
    pass

@pytest.mark.skip(reason="Need to do this with a different src_dir/targetdir fixture setup")
def test_default_output_filename_is_in_ignore_list():
    pass
