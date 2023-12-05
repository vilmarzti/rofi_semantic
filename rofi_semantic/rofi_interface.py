#!/home/martin/.cache/pypoetry/virtualenvs/rofi-semantic-vY6w7Ty4-py3.10/bin/python
import subprocess
import argparse
import sys

from subprocess import DEVNULL
from semantic import compare
from os import environ


def get_rofi_env():
    """
        return value: 0 - first call
                      1 - select an entry
                      2 - selected a custom entry
    """
    return {
            'return_value': environ['ROFI_RETV'],
            'info': envvion['ROFI_INFO'],
            'data': envviron['ROFI_DATA']
            }

def find_desktop_apps(query):
    app_infos, app_scores = compare(query)

    total = 0
    display_infos, display_scores = [], []
    for info, score in zip(app_infos, app_scores):
        display_infos.append(info)
        display_scores.append(score)
        if (total := total + score) > 100.0 or len(display_infos) > 7:
            break

    for info, score in zip(display_infos, display_scores):
        seperator = b'\x1f'.decode()
        null = b'\0'.decode()
        display_prompt = f'{info["name"]} {score:.2f}%'
        info_prompt = null + seperator.join(["icon", info['icon'], "info", info["icon"]])
        prompt = f'{display_prompt}, {info_prompt}'
        print(prompt, file=sys.stdout)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        prompt = b'\0prompt\x1f'.decode() + "NLP Search"
        print(prompt, file=sys.stdout)

    elif environ.get('ROFI_RETV') == "1":
        exec = environ.get('ROFI_INFO')
        subprocess.Popen(exec.split(" "), stdout=DEVNULL, stdin=DEVNULL, stderr=DEVNULL)

    else:
        parser = argparse.ArgumentParser(
            prog="Semantic Search Rofi Interface",
            description="Use semantic search to display desktop apps"
        )
        parser.add_argument('query')
        args = parser.parse_args()
        find_desktop_apps(args.query)
