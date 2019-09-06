from setuptools import setup

import sys
import registry

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='steward',
    version=registry.__version__,
    python_requires='>=3.5',
    author='artanicus & cheleus',
    author_email='dev@steward.app',
    url='https://github.com/Steward-app/steward',
    description='Lightweight Maintenance DB and scheduler',
    long_description=long_description,
    license='MIT',
    packages=['registry', 'app'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=[''],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ])  # yapf: disable
