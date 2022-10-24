
# CLI BASE

This is a basic structure to create a command without passing the python command and the relative (or absolute) path for the python file.

----------

## Usage

### Install

Just execute:

    > bash install

and, all the requirements will be installed.

You can change the requirements.txt libs that you need.
Also change the num version on the file VERSION.txt

### Execute

Once the lib be installed, execute the command:

    > pycmd

to check if it works. The command name is just that: a custom name. You can change it as you want.
The documentation will be on setup.py file.

### Uninstall

Also, just execute:

    > bash uninstall

and all the libs installed should be uninstalled.

### Recomemdation

As a recommendation, we encourage you to create first in virtual environment first, just for testing purpose.

### Setup install

    setup.py file for SWIG example. The following are the parameters to set up for your own setup

    name: name of the module
    version: version of the module
    py_modules: list of python modules to be installed
    ext_modules: list of extension modules to be installed
    packages: list of packages to be installed
    package_dir: dictionary of package names and their directories
    package_data: dictionary of package names and their data files
    data_files: list of data files to be installed
    scripts: list of scripts to be installed
    install_requires: list of dependencies to be installed
    author: author name
    author_email: author email
    entry_points:
        pycmd = cli_base.cli:main
            where pycmd is the name of the command line tool
            cli_base is the package name
            and cli is the module name
