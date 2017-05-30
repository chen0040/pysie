"""
pysie
-----

Package pysie implements a statistical inference engine
"""

import re
import ast
import io
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('pysie/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

def long_description():
    with io.open('README.rst', 'r', encoding='utf-8') as f:
        readme = f.read()
    return readme

setup(
    name='pysie',
    version=version,
    url='https://github.com/chen0040/pysie',
    license='MIT',
    author='Xianshun Chen',
    author_email='xs0040@gmail.com',
    description='Python implementation of a statistical inference engine',
    long_description=long_description(),
    packages=['pysie'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    setup_requires=["numpy"],
    install_requires=[
        "scipy",
        "enum"
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing :: General',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

__author__ = 'Xianshun Chen'
