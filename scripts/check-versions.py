#!/usr/bin/env python3
__author__ = "Johannes Schrimpf"
__copyright__ = "Copyright 2017, Blueye Robotics AS"
__credits__ = ["Johannes Schrimpf"]
__license__ = "GPLv3"

"""
check-version.py is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

check-version.py is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See <https://www.gnu.org/licenses/gpl-3.0.html> for full license text.
"""

import os
import urllib.request
import sys
import re
import hashlib
from distutils.version import LooseVersion
import yaml

BASE_DIR = "../recipes-ros"
DEBUG = True
EXCLUDE = ["packagegroups"]
DISTRO = "kinetic"
DIST_FILE = "https://raw.githubusercontent.com/ros/rosdistro/master/" + DISTRO+ "/distribution.yaml"
dist_raw = None


class MoveRepoExcetion(Exception):
    pass

def print_debug(text):
    pass

def print_err(text):
    pre = '\033[91m'
    post = '\033[0m'
    print(pre + text + post)


def print_ok(text):
    pre = '\033[92m'
    post = '\033[0m'
    print(pre + text + post)


def check_version(package, silent=False, details=False):
    global dist_raw
    printlist = []
    if dist_raw is None:
        dist_raw = yaml.load(urllib.request.urlopen(DIST_FILE).read())
    package_dir = os.path.join(BASE_DIR, package)
    versions = []
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

            if not silent and details:
                printlist.append(" - " + os.path.basename(filename))
    if len(versions) > 1:
        print("Package: %s" % package)
        print(versions)
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

    if not silent:
        print(package.ljust(35) + pre + version.ljust(10) + mid + dist_ver.ljust(10) + post)
        for line in printlist:
            print(line)
    return match, version, dist_ver


def get_checksums_from_url(url):
    data = urllib.request.urlopen(url).read()
    m = hashlib.md5()
    m.update(data)
    md5sum = m.hexdigest()
    m = hashlib.sha256()
    m.update(data)
    sha256sum = m.hexdigest()
    return md5sum, sha256sum


def update_checksums_in_file(package, fn, dist_version):
    with open(fn) as recipe_file:
        data = recipe_file.read()

    md5sum = re.search('SRC_URI\[md5sum\]\s*=\s*"(\S*)"', data).group(1)
    try:
        sha256sum = re.search('SRC_URI\[sha256sum\]\s*=\s*"(\S*)"', data).group(1)
    except:
        print_err("Error reading sha256sum in package %s" % package)
        sha256sum = " " * 64
    if len(md5sum) != 32 and len(sha256sum) != 64:
        print_err("Failed reading checksums.")
        return False
    pv = dist_version
    spn = package.replace('-', '_')
    sp = "%s-%s" % (spn, pv)
    
    url = re.search('SRC_URI\s*=\s*"(\S*)\s*["\\\\]', data).group(1)
    url = url.replace("${ROS_SPN}", spn)
    url = url.replace("${ROS_SP}", sp)
    url = url.replace("${PV}", pv)
    url = url.split(";")[0]

    repo = dist_raw["repositories"][package.replace("-", "_")]["source"]["url"].split(".git")[0]
    if repo not in url:
        print(url)
        print(repo)
        raise MoveRepoExcetion()

    md5sum_new, sha256sum_new = get_checksums_from_url(url)
    print_debug("Updating checksums in file %s" % fn)
    #print("old md5: %s" % md5sum)
    #print("new md5: %s" % md5sum_new)
    #print("old sha256: %s" % sha256sum)
    #print("new sha256: %s" % sha256sum_new)
    with open(fn) as recipe_file:
        recipe_data = recipe_file.read()
    recipe_data = recipe_data.replace(md5sum, md5sum_new)
    recipe_data = recipe_data.replace(sha256sum, sha256sum_new)
    with open(fn, 'w') as recipe_file:
        recipe_file.write(recipe_data)


def update_all_packages():
    dist_raw = yaml.load(urllib.request.urlopen(DIST_FILE).read())
    packages = [x for x in sorted(os.listdir(BASE_DIR)) if x not in EXCLUDE]
    for package in packages:
        if not check_version(package, silent=True)[0]:
            update_package(package)


def update_package(package):
    print_debug("Updating %s" % package)
    print_header()
    match, version, dist_version = check_version(package, silent=False, details=True)
    if match:
        print("Packet is already in newest version")
        return
    if dist_version == "":
        print("Packet not found in dist file")
        return

    if version == "git":
        print("Layer uses git version. Please update manually") 
        return
    elif LooseVersion(version) > LooseVersion(dist_version) and not "--downgrade" in sys.argv:
        print("Layer version is newer than dist version, use --downgrade as last argument to downgrade")
        return

    try:
        path = os.path.join(BASE_DIR, package)
        recipes = []
        for filename in os.listdir(path):
            if filename.endswith(".bb"):
                recipes.append(os.path.join(path, filename))

        update_include = False 
        rename_requests = []
        for recipe in recipes:
            with open(recipe) as recipe_file:
                data = recipe_file.read()
                
            old_fn = os.path.join(recipe)
            new_fn = os.path.join(recipe.replace(version, dist_version))
            rename_requests.append([old_fn, new_fn])

            if "SRC_URI[md5sum]" not in data and "SRC_URI[sha256sum]" not in data:
                update_include = True 
            else:
                update_checksums_in_file(package, old_fn, dist_version)

        if update_include:
            inc_fn = os.path.join(BASE_DIR, package, package + ".inc")
            update_checksums_in_file(package, inc_fn, dist_version)
    except MoveRepoExcetion:
        print_err("Repo moved %s" % package)
    else:
        for [old_fn, new_fn] in rename_requests:
            print_debug("Rename %s" % recipe)
            #print("old: %s" % old_fn)
            #print("new: %s" % new_fn)
            os.rename(old_fn, new_fn)
    print_ok("Updated")

        


def print_header():
    print("\033[1m\033[4m" + "package".ljust(35) +
          "layer".ljust(13) + "distro".ljust(10) + '\033[0m')


def print_list(details=False):
    dist_raw = yaml.load(urllib.request.urlopen(DIST_FILE).read())
    packages = [x for x in sorted(os.listdir(BASE_DIR)) if x not in EXCLUDE]
    print_header()
    for package in packages:
        check_version(package, details=details)


def print_mismatch(details=False):
    dist_raw = yaml.load(urllib.request.urlopen(DIST_FILE).read())
    packages = [x for x in sorted(os.listdir(BASE_DIR)) if x not in EXCLUDE]
    print_header()
    for package in packages:
        if not check_version(package, silent=True)[0]:
            match, version, dist_ver = check_version(package, details=details)


def print_help():
    fn = sys.argv[0]
    print("Usage:")
    print("List all versions:                  %s list (--details)" % fn)
    print("List all versions that don't match: %s mismatch (--details)" % fn)
    print("Update recipe to dist version:      %s update <package> (--downgrade)" % fn)
    print("Update all recipes to dist version: %s update-all (--downgrade)" % fn)



if __name__ == "__main__":
    if len(sys.argv) == 1:
        print_help()
    else:
        if sys.argv[1] == "list":
            print_list(details="--details" in sys.argv)
        elif sys.argv[1] == "mismatch":
            print_mismatch(details="--details" in sys.argv)
        elif sys.argv[1] == "update" and len(sys.argv) >= 3:
            update_package(sys.argv[2])
        elif sys.argv[1] == "update-all" and len(sys.argv):
            update_all_packages()
        else:
            print_help()
