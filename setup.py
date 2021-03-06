import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'html2text',
    'logbook',
    'mailer',
    'passlib',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_handlers',
    'pendulum',
    'pymysql',
    'requests',
    'rollbar',
    'sphinx',
    'sphinx-autobuild',
    'sphinx_rtd_theme',
    'sqlalchemy',
    'waitress',
    ]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
    ]

setup(name='mlbpool',
      version='1.1',
      description='mlbpool',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Paul Cutler',
      author_email='paul.r.cutler@gmail.com',
      url='https://github.com/prcutler/mlbpool2',
      keywords='web pyramid pylons baseball MLB fantasy-baseball',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = mlbpool:main
      """,
      )
