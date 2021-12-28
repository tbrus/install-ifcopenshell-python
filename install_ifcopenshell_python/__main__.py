"""
install_ifcopenshell_python.__main__
------------------------------------

Install ifcopenshell for python based on hard coded aws URL.

NOTE: ifcopenshell will not be visible via command `pip list`.
"""

import argparse
import os
import platform
import shutil
import site
import sys
import urllib.request
import zipfile


class SystemNotFoundError(Exception):
    pass


class PythonVersionError(Exception):
    pass


def get_system():
    """Get current platform system.

    Raises:
        SystemNotFoundError: if `system` is not any of the values:
            'linux', 'windows', 'darwin'.

    Returns:
        str: platform system.
    """
    if platform.system().lower() == "linux":
        system = "linux"
    elif platform.system().lower() == "windows":
        system = "win"
    elif platform.system().lower() == "darwin":
        system = "macos"
    else:
        msg = (
            f"{platform.system().lower()} is not the valid system name. "
            f"You can specify system manually via argument in command line."
        )
        raise SystemNotFoundError(msg)
    return system


def get_architecture():
    """Get platform architecture.

    Returns:
        str: platform architecture. One of values: '32' or '64'.
    """
    architecture_bit = platform.architecture()[0]
    architecture_list = [i for i in architecture_bit if i.isdigit()]
    architecture = "".join(architecture_list)
    return architecture


def get_python_version():
    """Get running python version.

    This function returns string of 2 digits. The first one determines
    the major version and the second one determines the minor version of
    running python, e.g. '38', '39'.
    pyifc supports python >= 3.7.

    Returns:
        str: current python version
    """
    python_major = str(sys.version_info.major)
    python_minor = str(sys.version_info.minor)
    python_version = python_major + python_minor
    if int(python_version) < 37:
        msg = (
            f"python{python_major}.{python_minor} is not supported "
            f"by pyifc. Install python >= 3.7) on your computer."
        )
        raise PythonVersionError(msg)
    return python_version


def get_args():
    """Get values for system, architecture and python version
    specified by the user via command line. Default values are
    determined automatically.

    Possible arguments typed via command line are:
        -s --system -  platform system. Possible values: 'linux',
            'win', 'macos'.
        -a --architecture - platform architecture. Possible values:
              '32' and '64'.
        -v --python_version - version of running python. This should be
            a string of two digits: the major and minor versions of
            running python. Possible values: '37', '38', '39' (pyifc
            supports python >= 3.7).

    Returns:
        [argparse.Namespace]: Namespace containing 3 values:
            - str - args.system
            - str - args.architecture
            - str - args.python_version
    """
    description = (
        "Download ifcopenshell based on platform system, "
        "platform architecture and running python version."
    )
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-s",
        "--system",
        help="Platform system.",
        type=str,
        choices=["linux", "win", "macos"],
        default=get_system(),
    )
    parser.add_argument(
        "-a",
        "--architecture",
        help="Platform architecture.",
        type=str,
        choices=["32", "64"],
        default=get_architecture(),
    )
    parser.add_argument(
        "-v",
        "--python-version",
        help=(
            "Running python version; string of major and minor version, "
            "e.g. '39'. pyifc supports python >= 3.7."
        ),
        type=str,
        choices=["37", "38", "39"],
        default=get_python_version(),
    )
    args = parser.parse_args()
    return args


def main():
    """The main function of this script.

    Downloads ifcopenshell.zip, extracts and removes zip file, moves dir
    with ifcopenshell package to site-packages directory of currently
    running venv. It forces moving (overwrites package if exists).
    """
    # Get url for given system, architecture and python version
    args = get_args()
    print("Getting arguments...")
    print(
        f"Arguments: system='{args.system}', "
        f"architecture='{args.architecture}', "
        f"python_version='{args.python_version}'"
    )
    url = f"https://s3.amazonaws.com/ifcopenshell-builds/ifcopenshell-python-{args.python_version}-v0.6.0-517b819-{args.system}{args.architecture}.zip"

    # Check whether url is valid
    print(f"Checking if url is valid...")
    print(url)
    try:
        response = urllib.request.urlopen(url)
        code = response.getcode()
        print(f"Status: {code}")
        print("Given url is valid")
    except Exception as e:
        print("Given url is not valid")
        print(f"Error:  {url} : {str(e)}")

    # Download ifcopenshell package, unzip and delete zip file
    zip_filename = "ifcopenshell.zip"
    print("Downloading ifcopenshell...")
    urllib.request.urlretrieve(url, zip_filename)
    print("Extracting files...")
    with zipfile.ZipFile("ifcopenshell.zip", "r") as zip_ref:
        zip_ref.extractall()
    print("Removing irrelevant files...")
    if os.path.exists(zip_filename):
        os.remove(zip_filename)

    # Move ifcopenshell package directory to site-packages directory
    # of currently running venv
    # If package exists in target directory - remove it and move newly
    # downloaded package
    print("Moving files...")
    source_dir = os.path.join(os.getcwd(), "ifcopenshell")
    if args.system == 'win':
        target_dir = site.getsitepackages()[1]
    else:
        target_dir = site.getsitepackages()[0]
    target = os.path.join(target_dir, "ifcopenshell")
    if os.path.exists(target):
        print("Found ifcopenshell in packages")
        print("Removing found files...")
        shutil.rmtree(target)
        print("Successfully removed files")
        print("Moving newly downloaded files...")
    shutil.move(source_dir, target_dir)
    print("Ifcopenshell successfully moved")
    print(
        "\nWARNING: ifcopenshell is now available via import, but ",
        "not via pip list",
    )


if __name__ == "__main__":
    main()