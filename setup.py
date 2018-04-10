from setuptools import setup
import os

#: Parse requirements/production.txt and extract dependencies
PROJ_ROOT = os.path.dirname(os.path.abspath(__file__))
with open(f'{PROJ_ROOT}/requirements/production.txt', 'r') as prod_file:
    prod_deps = prod_file.read().splitlines()

#: init setuptools
setup(
    name='FridgeFarm',
    version='0.1',
    long_description=__doc__,
    packages=['app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=prod_deps,
    entry_points={
        'console_scripts': [
            'fridgefarm = flask.cli:main',
            'ff = flask.cli:main',
        ],
    },
)
