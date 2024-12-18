###############################################################################
#
# Copyright 2017 by Plone Foundation and Shoobx, Inc.
#
###############################################################################
"""Shoobx JUnit XML Output feature
"""
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

        group = zope.testrunner.options.parser.add_argument_group(
            "JUnit",
            """JUnit XML options.""")
        group.add_argument(
            '--junitxml',
            dest='xml_path',
            help="""Store XML output (one file) in the specified file path.""")

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
