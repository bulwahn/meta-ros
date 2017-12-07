#!/usr/bin/env python3
__author__ = "Johannes Schrimpf"
__copyright__ = "Copyright 2017, Blueye Robotics AS"
__credits__ = ["Johannes Schrimpf"]
__license__ = "GPLv3"

import os
import urllib.request
import sys
from distutils.version import LooseVersion
import yaml

BASE_DIR = "../recipes-ros"
DEBUG = True
EXCLUDE = ["packagegroups"]
DISTRO = "indigo"
DIST_FILE = "https://raw.githubusercontent.com/ros/rosdistro/master/" + DISTRO+ "/distribution.yaml"



def check_version(package, silent=False, details=False):
    package_dir = os.path.join(BASE_DIR, package)
    versions = []
    if not silent:
        if details:
            print(package)
    try:
        dist_ver = dist_raw["repositories"][package.replace("-", "_")]["release"]["version"]
        dist_ver = dist_ver.split("-")[0]
    except KeyError:
        dist_ver = ""
    for filename in os.listdir(package_dir):
        if filename.endswith(".bb"):
            version = filename.split("_")[1].split(".bb")[0]
            if version not in versions:
                versions.append(version)
    if len(versions) > 1:
        raise Exception("Multiple versions per package not supported at this time")

    match = dist_ver == version
    if dist_ver == "":
        pre = post = ""
        mid = "   "
    elif version == "git":
        mid = "   "
        pre = post = ""
    else:
        pre = '\033[92m' if match else '\033[91m'
        post = '\033[0m'
        if match:
            mid = " = "
        else:
            assert LooseVersion(version) != LooseVersion(dist_ver)
            if LooseVersion(version) > LooseVersion(dist_ver):
                mid = " > "
            elif LooseVersion(dist_ver) > LooseVersion(version):
                mid = " < "

    if not details and not silent:
        print(package.ljust(35) + pre + version.ljust(10) + mid + dist_ver.ljust(10) + post)
    return match, version, dist_ver


def print_header():
    print("\033[1m\033[4m" + "package".ljust(35) +
          "layer".ljust(13) + "distro".ljust(10) + '\033[0m')

def print_help():
    print("Usage:")
    print("List all versions:                  ./check_versions.py list")
    print("List all versions that don't match: ./check_versions.py mismatch")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print_help()
    else:
        if sys.argv[1] == "list":
            dist_raw = yaml.load(urllib.request.urlopen(DIST_FILE).read())
            packages = [x for x in os.listdir(BASE_DIR) if x not in EXCLUDE]
            print_header()
            for package in packages:
                check_version(package)
        elif sys.argv[1] == "mismatch":
            dist_raw = yaml.load(urllib.request.urlopen(DIST_FILE).read())
            packages = [x for x in os.listdir(BASE_DIR) if x not in EXCLUDE]
            print_header()
            for package in packages:
                if not check_version(package, silent=True)[0]:
                    match, version, dist_ver = check_version(package)
        else:
            print_help()
