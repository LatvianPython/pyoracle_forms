import setuptools

from pyoracle_forms import __version__

with open("README.rst", mode="r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyoracle_forms",
    version=__version__,
    author="LatvianPython",
    author_email="kalvans.rolands@gmail.com",
    description="Python wrapper of the Oracle Forms API",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/LatvianPython/pyoracle_forms",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 2 - Pre-Alpha",
    ],
    include_package_data=True,
    python_requires=">=3.7",
)
