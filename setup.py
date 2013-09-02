from __future__ import with_statement

from setuptools import setup


def get_version():
    with open('redistruct/version.txt') as f:
        return f.read().strip()


def get_readme():
    try:
        with open('README.rst') as f:
            return f.read().strip()
    except IOError:
        return ''


setup(
    name='redistruct',
    version=get_version(),
    description='Human-friendly structured redis API wrapper.',
    long_description=get_readme(),
    author='Jeong YunWon',
    author_email='redistruct@youknowone.org',
    url='https://github.com/youknowone/redistruct',
    packages=(
        'redistruct',
    ),
    package_data={
        'redistruct': ['version.txt']
    },
    install_requires=[
        'redis',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
     ],
)

