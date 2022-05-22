from setuptools import setup

setup(
    name="Python Farm Game",
    version="0.5.2",
    description="Python farm game ",
    author="orneo1212",
    author_email="orneo1212@gmail.com",
    packages=["farmlib", "pygameui"],  # same as name
    entry_points={
        "console_scripts": [
            "main=farmlib.main:main",
        ],
    },
)
