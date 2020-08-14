from writhub.mylog import mylogger

from pathlib import Path
from typing import List as tList

DEFAULT_COLLATION_MARKER = 'writhub-collated-page'

class TextCollater(object):
    """Manages the text compilation and transformation of a writhub project"""


    def __init__(self, make_mark:bool=True, collation_marker:str=DEFAULT_COLLATION_MARKER,
        **kwargs):

        self.make_mark = make_mark
        self.collation_marker = collation_marker


    def collate(self, src_paths:tList[Path]) -> str:
        txt = self.collate_text(src_paths, self.make_mark, self.collation_marker)
        return txt


    def insert_toc(filepath:Path) -> Path:
        mylogger.info(f"Inserting TOC into {filepath}")
        return filepath
        pass

    # TODO: move page_collation markup into its own method
    @staticmethod
    def collate_text(
        src_paths:tList[Path],
        make_mark:bool,
        collation_marker:str
        ) -> str:
        """
        Arguments:
            src_paths (List[Path])

        Returns:
            returns a text string consisting of the concatenated content of
                valid source text files in `src_paths`

        TODO: have an option to not insert file break comments
        TODO: ignore_output_filename edge cases handled/tested
        """
        # ignore_output_filename=DEFAULT_COLLATED_FILENAME, ):
        if not all(issubclass(type(p), Path) for p in src_paths):
            raise ValueError(f"Expected `src_paths` to be a collection of file paths")


        txt = ""
        for path in src_paths:
            pagetxt = path.read_text()
            if make_mark:
                pagetxt = f"\n<!---{collation_marker} {path} -->\n" + pagetxt + f"\n<!---/{collation_marker} {path} -->\n"
            txt += pagetxt

        return txt


