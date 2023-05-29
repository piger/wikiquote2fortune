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
    version='0.2.0',
    description="Create a fortune file from a wikiquote page",
    author='Daniel Kertesz',
    author_email='daniel@spatof.org',
    url='https://github.com/piger/wikiquote2fortune',
    license='BSD',
    long_description=__doc__,
    install_requires=[
        'beautifulsoup4==4.10.0',
        'Click==8.0.3',
        'lxml==4.9.1',
        'requests==2.31.0',
    ],
    include_package_data=True,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wikiquote2fortune = wikiquote2fortune.main:main',
        ],
    },
)
