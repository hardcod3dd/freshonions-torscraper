import re

REGEX = re.compile(
    "\b[a-zA-Z0-9_.+-]{1,50}@[a-zA-Z0-9-]{1,50}\.[a-zA-Z0-9-.]{1,50}[a-zA-Z0-9]\b",
    re.MULTILINE,
)
REGEX_ALL = re.compile(
    "^[a-zA-Z0-9_.+-]{1,50}@[a-zA-Z0-9-]{1,50}\.[a-zA-Z0-9-.]{1,50}[a-zA-Z0-9]$",
    re.MULTILINE,
)
