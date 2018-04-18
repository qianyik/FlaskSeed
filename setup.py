from setuptools import setup, find_packages


requires = [
    'PasteDeploy==1.5.2',
    'Flask==0.10.1',
    'flup==1.0.2',
    'Mako==1.0.3',
    'MySQL-python==1.2.3',
    'SQLAlchemy==1.1.3',
    'requests==2.7.0',
    'transaction==2.0.3',
    'Werkzeug==0.10.4',
    'Flask-RESTful==0.3.6',
]

setup(name='flask_angular_scaffold',
      version='0.0',
      description='flask_angular_scaffold',
      author='',
      author_email='',
      url='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='flask_angular_scaffold',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = flask_angular_scaffold:main
      [console_scripts]
      initialize_flask_angular_scaffold_db = flask_angular_scaffold.scripts.initializedb:main
      """,
      )
