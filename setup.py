from setuptools import setup

import sys
import maintcal

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='maintcal',
    version=maintcal.__version__,
    python_requires='>=3.5',
    author='artanicus',
    author_email='maintcal@nocturnal.fi',
    url='https://github.com/Artanicus/maintcal',
    description='Lightweight Maintenance DB and scheduler',
    long_description=long_description,
    license='MIT',
    packages=['maintcal'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=['google_api', 'absl-py'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ])  # yapf: disable
