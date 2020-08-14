
from writhub.collaters.collater import TextCollater
from writhub.collaters.md import MarkdownCollater



def get_collater_type(mode:str=None) -> type:
    if mode == 'md':
        return MarkdownCollater
    else:
        return TextCollater

