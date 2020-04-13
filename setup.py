from setuptools import setup, find_packages
import sys
sys.path.append('./tests')


setup(
    name='LC_Manager',
    version='1.1',
    packages=find_packages(),
    url='https://it-for-pharma.com',
    license='MIT',
    author='parsely',
    author_email='humi20190106@gmail.com',
    install_requires=['PySimpleGUI==4.16.0', 'openpyxl==3.0.3'],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"],
)