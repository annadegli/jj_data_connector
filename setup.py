import os
import sys
from setuptools import setup, find_packages
from pathlib import Path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='jj_data_connector',
    author='Jie Jenn',
    author_email='jiejenn@learndataanalysis.org',
    version='0.1.0',
    keywords=['data connector', 'google analtics 4', 'GA4', 'Salesforce', 'sfdc', 'Google Search Console'],
    python_requires='>=3.6',
    install_requires=['google-api-python-client>=2.51.0', 'google-auth-httplib2>=0.1.0', 'google-auth-oauthlib>=0.5.2', 'requests>=2.28.0'],
    packages=['jj_data_connector'],
    license='MIT',
)   