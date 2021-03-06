import click
from click.testing import CliRunner
from pathlib import Path
import pytest

from writhub.cli import main as maincli
from writhub.writhub import DEFAULT_COLLATED_FILENAME, WRITHUB_PROJECT_HEADER

runner = CliRunner()

SRC_DIR_ONEOFF = Path('./examples/oneoff/')


def test_main_hello():
    result = runner.invoke(maincli)
    assert result.exit_code == 0
    assert 'Welcome to writhub' in result.output
    assert '--help' in result.output


@pytest.mark.janky()
def test_specified_src_dir_and_default_output_path(tmpdir):
    src_dir = Path(tmpdir).joinpath('hey/you')
    src_dir.mkdir(exist_ok=True, parents=True)
    src_path = src_dir.joinpath('yo.md')
    src_path.write_text("# yo world")
    targpath = src_dir.joinpath(DEFAULT_COLLATED_FILENAME)


    result = runner.invoke(maincli, ['md', str(src_dir)])
    assert targpath.is_file()
    assert WRITHUB_PROJECT_HEADER in targpath.read_text()
    # assert 'xxx' in result.output


@pytest.mark.janky()
def test_specified_output_path(tmpdir):
    targ_dir = Path(tmpdir).joinpath('hey/you')
    targ_dir.mkdir(exist_ok=True, parents=True)
    targ_path = targ_dir.joinpath(DEFAULT_COLLATED_FILENAME)

    result = runner.invoke(maincli, ['md', str(SRC_DIR_ONEOFF), '-o', targ_path])
    assert targ_dir.is_dir()
    assert WRITHUB_PROJECT_HEADER in targ_path.read_text()
    assert '# hello world' in targ_path.read_text()



@pytest.mark.janky()
def test_specified_output_path_as_dir(tmpdir):
    targ_dir = Path(tmpdir).joinpath('hey/path')
    targ_dir.mkdir(exist_ok=True, parents=True)
    targ_path = targ_dir.joinpath(DEFAULT_COLLATED_FILENAME)

    result = runner.invoke(maincli, ['md', str(SRC_DIR_ONEOFF), '-o', targ_path])
    assert targ_dir.is_dir()
    assert WRITHUB_PROJECT_HEADER in targ_path.read_text()
    assert '# hello world' in targ_path.read_text()
