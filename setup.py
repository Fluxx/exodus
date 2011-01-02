from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='exodus',
      version=version,
      description="Dead simple, language agnostic migrations framework written in python.",
      long_description="""\
Dead simple, language agnostic migrations framework written in python.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Jeff Pollard',
      author_email='jeff.pollard@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
