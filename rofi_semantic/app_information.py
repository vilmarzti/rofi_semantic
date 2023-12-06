from os import path, environ

from glob import glob
from xdg.BaseDirectory import xdg_data_dirs
from xdg.DesktopEntry import DesktopEntry
from xdg.Exceptions import ParsingError, DuplicateGroupError, DuplicateKeyError

#from semantic_transformer import SemanticTransformer

import re
import logging
import subprocess


def get_app_paths():
    """ Returns all entries from the given xdg paths
    """
    file_paths = []
    for p in xdg_data_dirs:
        file_paths.extend(glob(path.join(p, '**/*.desktop'), recursive=True))
    return file_paths


def get_raw_app_information():
    """Parse all the xdg entries.
    """
    entries = []
    for file_path in get_app_paths():
        try:
            entry = DesktopEntry(file_path)
            if entry.getType() == 'Application' and entry.getExec() is not None and entry.getIcon() is not None:
                entries.append(entry)
        except (ParsingError, DuplicateGroupError, DuplicateKeyError):
            logging.warning(f'Parsing Error in file {file_path}')
    return entries


def get_app_information():
    """get_app_information.
    """
    entries = get_raw_app_information()

    encoder = SemanticTransformer()
    processed_entries = []
    for entry in entries:
        description = get_app_description(entry)
        embedding = encoder.encode([description])[0].tolist()
        processed_entries.append({
            'name': entry.getName(),
            'icon': entry.getIcon(),
            'exec': entry.getExec(),
            'desc': description,
            'embedding': embedding
        })
    return processed_entries
