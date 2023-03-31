from functools import reduce
from ripgrepy import Ripgrepy
from os import path, environ


def get_app_paths():
    paths = environ.get("XDG_DATA_DIRS").split(':')
    paths = [p for p in paths if path.exists(p)]
    return paths


def get_raw_app_information():
    matches = []
    for desktop_path in get_app_paths():
        rg = Ripgrepy(r'Exec=([^\s\n]*)|Name=(.*)|GenericName=(.*)', desktop_path)
        results = rg.glob('*.desktop').only_matching().json().run().as_dict
        matches += results
    return matches


def map_match(match):
    match_type, submatch = match['data']['submatches'][0]['match'].split('=')
    return {
            'path': match['data']['path'],
            'type': match_type,
            'match': submatch
    }


def reduce_matches(match_list, new_match):
    pass


def get_app_information():
    matches = get_raw_app_information()
    matches = map(map_match, matches)
    matches = reduce(reduce_matches, matches, [])


def list_app_names():
    pass
    """
    program_list = list_apps()
    # remove desktop postfix
    program_list = [app_basename.replace('.desktop', '') for app_basename in program_list]
    return program_list
    """


if __name__ == '__main__':
    get_app_information()
