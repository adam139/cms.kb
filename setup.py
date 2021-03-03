from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='cms.db',
      version=version,
      description="Chinese medical science AI system db.",
      long_description=open("README.md").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['cms'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'mysqlclient==1.4.6',
          'SQLAlchemy',
          'plone.behavior',
          'plone.app.dexterity',
          'plone.app.textfield',
          'plone.directives.form',
          'collective.z3cform.datagridfield>=1.5.3',
          'plone.formwidget.autocomplete==1.4.0',
      ],
      extras_require={
    'test': ['plone.app.testing',]
        },       
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
