from pathlib import Path
import pytest

from writhub.writhub import Writhub
from writhub.errors import *
from writhub import __version__

def test_version():
    assert __version__ == '0.0.1'



@pytest.fixture
def srcdir(tmpdir):
    srcdir = Path(tmpdir).joinpath('mysrc')
    srcdir.mkdir(exist_ok=True, parents=True)
    srcdir.joinpath('000-hello.md').write_text('# hey')
    return srcdir


@pytest.fixture
def targetdir(tmpdir):
    targetdir = Path(tmpdir).joinpath('targdir')
    return targetdir


def test_basic_init_of_writhub(srcdir):
    hub = Writhub(src_dir=srcdir,)
    assert hub.src_dir == Path(srcdir)
    assert hub.mode == 'md'
    assert hub.target_basename == 'index.md'
    assert hub.target_path == Path(srcdir).joinpath('index.md')


def test_init_writhub_with_output_path_creates_output_parent(srcdir, targetdir):
    tpath = targetdir.joinpath('subby', 'index.md')
    hub = Writhub(src_dir=srcdir, output_path=tpath)
    assert hub.target_path == tpath
    assert hub.target_dir == targetdir.joinpath('subby')
    assert hub.target_dir.is_dir() and hub.target_dir.exists()

def test_init_writhub_with_output_path_as_nonindexmd(srcdir, targetdir):
    bname = 'whateverdude.txt'
    tpath = targetdir.joinpath('bubdir', bname)
    hub = Writhub(src_dir=srcdir, output_path=tpath)
    assert hub.target_basename == bname
    assert hub.target_path == tpath

def test_init_writhub_with_output_path_as_dir(srcdir, targetdir):
    hub = Writhub(src_dir=srcdir, output_path=targetdir)
    assert hub.target_basename == 'index.md'
    assert hub.target_path == Path(targetdir, 'index.md')

def test_writhub_src_dir_can_be_the_same_as_output_path_dir(srcdir, targetdir):
    hub = Writhub(src_dir=srcdir, output_path=srcdir.joinpath('hey.md'))
    assert hub.src_dir == hub.target_dir


#### error conditions

@pytest.fixture
def empty_srcdir(tmpdir):
    srcdir = Path(tmpdir).joinpath('mysrc')
    srcdir.mkdir(exist_ok=True, parents=True)
    return srcdir

@pytest.fixture
def nonexistent_dir(tmpdir):
    xdir = Path(tmpdir).joinpath('asdk')
    if xdir.is_dir():
        raise ValueError("Did not expect nonexistent_dir fixture to have an existing directory")
    return xdir



def test_writhub_init_with_nonexistent_src_dir(nonexistent_dir):
    with pytest.raises(WrithubIOError) as err:
        Writhub(src_dir=nonexistent_dir)

    assert str(nonexistent_dir) in str(err.value)
    assert str('is not an existing directory') in str(err.value)


def test_writehub_init_src_cannot_be_list(tmpdir):
    with pytest.raises(TypeError) as err2:
        Writhub(src_dir=['/tmp/foo.md'])

    assert str('expected str') in str(err2.value)
    assert str('not list') in str(err2.value)


def test_writehub_init_src_cannot_be_existing_file_path(tmpdir):
    srcfilepath = Path(tmpdir).joinpath('000-hello.md')
    srcfilepath.parent.mkdir(exist_ok=True, parents=True)
    srcfilepath.write_text("bad bad bad")

    with pytest.raises(WrithubIOError) as err:
        Writhub(src_dir=srcfilepath)

    assert str(srcfilepath) in str(err.value)
    assert str('must be a directory, not a file path') in str(err.value)

