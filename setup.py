"""Setup file for GitSecret"""
from setuptools import setup, find_packages


def readme():
    """Include README.md content in PyPi build information"""
    with open('README.md') as file:
        return file.read()


setup(
    name='envadmin',
    version='0.0.1',
    author='Ivan Lee',
    author_email='ivanklee86@gmail.com',
    description='Secure-ish environment management.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/ivanklee86/envadmin',
    packages=find_packages(),
    install_requires=[],
    tests_require=[],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points='''
        [console_scripts]
        envadmin=envadmin.cli:cli
    '''
)
