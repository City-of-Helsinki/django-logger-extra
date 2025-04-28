import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-logger-extra",
    version="0.1.1",
    packages=["logger_extra"],
    include_package_data=True,
    license="MIT",
    description="A module that provides extras for logger.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/City-of-Helsinki/django-logger-extra",
    author="City of Helsinki",
    author_email="dev@hel.fi",
    install_requires=[],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    keywords=[
        "logging",
        "extra tools",
        "plugin extension",
    ]
)

