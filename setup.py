try:
        from setuptools import setup
except ImportError:
        print("+++++++++++ WARNING +++++++++++")
        print("WARNING: setuptools not installed! This will break automatic installation of requirements!")
        print("Please install the Python package python-kafka and pytz manually.")
        print("+++++++++++++++++++++++++++++++++")
        from distutils.core import setup

setup(
    # Application name:
    name="hvmonitor",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Christian Sieber",
    author_email="c.sieber@tum.de",

    # Packages
    packages=["hvmonitor"],

    # Include additional files into the package
    include_package_data=False,

    # Details
    url="https://github.com/csieber/hvmonitor",

    #
    # license="LICENSE.txt",
    description="Resource usage monitor for SDN hypervisors.",

    long_description=open("README.md").read(),

    # Dependent packages (distributions)
    install_requires=["kafka-python", "pytz"],
)
