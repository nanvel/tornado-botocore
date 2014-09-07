# -*- encoding: utf-8 -*-
"""
Python setup file for the nicedit app.

In order to register your app at pypi.python.org, create an account at
pypi.python.org and login, then register your new app like so:

    python setup.py register

If your name is still free, you can now make your first release but first you
should check if you are uploading the correct files:

    python setup.py sdist

Inspect the output thoroughly. There shouldn't be any temp files and if your
app includes staticfiles or templates, make sure that they appear in the list.
If something is wrong, you need to edit MANIFEST.in and run the command again.

If all looks good, you can make your first release:

    python setup.py sdist upload

For new releases, you need to bump the version number in
nicedit/__init__.py and re-run the above command.

For more information on creating source distributions, see
http://docs.python.org/2/distutils/sourcedist.html

"""
import os
import tornado_botocore as app

from setuptools import setup, find_packages
from setuptools.command.bdist_egg import bdist_egg as _bdist_egg


class bdist_egg(_bdist_egg):
    def run(self):
        call(["pip install -r requirements.txt --no-clean"], shell=True)
        _bdist_egg.run(self)

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name="tornado-botocore",
    version=app.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='tornado, botocore, async boto, amazon, aws',
    author='Oleksandr Polyeno',
    author_email='polyenoom@gmail.com',
    url="https://github.com/nanvel/tornado-botocore",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'botocore',
        'tornado',
    ],
    cmdclass={'bdist_egg': bdist_egg},  # override bdist_egg
)
