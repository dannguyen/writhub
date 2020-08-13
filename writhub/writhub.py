from pathlib import Path
import re

from writhub.errors import *


COMPILE_HEADER = "<!----compiled-by-writhub--- -->"
DEFAULT_COLLATED_STEM = "index"
DEFAULT_COLLATED_FILENAME = f"{DEFAULT_COLLATED_STEM}.md"  # TODO: deprecate


IGNORE_DIR_PATTERNS = (r"^_",)

IGNORE_FILE_PATTERNS = (
    DEFAULT_COLLATED_FILENAME,
    r"^_.+\.md",
    ".DS_Store",
)


class Writhub:
    def __init__(self, mode="md", src_dir=None, output_path=None):
        self.mode = mode
        self.src_dir = Path(src_dir).resolve()
        if not self.src_dir.is_dir():
            raise WrithubIOError(f"src_dir is not a directory: {self.src_dir}")

        self.src_paths = Helpers.get_source_paths(self.src_dir, self.mode)

        _opath = Path(output_path).resolve() if output_path else self.src_dir
        self.target_path = Helpers.get_target_from_output_path(_opath, mode=self.mode)
        self.target_dir = self.target_path.parent
        self.target_basename = self.target_path.name

        if not self.target_dir.exists():
            self.target_dir.mkdir(exist_ok=True, parents=True)

        Helpers.self_check(self)


class Helpers(object):
    @staticmethod
    def self_check(self:Writhub):
        """self file check"""
        pass

    @staticmethod
    def get_source_paths(srcdir:Path, mode:str) -> list:
        return sorted(srcdir.glob(f"*.{mode}"))

    @staticmethod
    def get_target_from_output_path(output_path:Path, mode:str) -> Path:
        """

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

