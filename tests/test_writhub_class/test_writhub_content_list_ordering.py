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

    for bname in (
                'assets/asset.md',
                'ignore.me', 'not.content.file',
                '000-hello.md',
                '100-world.md', '400-alpha.md',
                '200-stuff/320-alpha.md', '200-stuff/999-omega.md',
                '200.md',
                '400-zeta_zed.md',
                'index.md',
                '_500-what.md',
                '_drafts/draft.md',):

        p = ct['dir'].joinpath(bname)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"# {bname}\n\n\n")
    return ct


@pytest.fixture
def hub(content, targetdir):
    return Writhub(mode='md', src_dir=content['dir'], output_path=targetdir)

@pytest.fixture
def clist(hub):
    return hub.content_list


def test_content_list_ignores_files_without_proper_mode_eg_md(clist):
    assert all('ignore.me' not in c.name for c in clist)
    assert all('not.content.file' not in c.name for c in clist)


def test_content_list_ignores_file_patterns(clist):
    assert all('index.md' not in c.name for c in clist)
    assert all('_500-what.md' not in c.name for c in clist)

def test_content_list_ignores_dir_patterns(clist):
    assert all('_drafts/draft.md' not in str(c) for c in clist)
    assert all('assets/asset.md' not in str(c) for c in clist)



@pytest.mark.skip(reason="Need to do this with a different src_dir/targetdir fixture setup")
def test_content_list_ignores_target_path_explicitly(hub):
    pass


#### Sorting

def test_sort_content_list_first_and_last(clist):
    assert clist[0].name == '000-hello.md'
    assert clist[-1].name == '400-zeta_zed.md'

def test_sort_content_list_subfolder_sort(clist):
    assert clist[-2].name == '400-alpha.md'
    assert clist[1].name == '100-world.md'
    assert clist[2].name == '200.md'

