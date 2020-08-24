from pathlib import Path
import re
import subprocess
from typing import NoReturn, List as tList

from writhub.errors import *
from writhub.mylog import mylogger
from writhub.settings import *

from writhub.collaters import get_collater_type


class Writhub(object):
    """The object that handles file operations and logistics, i.e. project manager"""
    def __init__(self, mode="md", src_dir=None, output_path=None, **kwargs):
        """
        Attributes:
            target_path (Path): file path to compile project into

        Effects:
            Creates the parent directory of `target_path`
        """
        self.mode = mode
        self.collated_text = None
        self.published = False
        # source resolution
        try:
            self.src_dir = Path(src_dir).expanduser().resolve()
        except TypeError as err:
            raise err
        else:
            if self.src_dir.is_file():
                raise WrithubIOError(f"src_dir must be a directory, not a file path: {self.src_dir}")
            if not self.src_dir.is_dir():
                raise WrithubIOError(f"src_dir is not an existing directory: {self.src_dir}")

        self.content_list = Helpers.get_content_list(self.src_dir, self.mode)

        # target path resolution
        _opath = Path(output_path).expanduser().resolve() if output_path else self.src_dir
        self.target_path = Helpers.get_target_from_output_path(_opath, mode=self.mode)
        self.target_dir = self.target_path.parent
        self.target_basename = self.target_path.name
        if not self.target_dir.exists():
            self.target_dir.mkdir(exist_ok=True, parents=True)

        Helpers.self_check(self)


    def src_assets_dir(self) -> (Path, False):
        apath = self.src_dir.joinpath(DEFAULT_ASSETS_DIRNAME)
        if apath.is_dir():
            return apath
        else:
            return False

    def target_assets_dir(self) -> (Path, False):
        apath = self.src_assets_dir()
        if apath:
            tpath = self.target_dir.joinpath(apath.name)
            return tpath
        else:
            return False



    def __collate(self) -> NoReturn:
        """produces a text file!"""
        collater = get_collater_type(self.mode)()
        ctxt = collater.collate(self.content_list,)
        self.collated_text = WRITHUB_PROJECT_HEADER + "\n" + ctxt
        self.target_path.write_text(self.collated_text)
        collater.insert_toc(self.target_path)

    def publish(self)  -> NoReturn:
        """makes content!"""
        self.__collate()
        assetsdir = self.src_assets_dir()
        if assetsdir:
            Helpers.sync_subdir(self.src_dir, assetsdir, self.target_dir)
        self.published = True


class Helpers(object):
    @staticmethod
    def self_check(self:Writhub):
        """self file check"""
        mylogger.debug(f"src_dir: {self.src_dir}")
        mylogger.debug(f"target_dir: {self.target_dir}")
        mylogger.debug(f"target_path: {self.target_path}")

        pass

    @staticmethod
    def get_content_list(srcdir:Path, mode:str) -> tList[Path]:
        """returns a list of alphabetically sorted source files that meet selection criteria"""
        mypaths = []
        for path in srcdir.glob(f"*.{mode}"):
            if any(re.match(rx, path.name) for rx in IGNORE_FILE_PATTERNS):
                mylogger.debug(f'{path} based on `IGNORE_FILE_PATTERNS`',  label="Ignoring")
            elif any(re.match(rx, path.parent.name) for rx in IGNORE_DIR_PATTERNS):
            # TODO: right now, only the parent directory is checked for ignored dir patterns
                mylogger.debug(f'{path} based on `IGNORE_DIR_PATTERNS`',  label="Ignoring")
            else:
                mypaths.append(path)

        # TODO: decide whether to sort by
        return sorted(mypaths)



    @staticmethod
    def get_target_from_output_path(output_path:Path, mode:str) -> Path:
        """Generates a target path, given an ostensible output path (file or directory)
        and a mode (i.e. file extension)

        Returns:
            A file path, ostensibly for Writhub to compile stuff to a single file
        """
        def _do_dir(xpath:Path) -> bool:
            if xpath.name == f"{xpath.stem}.{mode}" or xpath.is_file():
                # automatically assume the target is meant to be a file
                booldir = False
            elif xpath.is_dir() or (  # if the output path is an existing directory
                not xpath.is_file() # or if output path is not file, but seems to be a dirname
                and ((xpath.name[-1] == "/") or (xpath.name == xpath.stem))
            ):
                booldir = True
            elif re.search(r"\.\w{1,10}$", xpath.name):
                # if output path has some kind of file extension
                # then assume it's a valid destination
                booldir = False
            else:
                raise WrithubValueError(f"Unexpected type of output path: {xpath}")
            return booldir

        if _do_dir(output_path):
            t_dir = output_path
            t_basename = f"{DEFAULT_COLLATED_STEM}.{mode}"
        else:
            t_dir = output_path.parent
            t_basename = output_path.name

        return t_dir.joinpath(t_basename)


    @staticmethod
    def sync_subdir(src_dir:Path, src_subdir:Path, target_dir:Path, ):
        """
        contents of `src_subdir` is rsynced to `target_dir`/subdir, where
            subdir is src_subdir relative to src_dir

        Example
        -------
        src_dir:    /tmp/foo/home
        src_subdir: /tmp/foo/home/assets or ./assets
        target_dir: ./dest/

        Contents of /tmp/foo/home/assets are
            synced to: dest/assets
        """

        reldir = src_subdir.relative_to(src_dir)
        _from = str(src_subdir.joinpath(src_subdir)).rstrip('/') + '/'
        _to = str(target_dir.joinpath(reldir)).rstrip('/')


        if _from == _to + '/':
            mylogger.debug(f"_from and _to are the same: {_from}", label="skip rSyncing")
        else:
            mylogger.debug(f"{_from} to {_to}", label="rSyncing")
            proc = subprocess.call(['rsync', '-a', '-m', _from, _to])
            return proc


#        proc = subprocess.call(['rsync', '-a', '-m', '--exclude', RSYNC_EXCLUDED, src, target])
#             pubstr = str(_pubdir.joinpath(subdir.name)).rstrip('/')
