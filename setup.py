#!/usr/bin/env python
# -*- coding: utf-8 -*-

#This was modified from https://github.com/navdeep-G/setup.py/blob/master/setup.py
#Which is part of the repository https://github.com/navdeep-G/setup.py
#Which is part of the public domain. 
# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from shutil import rmtree
from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'CiteSoft'
DESCRIPTION = 'This is a python implementation of CiteSoft. CiteSoft is a plain text standard consisting of a format and a protocol that exports the citations for the  end-users for whichever softwares they have used. CiteSoft has been designed so that software dev-users can rely upon it regardless of coding language or platform, and even for cases where multiple codes are working in a coupled manner..'
URL = 'https://github.com/AdityaSavara/CiteSoft_py'
EMAIL = 'AditySavara2008@u.northwestern.edu'  
AUTHOR = 'Aditya Savara'
REQUIRES_PYTHON = '>=3.0.0'
VERSION = '0.3.9'
LICENSE = 'BSD-3-Clause'

# What packages are required for this module to be executed?
REQUIRED = [
    'semantic_version', 'PyYAML'
    # 'requests', 'maya', 'records', #numpy...
]

# What packages are optional?
EXTRAS = {
    # 'uncertainties': ['uncertainties'], #pymc...
}

#To make sure the license etc. is included, I added the DATA_FILES object based on https://stackoverflow.com/questions/9977889/how-to-include-license-file-in-setup-py-script
DATA_FILES = [
       ("", ["LICENSE.txt", "README.md"]),
       ]

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME.lower(),
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    data_files = DATA_FILES,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license=LICENSE,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
