"""
Affordable project setup file.

Copyright (C) 2017

This file is part of Affordable.

Affordable is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Affordable is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Affordable.  If not, see <http://www.gnu.org/licenses/>.
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='affordable',
    version='0.0.1',
    description='Sokoban robot version',
    url='https://github.com/...',
    license='GPL3',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: HOOMANO Hackathon',
        'License :: GPL3',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='Hackathon',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['cozmo'],

    entry_points={
        'console_scripts': [
            'affordable=affordable.affordable2:main',
        ],
    },
)
