from ripgrepy import Ripgrepy
from constants import APPLICATION_PATH
import subprocess


def get_description():
    rg = Ripgrepy('(^Exec=([\w-]*))|(^Name=.*)|(^GenericName=.*)', APPLICATION_PATH)
    results = rg.only_matching().json().run().as_dict

    matches = {}
    for m in results:
        file_path = m['data']['path']['text']
        if file_path in matches:
            matches[file_path].append(m['data']['submatches'])
        else:
            matches[file_path] = [(m['data']['submatches'])]
    return matches


def list_apps():
    """List desktop apps in the APPLICATION_PATH folder.

    Returns:
        Array with desktop apps.
    """
    command = 'ls ' + APPLICATION_PATH
    ls_output = subprocess.check_output(command, shell=True)

    program_list = ls_output.decode().split('\n')

    return program_list


def list_app_names():
    program_list = list_apps()
    # remove desktop postfix
    program_list = [app_basename.replace('.desktop', '') for app_basename in program_list]
    return program_list


if __name__ == '__main__':
    get_description()
