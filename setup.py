"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

def readme():
    with open('README.rst') as file:
        return file.read()

setup(
    name='ANYstructure',  # Required
    url = 'https://github.com/audunarn/ANYstructure',
    entry_points={'gui_scripts': ['ANYstructure = ANYstructure.__main__:main']},
    version='0.2.2',  # Required
    description='A plate field optimization tool for offshore structures according to DNVGL standards',  # Required
    long_description = readme(),
    author='Audun Arnesen Nyhus',  # Optional
    author_email='audunarn@gmail.com',  # Optional
    classifiers=[  # Optional
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering'],
    keywords='dnv-gl-os-c101 naval_architecture structural_engineering steel buckling fatigue local_scantlings',
    include_package_data=True,
    packages=['ANYstructure'],
    install_requires=['scipy', 'numpy', 'pyswarm', 'matplotlib','reportlab==3.4.0']
)