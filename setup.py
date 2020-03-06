from setuptools import setup
from setuptools import find_packages

setup(
        name="strcuta",
        version="0.0.1",
        url="https://github.com/takagiy/strcutau",
        description="Load UTAU voice banks into the Python data structure.",
        author="takagiy",
        author_email="takagiy.4dev@gmail.com",
        license="MIT",
        packages=find_packages(),
        include_package_data=False,
        install_requires=[])
