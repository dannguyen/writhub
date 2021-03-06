WRITHUB_PROJECT_HEADER = "<!----collated-by-writhub--- -->"

DEFAULT_COLLATED_STEM = "index"
DEFAULT_COLLATED_FILENAME = f"{DEFAULT_COLLATED_STEM}.md"  # TODO: deprecate

DEFAULT_ASSETS_DIRNAME = 'assets'

ASSETS_DIR_PATTERNS = (rf'\b{DEFAULT_ASSETS_DIRNAME}\b',)

IGNORE_DIR_PATTERNS = (r"^_", *ASSETS_DIR_PATTERNS)

IGNORE_FILE_PATTERNS = (
    DEFAULT_COLLATED_FILENAME,
    r"^_.+\.md",
    ".DS_Store",
)
