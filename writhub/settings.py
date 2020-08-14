WRITHUB_PROJECT_HEADER = "<!----collated-by-writhub--- -->"

DEFAULT_COLLATED_STEM = "index"
DEFAULT_COLLATED_FILENAME = f"{DEFAULT_COLLATED_STEM}.md"  # TODO: deprecate

IGNORE_DIR_PATTERNS = (r"^_",)

IGNORE_FILE_PATTERNS = (
    DEFAULT_COLLATED_FILENAME,
    r"^_.+\.md",
    ".DS_Store",
)
