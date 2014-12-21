try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os

long_description = 'library for analyzing company financial documents'
if os.path.exists('README.rst'):
    long_description = open('README.rst').read()

setup(
    name='DIY-FilingsResearch',
    version='0.0.1',
    description='library for analyzing company financial documents',
    author='Joe Cabrera',
    author_email='jcabrera@eminorlabs.com',
    url='https://github.com/greedo/DIY-FilingsResearch/',
    license='Apache License',
    keywords='Financial, Accounting, file formats, 10k,filings',
    packages=['research'],
    install_requires=['requests', 'lxml'],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Office/Business :: Financial',
    ],
    long_description=long_description
)
