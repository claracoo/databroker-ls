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

```
git clone https://github.com/claracoo/databroker-ls.git
```

```
cd databroker-ls
```

Please make sure python3 is installed. Create a new Virtual Environment. For example:
```
python3 -m venv venv
```

```
. venv/bin/activate
```

```
python3 setup.py develop
```


Some libraries and modules to have installed:
pynput:
``
pip install pynput
``

databroker:
``
pip install databroker
``

databroker-pack:
``
pip install databroker-pack
``

bluesky:
``
pip install bluesky
``

ophyd:
``
pip install ophyd
``

bluesky-widgets:
``
pip install bluesky-widgets
``

tableprint:
``
pip install tableprint
``

yaml:
``
pip install pyyaml
``



## Usage example

This can be used with ``db-ls`` or in an ipython environment ``!db-ls``. The first time you use it, you should be prompted to pick a default catalog.



























