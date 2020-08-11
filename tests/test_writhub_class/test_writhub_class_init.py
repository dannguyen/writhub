from pathlib import Path
from writhub.writhub import Writhub

import pytest


def test_basic_init_of_writhub(tmpdir):
    srcdir = Path(tmpdir).joinpath('mysrc')
    srcdir.mkdir(exist_ok=True, parents=True)
    targetdir = Path(tmpdir).joinpath('targdir')

    hub = Writhub(src_dir=srcdir,)
    assert hub.src_dir == Path(srcdir)
    assert hub.mode == 'md'
    assert hub.target_path == Path(srcdir).joinpath('index.md')



def test_init_writhub_with_target_path(tmpdir):
    assert pytest.fail('need to write this')
