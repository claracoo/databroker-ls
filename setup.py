from os import path
from setuptools import setup, find_packages
import sys
import versioneer


# NOTE: This file must remain Python 2 compatible for the foreseeable future,
# to ensure that we error out properly for people with outdated setuptools
# and/or pip.
min_version = (3, 7)
if sys.version_info < min_version:
    error = """
databroker-ls does not support Python {0}.{1}.
Python {2}.{3} and above is required. Check your Python version like so:

python3 --version

This may be due to an out-of-date pip. Make sure you have pip >= 9.0.1.
Upgrade pip like so:

pip install --upgrade pip
""".format(
        *(sys.version_info[:2] + min_version)
    )
    sys.exit(error)

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst"), encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open(path.join(here, "requirements.txt")) as requirements_file:
    # Parse requirements.txt, ignoring any commented-out lines.
    requirements = [
        line
        for line in requirements_file.read().splitlines()
        if not line.startswith("#")
    ]


setup(
    name="databroker-ls",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="listing option for databroker",
    long_description=readme,
    author="Brookhaven National Lab",
    author_email="ccook@bnl.gov",
    url="https://github.com/claracoo/databroker-ls",
    python_requires=">={}".format(".".join(str(n) for n in min_version)),
    packages=find_packages(exclude=["docs", "tests"]),
    entry_points={
        "console_scripts": [
            "db-snek = databroker_ls.snek:main",
            "db-ls = databroker_ls.command_line:main",
            "db-cat = databroker_ls.databroker_cat.cat:main",
        ],
       "intake.catalogs": ["local = databroker_ls:databroker_ls_catalog_instance"],
    },
    include_package_data=True,
    package_data={
        "databroker_ls": [
            "db-snek = databroker_ls.snek.py",
            "db-ls = databroker_ls.main.py",
            "db-cat = databroker_ls.databroker_cat.cat.py"
            # When adding files here, remember to update MANIFEST.in as well,
            # or else they will not be included in the distribution on PyPI!
            # 'path/to/data_file',
        ],
    },
    install_requires=requirements,
    license="BSD (3-clause)",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
)
