# -*- coding: utf-8 -*-
"""
wikiquote2fortune
-----------------

wikiquote2fortune is a little script that can fetch a wikiquote page and extract
quotes to create a fortune(6) file.

"""
from setuptools import setup, find_packages


setup(
    name='wikiquote2fortune',
    version='0.1.1',
    description="Create a fortune file from a wikiquote page",
    author='Daniel Kertesz',
    author_email='daniel@spatof.org',
    url='',
    license='BSD',
    long_description=__doc__,
    install_requires=[
        'beautifulsoup4>=4',
        'requests>=1.2',
    ],
    include_package_data=True,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wikiquote2fortune = wikiquote2fortune.main:main',
        ],
    },
)
