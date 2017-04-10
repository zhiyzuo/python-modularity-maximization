# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
import os, codecs

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()

import modularity_maximization
VERSION = modularity_maximization.__version__

setup(
    name='python-modularity-maximization',
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['modularity_maximization'],
    exclude_package_data={'': ['data*']},

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=VERSION,

    description='Community detection using Newman spectral methods to maximize modularity',
    long_description=read("README.rst"),

    # The project's main homepage.
    url='http://zhiyzuo.github.io/python-modularity-maximization/',
    download_url='https://github.com/zhiyzuo/python-modularity-maximization/tarball/' + VERSION,

    # Author details
    author='Zhiya Zuo',
    author_email='zhiyazuo@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'Topic :: Scientific/Engineering :: Information Analysis',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='modularity newman community-detection network-analysis clustering',

    install_requires=[
        "scipy",
        "numpy",
        "networkx",
    ]
)
