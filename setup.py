import os

from setuptools import setup, find_packages


def get_version():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'diff/version.py')) as f:
        locals = {}
        exec(f.read(), locals)
        return locals['VERSION']
    raise RuntimeError('No version info found.')


setup(
    name='diff-and-patch',
    version=get_version(),
    packages=find_packages(exclude=['tests', 'samples']),
    install_requires=[
        'click>=3.0.0'
    ],
    url='',
    license='BSD',
    author='bkp',
    author_email='pramod.mundhra@treebohotels.com',
    entry_points={
        'console_scripts': [
            'diff = diff.cli:main'
        ],
    },
    test_suite="tests",
    description='A highly configurable python library that can be used to diff and patch python objects'
)
