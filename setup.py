from setuptools import setup, find_packages

setup(
    name="st-transformers-js",
    version="0.2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["streamlit>=1.0"],
    package_data={
        'st_transformers_js': ['frontend_v1/*', 'frontend_v2/dist/*']
    },
)
