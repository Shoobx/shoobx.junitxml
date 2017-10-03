###############################################################################
#
# Copyright 2017 by Plone Foundation and Shoobx, Inc.
#
###############################################################################
"""Shoobx JUnit XML Output feature
"""
import optparse
import zope.testrunner.feature
import zope.testrunner.options

from shoobx.junitxml import formatter

class JUnitXMLSupport(zope.testrunner.feature.Feature):
    """JUnit XML Support"""

    def __init__(self, runner):
        super(JUnitXMLSupport, self).__init__(runner)
        self.active = True

    @classmethod
    def install_options(cls):
        if getattr(cls, '_options_installed', False):
            return
        cls._options_installed = True
        opts = optparse.OptionGroup(
            zope.testrunner.options.parser,
            "JUnit",
            """JUnit XML options.""")
        opts.add_option(
            '--xml',
            dest='xml_path',
            help="""Store XML output (one file) in the specified file path.""")
        zope.testrunner.options.parser.add_option_group(opts)

    def report(self):
        if not self.runner.options.xml_path:
            return
        self.runner.options.output.writeXMLReports()

    def global_setup(self):
        """Executed once when the test runner is being set up."""
        if not self.runner.options.xml_path:
            return
        self.runner.options.output = formatter.XMLOutputFormattingWrapper(
            self.runner.options.output, self.runner.options.xml_path)
