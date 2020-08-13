from typing import List as tList
from writhub.writhub import WRITHUB_PROJECT_HEADER
from writhub.mylog import mylogger

from pathlib import Path

DEFAULT_COLLATION_MARKER = 'writhub-collated-page'

class TextCollater(object):
    """Manages the text compilation and transformation of a writhub project"""

    def collate_text(
        src_paths:tList[Path],
        make_mark:bool = True,
        collation_marker:str = DEFAULT_COLLATION_MARKER,
        **kwargs) -> str:
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


    def insert_toc(src_path:Path):
        mylogger.info(f"Inserting TOC into {src_path}")
        pass
