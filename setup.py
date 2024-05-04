from setuptools import find_packages, setup

from spectrumapp_loader import AUTHOR_EMAIL, AUTHOR_NAME, DESCRIPTION, NAME, VERSION  # noqa: I100


setup(
    # info
    name=NAME,
    description=DESCRIPTION,
    license='MIT',
    keywords=['spectroscopy', 'atomic emission spectroscopy', 'atomic absorption spectroscopy'],

    # version
    version=VERSION,

    # author details
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,

    # setup directories
    packages=find_packages(),

    # setup data
    package_data={
        '': [],
    },

    # requires
    install_requires=[
        item.strip() for item in open('requirements.txt', 'r').readlines()
        if item.strip()
    ],
    python_requires='>=3.10',
)
