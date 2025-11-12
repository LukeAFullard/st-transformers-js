import os
from setuptools import setup, find_packages
import re

def get_version():
    """
    Read the version from the __init__.py file.
    """
    with open(os.path.join("st_transformers_js", "__init__.py"), "r") as f:
        version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name="st-transformers-js",
    version=get_version(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=["streamlit>=1.0"],
    package_data={
        'st_transformers_js': ['frontend_v1/*', 'frontend_v2/dist/*']
    },
)
