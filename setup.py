from setuptools import setup, find_packages

setup(
    name="Insurance-Fraud-Detection",
    version="1.0.0",
    author="Arpit Kadam",
    author_email="arpitkadam2000@gmail.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[],
    include_package_data=True,
    package_data={'': ['templates/*']}  
)
