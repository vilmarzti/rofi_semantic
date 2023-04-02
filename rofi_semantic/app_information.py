from os import path, environ
from glob import glob
from xdg.DesktopEntry import DesktopEntry
from xdg.Exceptions import ParsingError, DuplicateGroupError, DuplicateKeyError

from semantic_transformer import SemanticTransformer

import re
import logging
import subprocess


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
            if entry.getType() == 'Application' and entry.getExec() is not None and entry.getIcon() is not None:
                entries.append(entry)
        except (ParsingError, DuplicateGroupError, DuplicateKeyError):
            logging.warning(f'Parsing Error in file {file_path}')
    return entries


def get_whatis_entry(name, command):
    whatis_cmd = subprocess.run(['whatis', '-l', command], capture_output=True)

    description = None
    if whatis_cmd.returncode == 0:
        description = re.sub(r'^.*-', f'{name}:', whatis_cmd.stdout.decode('utf-8'))
        description = re.sub(r'(\n.*)*', '', description)

    return description


def get_app_description(xdg_entry):
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
