Introduction
============

.. image:: https://travis-ci.org/Shoobx/shoobx.junitxml.png?branch=master
   :target: https://travis-ci.org/Shoobx/shoobx.junitxml

.. image:: https://coveralls.io/repos/github/Shoobx/shoobx.junitxml/badge.svg?branch=master
   :target: https://coveralls.io/github/Shoobx/shoobx.junitxml?branch=master

.. image:: https://img.shields.io/pypi/v/shoobx.junitxml.svg
   :target: https://pypi.python.org/pypi/shoobx.junitxml

.. image:: https://img.shields.io/pypi/pyversions/shoobx.junitxml.svg
   :target: https://pypi.python.org/pypi/shoobx.junitxml/

This package provides a `zope.testrunner` feature that stores the test
results in a JUnit-compatible XML file. This file can be consumed by
Jenkins and other tools to generate test reports.

This is achieved by implementing a custom output formatter that
collects and then writes out the XML file. The formatter then
delegates further test result tracking to the oriignal output formatter.

The core code of this package is based on the excellent work by Martin
Aspelli and the Plone Foundation. Thus the code is released under ZPL
2.1, the original license of `collective.xmltestreport`.


Usage
=====

In order to install your own features, you have to customize the main
`Runner` class a bit. Here is what we do at Shoobx:

::

  from shoobx.junitxml import feature
  import zope.testrunner.runner

  feature.JUnitXMLSupport.install_options()

  class Runner(zope.testrunner.runner.Runner):

      def configure(self):
          super(Runner, self).configure()
          self.features.append(feature.JUnitXMLSupport(self))

  zope.testrunner.runner.Runner = Runner

Call the test runner with the argument `--xml=junit.xml` to specify the name
of the generated JUnit file.

Code repository
===============

https://github.com/shoobx/shoobx.junitxml
