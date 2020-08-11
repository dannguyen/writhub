from pathlib import Path



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
        self.ext = f'.{self.mode}'
        self.basename = f'{DEFAULT_COLLATED_STEM}{self.ext}'

        self.src_dir = Path(src_dir)

        if not self.src_dir.is_dir():
            raise ValueError(f"src_dir: {self.src_dir} does not exist!")

        if not output_path:
            self.target_dir = self.src_dir
            self.target_path = self.src_dir.joinpath(self.basename)
        else:
            output_path = Path(output_path)
            if self.ext in output_path.name:
                self.target_path = output_path
            else:
                self.target_path = output_path.joinpath(self.basename)

            self.target_dir = self.target_path.parent
