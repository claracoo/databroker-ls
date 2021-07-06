=============
databroker-ls
=============

.. image:: https://img.shields.io/travis/claracoo/databroker-ls.svg
        :target: https://travis-ci.org/claracoo/databroker-ls

.. image:: https://img.shields.io/pypi/v/databroker-ls.svg
        :target: https://pypi.python.org/pypi/databroker-ls


listing option for databroker

* Free software: 3-clause BSD license
* Documentation: (COMING SOON!) https://claracoo.github.io/databroker-ls.

Features
--------

## Installation

OS X & Linux:

```sh
git clone https://github.com/claracoo/databroker-ls.git
```
```sh
cd databroker-ls
```
Please make sure python3 is installed. Create a new Virtual Environment. For example:
```sh
python3 -m venv venv
```
```sh
. venv/bin/activate
```
```sh
python3 setup.py develop
```
Some libraries and modules to have installed:
pynput:
```sh
pip install pynput
```
databroker:
```sh
pip install databroker
```
databroker-pack:
```sh
pip install databroker-pack
```
bluesky:
```sh
pip install bluesky
```
ophyd:
```sh
pip install ophyd
```
bluesky-widgets:
```sh
pip install bluesky-widgets
```
tableprint:
```sh
pip install tableprint
```
yaml:
```sh
pip install pyyaml
```

## Usage example

This can be used with ```db-ls`` or in an ipython environment ```!db-ls```. The first time you use it, you should be prompted to pick a default catalog.



























