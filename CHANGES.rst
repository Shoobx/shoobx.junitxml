Changelog
=========


0.3.0 (unreleased)
------------------

- Rename command line option `--xml`` to ``--junitxml`` since zope.testrunner 6.3.0
  added the same option and there's a conlict


0.2.2 (2021-01-13)
------------------

- Fixed documentation.


0.2.1 (2020-12-03)
------------------

- Support for latest zope.testrunner and other latest dependencies
- Added missing stderr and stdout params to test_failure and test_error
  methods of XMLOutputFormattingWrapper
  (prevented xml report file generation in zope.testrunner >= 5.1)
- dropped support for python 2, updated support for 3.X


0.2.0 (2018-10-10)
------------------

- Add support for Python 3.7

- Add support for the latest `zope.testrunner`, which switches from `optparse`
  to `argparse`.


0.1.4 (2018-03-30)
------------------

- Record doctest cases in modules where test cases are defined,
  instead of putting them all in 'doctest' module.


0.1.3 (2018-02-09)
------------------

- Bugfix: When test failure has binary data, record a Base64 representation of
  the failure


0.1.2 (2018-02-07)
------------------

- Python 3 bugfix


0.1.1 (2017-10-03)
------------------

- Added some basic tests.

- Official Python 3.6 support.


0.1.0 (2017-10-03)
------------------

* Initial release
