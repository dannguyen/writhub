from pathlib import Path
import re
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
            self.src_dir = Path(src_dir).resolve()
        except TypeError as err:
            raise err
        else:
            if self.src_dir.is_file():
                raise WrithubIOError(f"src_dir must be a directory, not a file path: {self.src_dir}")
            if not self.src_dir.is_dir():
                raise WrithubIOError(f"src_dir is not an existing directory: {self.src_dir}")

        self.content_list = Helpers.get_content_list(self.src_dir, self.mode)

        # target path resolution
        _opath = Path(output_path).resolve() if output_path else self.src_dir
        self.target_path = Helpers.get_target_from_output_path(_opath, mode=self.mode)
        self.target_dir = self.target_path.parent
        self.target_basename = self.target_path.name
        if not self.target_dir.exists():
            self.target_dir.mkdir(exist_ok=True, parents=True)

        Helpers.self_check(self)


    def inner_collate(self) -> NoReturn:
        """produces a text file!"""
        collater = get_collater_type(self.mode)()
        ctxt = collater.collate(self.content_list,)
        self.collated_text = WRITHUB_PROJECT_HEADER + "\n" + ctxt
        self.target_path.write_text(self.collated_text)

    def publish(self)  -> NoReturn:
        """makes content!"""
        self.inner_collate()
        self.published = True

class Helpers(object):
    @staticmethod
    def self_check(self:Writhub):
        """self file check"""
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

