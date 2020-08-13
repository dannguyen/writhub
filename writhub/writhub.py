from pathlib import Path
import re

from writhub.errors import *


COMPILE_HEADER = '<!----compiled-by-writhub--- -->'
DEFAULT_COLLATED_STEM = 'index'
DEFAULT_COLLATED_FILENAME = f'{DEFAULT_COLLATED_STEM}.md' # TODO: deprecate


IGNORE_DIR_PATTERNS = (
    r'^_',
)

IGNORE_FILE_PATTERNS = (
    DEFAULT_COLLATED_FILENAME,
    r'^_.+\.md',
    '.DS_Store',
)



class Writhub():
    def __init__(self, mode='md', src_dir=None, output_path=None):
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
    def self_check(self):
        """self file check"""
        if not self.src_dir.is_dir():
            raise WrithubIOError(f"src_dir is not a directory: {self.src_dir}")


    @staticmethod
    def get_source_paths(srcdir, mode):
        return sorted(srcdir.glob(f'*.{mode}'))



    @staticmethod
    def get_target_from_output_path(output_path, mode):

        def _do_dir(xpath):
            if xpath.is_dir():
                # if the output path is an existing directory,
                # set target_path to outdir/index.ext
                booldir = True
            elif xpath.is_file() or re.search(r'\.{}$'.format(mode), xpath.name):
                # if output path is an existing file, or the name has expected file extension,
                # then assume it's a valid destination and make its parent directory if necessary
                booldir = False
            elif xpath.name == xpath.stem:
                # if output_path is not file, and also seems to be a directory name
                # then assume it's a target directory
                booldir = True
            elif re.search(r'\.\w{1,10}$', xpath.name):
                # assume it's a file path of weird file extension
                booldir = False
            else:
                raise WrithubValueError(f"Unexpected type of output path: {xpath}")
            return booldir


        def _make_target(xpath):
            if _do_dir(xpath):
                _basename = f'{DEFAULT_COLLATED_STEM}.{mode}'
                _dir = xpath
            else:
                _basename = xpath.name
                _dir = xpath.parent

            tpath = _dir.joinpath(_basename)
            return tpath


        return _make_target(output_path)
