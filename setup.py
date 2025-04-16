from setuptools import setup, find_packages
from pathlib import Path


long_description = Path("README.md").read_text(encoding="utf-8")

setup(
    name="cnmaptiling",
    version="0.1.0",
    author="k96e",
    author_email="zy1835562526@gmail.com",
    description="A Python library for tiling based on Chinese mapping standards.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/k96e/cnmaptiling",
    packages=find_packages(exclude=["tests", "docs"]),
    python_requires=">=3.6",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
    ],
)
