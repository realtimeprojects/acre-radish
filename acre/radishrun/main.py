import re
import os
import sys
import logging as log

from acre.path import AcrePath


def main():
    """ invoke a test run """

    log.debug(f"arguments: {sys.argv}")

    userdata = _read_userdata()

    cmd = f'PYTHONPATH=src/ radish -b ./steps -b {AcrePath.steps()} {userdata} {" ".join(sys.argv[1:])}'
    log.info("running: {cmd}")
    os.system(cmd)


def _read_userdata():
    if not os.path.exists("etc/user.data"):
        return ""

    userdata = []
    for line in open("etc/user.data", "r").readlines():
        if not re.match(r"\w+=.*", line):
            log.bailout(f'invalid user data: {line}', 3)
        userdata.append(f'-u "{line.strip()}"')
    return " ".join(userdata)


if __name__ == "__main__":
    ec = main()
    sys.exit(ec)
