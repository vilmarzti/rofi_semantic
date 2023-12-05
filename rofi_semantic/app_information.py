from os import path, environ
<<<<<<< HEAD
from glob import glob
from xdg.DesktopEntry import DesktopEntry
from xdg.Exceptions import ParsingError, DuplicateGroupError, DuplicateKeyError

from semantic_transformer import SemanticTransformer
=======

from glob import glob
from xdg.BaseDirectory import xdg_data_dirs
from xdg.DesktopEntry import DesktopEntry
from xdg.Exceptions import ParsingError, DuplicateGroupError, DuplicateKeyError

#from semantic_transformer import SemanticTransformer
>>>>>>> a8eaea6 (Docs)

import re
import logging
import subprocess


def get_app_paths():
<<<<<<< HEAD
    paths = environ.get("XDG_DATA_DIRS").split(':')
    paths = [p for p in paths if path.exists(p)]

    file_paths = []
    for p in paths:
=======
    """ Returns all entries from the given xdg paths
    """
    file_paths = []
    for p in xdg_data_dirs:
>>>>>>> a8eaea6 (Docs)
        file_paths.extend(glob(path.join(p, '**/*.desktop'), recursive=True))
    return file_paths


def get_raw_app_information():
<<<<<<< HEAD
=======
    """Parse all the xdg entries.
    """
>>>>>>> a8eaea6 (Docs)
    entries = []
    for file_path in get_app_paths():
        try:
            entry = DesktopEntry(file_path)
            if entry.getType() == 'Application' and entry.getExec() is not None and entry.getIcon() is not None:
                entries.append(entry)
        except (ParsingError, DuplicateGroupError, DuplicateKeyError):
            logging.warning(f'Parsing Error in file {file_path}')
    return entries


def get_whatis_entry(name, command):
<<<<<<< HEAD
=======
    """ Use 'whatis <command>' to get a natural language description.

    Args:
        name: Name of entry
        command: Command to look up
    """
>>>>>>> a8eaea6 (Docs)
    whatis_cmd = subprocess.run(['whatis', '-l', command], capture_output=True)

    description = None
    if whatis_cmd.returncode == 0:
        description = re.sub(r'^.*-', f'{name}:', whatis_cmd.stdout.decode('utf-8'))
        description = re.sub(r'(\n.*)*', '', description)

    return description


def get_app_description(xdg_entry):
<<<<<<< HEAD
=======
    """Check 'whatis' or xdg entry comment for natural language description

    Args:
        xdg_entry: Parsed xdg entry
    """
>>>>>>> a8eaea6 (Docs)
    name = xdg_entry.getName()
    exec_command = re.match(r'\S*', xdg_entry.getExec())

    if exec_command is not None:
        description = get_whatis_entry(name, exec_command.string)

    if description is None and (comment := xdg_entry.getComment()) != '':
        description = f'{name}: {comment}'

    if description is None:
        description = f'{name}'

    return description


def get_app_information():
<<<<<<< HEAD
=======
    """get_app_information.
    """
>>>>>>> a8eaea6 (Docs)
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
<<<<<<< HEAD
=======


get_raw_app_information()
>>>>>>> a8eaea6 (Docs)
