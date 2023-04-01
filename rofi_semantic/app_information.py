from os import path, environ
from glob import glob
from xdg.DesktopEntry import DesktopEntry
from xdg.Exceptions import ParsingError, DuplicateGroupError, DuplicateKeyError

import logging


def get_app_paths():
    paths = environ.get("XDG_DATA_DIRS").split(':')
    paths = [p for p in paths if path.exists(p)]

    file_paths = []
    for p in paths:
        file_paths.extend(glob(path.join(p, '**/*.desktop'), recursive=True))
    return file_paths


def get_raw_app_information():
    entries = []
    for file_path in get_app_paths():
        try:
            entry = DesktopEntry(file_path)
            if entry.getType() == 'Application':
                entries.append(entry)
        except (ParsingError, DuplicateGroupError, DuplicateKeyError):
            logging.warning(f'Parsing Error in file {file_path}')
    return entries


def get_app_information():
    # TODO: Select information and query man
    matches = get_raw_app_information()
    return matches


def list_app_names():
    entries = get_raw_app_information()
    return [e.getName() for e in entries]


if __name__ == '__main__':
    get_app_information()
