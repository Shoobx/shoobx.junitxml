###############################################################################
#
# Copyright 2017 by Plone Foundation and Shoobx, Inc.
#
###############################################################################
"""Shoobx JUnit XML Output Formatter
"""
import datetime
import doctest
import lxml.etree
import os
import os.path
import socket
import traceback
from zope.testrunner.find import StartUpFailure

try:
    import manuel.testing
    HAVE_MANUEL = True
except ImportError:
    HAVE_MANUEL = False


PRECISION = 5
STRFMT = "%." + str(PRECISION) + "f"


class TestSuiteInfo(object):

    def __init__(self):
        self.testCases = []
        self.errors = 0
        self.failures = 0
        self.time = 0.0

    @property
    def tests(self):
        return len(self.testCases)

    @property
    def successes(self):
        return self.tests - (self.errors + self.failures)


class TestCaseInfo(object):

    def __init__(self, test, time, testClassName, testName, failure=None,
                 error=None, extraData=None):
        self.test = test
        self.time = time
        self.testClassName = testClassName
        self.testName = testName
        self.failure = failure
        self.error = error
        self.extraData = extraData


def round_str(number):
    return STRFMT % round(number, PRECISION)


def get_test_class_name(test):
    """Compute the test class name from the test object."""
    return "%s.%s" % (test.__module__, test.__class__.__name__, )


def filename_to_suite_name_parts(filename):
    # lop off whatever portion of the path we have in common
    # with the current working directory; crude, but about as
    # much as we can do :(
    filenameParts = filename.split(os.path.sep)
    cwdParts = os.getcwd().split(os.path.sep)
    longest = min(len(filenameParts), len(cwdParts))
    for i in range(longest):
        if filenameParts[i] != cwdParts[i]:
            break

    if i < len(filenameParts) - 1:

        # The real package name couldn't have a '.' in it. This
        # makes sense for the common egg naming patterns, and
        # will still work in other cases

        # most zope packages source is in 'src', stop there

        suiteNameParts = []
        for part in reversed(filenameParts[i:-1]):
            if part == 'src' or '.' in part:
                break
            suiteNameParts.insert(0, part)

        # don't lose the filename, which would have a . in it
        suiteNameParts.append(filenameParts[-1])
        return suiteNameParts


def parse_layer(test):
    if isinstance(test, basestring):
        parts = test.split('.')
        klass = '.'.join(parts[:-1])
        return parts[-1], klass
    return None, None


def parse_doc_file_case(test):
    if not isinstance(test, doctest.DocFileCase):
        return None, None

    filename = test._dt_test.filename
    suiteNameParts = filename_to_suite_name_parts(filename)
    testName = test._dt_test.name
    testClassName = '.'.join(suiteNameParts[:-1])
    return testName, testClassName


def parse_doc_test_case(test):
    if not isinstance(test, doctest.DocTestCase):
        return None, None

    testDottedNameParts = test._dt_test.name.split('.')
    testClassName = get_test_class_name(test)
    testName = testDottedNameParts[-1]
    return testName, testClassName


def parse_manuel(test):
    if not (HAVE_MANUEL and isinstance(test, manuel.testing.TestCase)):
        return None, None
    filename = test.regions.location
    suiteNameParts = filename_to_suite_name_parts(filename)
    testName = suiteNameParts[-1]
    testClassName = '.'.join(suiteNameParts[:-1])
    return testName, testClassName


def parse_startup_failure(test):
    if not isinstance(test, StartUpFailure):
        return None, None
    testModuleName = test.module
    return 'Startup', testModuleName


def parse_unittest(test):
    testId = test.id()
    if testId is None:
        return None, None
    testClassName = get_test_class_name(test)
    testName = testId[len(testClassName)+1:]
    return testName, testClassName


class XMLOutputFormattingWrapper(object):
    """Output formatter which delegates to another formatter for all
    operations, but also prepares an element tree of test output.
    """

    def __init__(self, delegate, outputPath, outputSetupTeardown=True):
        self.delegate = delegate
        self.testSuite = TestSuiteInfo()
        self.outputPath = outputPath
        self.outputSetupTeardown = outputSetupTeardown

    def __getattr__(self, name):
        return getattr(self.delegate, name)

    def test_failure(self, test, seconds, exc_info):
        self._record(test, seconds, failure=exc_info)
        return self.delegate.test_failure(test, seconds, exc_info)

    def test_error(self, test, seconds, exc_info):
        self._record(test, seconds, error=exc_info)
        return self.delegate.test_error(test, seconds, exc_info)

    def test_success(self, test, seconds):
        self._record(test, seconds)
        return self.delegate.test_success(test, seconds)

    def test_skipped(self, test, reason):
        self._record(test, 0, extraData=dict(skipped=reason))
        return self.delegate.test_success(test, reason)

    def import_errors(self, import_errors):
        if import_errors:
            for test in import_errors:
                self._record(test, 0, error=test.exc_info)
        return self.delegate.import_errors(import_errors)

    def start_set_up(self, layer_name):
        """Report that we're setting up a layer."""
        self._last_layer = layer_name
        return self.delegate.start_set_up(layer_name)

    def stop_set_up(self, seconds):
        layer_name = self._last_layer
        self._last_layer = None
        if self.outputSetupTeardown:
            self._record('%s:setUp' % (layer_name,), seconds)
        return self.delegate.stop_set_up(seconds)

    def start_tear_down(self, layer_name):
        """Report that we're tearing down a layer."""
        self._last_layer = layer_name
        return self.delegate.start_tear_down(layer_name)

    def stop_tear_down(self, seconds):
        layer_name = self._last_layer
        self._last_layer = None
        if self.outputSetupTeardown:
            self._record('%s:tearDown' % (layer_name,), seconds)
        return self.delegate.stop_tear_down(seconds)

    def tear_down_not_supported(self):
        """Report that we could not tear down a layer."""
        layer_name = self._last_layer
        self._last_layer = None
        self._record('%s:tearDown' % (layer_name,), 0,
                     extraData=dict(skipped=u'Not supported'))
        return self.delegate.tear_down_not_supported()

    def _record(self, test, seconds, failure=None, error=None,
                extraData=None):
        for parser in [parse_layer,
                       parse_doc_file_case,
                       parse_doc_test_case,
                       parse_manuel,
                       parse_startup_failure,
                       parse_unittest]:
            testName, testClassName = parser(test)
            if (testName, testClassName) != (None, None):
                break

        if (testName, testClassName) == (None, None):
            raise TypeError(
                "Unknown test type: Could not compute testName, "
                "testClassName: %r" % test)

        self.testSuite.testCases.append(
            TestCaseInfo(
                test, seconds, testClassName, testName,
                failure, error, extraData))

        if failure is not None:
            self.testSuite.failures += 1

        if error is not None:
            self.testSuite.errors += 1

        if seconds:
            self.testSuite.time += seconds

    def writeXMLReports(self, properties=None):
        testSuiteNode = lxml.etree.Element(
            'testsuite',
            tests=str(self.testSuite.tests),
            errors=str(self.testSuite.errors),
            failures=str(self.testSuite.failures),
            hostname=socket.gethostname(),
            name='',
            time=round_str(self.testSuite.time),
            timestamp=datetime.datetime.now().isoformat()
        )

        propertiesNode = lxml.etree.SubElement(testSuiteNode, 'properties')
        for k, v in (properties or {}).items():
            lxml.etree.SubElement(
                propertyNode, 'property', name=k, value=v)

        for testCase in self.testSuite.testCases:
            testCaseNode = lxml.etree.SubElement(
                testSuiteNode, 'testcase',
                classname=testCase.testClassName,
                name=testCase.testName,
                time=round_str(testCase.time))

            if testCase.error:
                errorNode = lxml.etree.SubElement(testCaseNode, 'error')
                try:
                    excType, excInstance, tb = testCase.error
                    errorMessage = str(excInstance)
                    stackTrace = ''.join(traceback.format_tb(tb))
                finally: # Avoids a memory leak
                    del tb
                errorNode.attrib.update({
                    'message': errorMessage.split('\n')[0],
                    'type': str(excType)
                })
                errorNode.text = errorMessage + '\n\n' + stackTrace

            if testCase.failure:
                failureNode = lxml.etree.SubElement(testCaseNode, 'failure')
                try:
                    excType, excInstance, tb = testCase.failure
                    errorMessage = str(excInstance)
                    stackTrace = ''.join(traceback.format_tb(tb))
                except UnicodeEncodeError:
                    errorMessage = \
                      'Could not extract error str for unicode error'
                    stackTrace = ''.join(traceback.format_tb(tb))
                finally: # Avoids a memory leak
                    del tb
                failureNode.attrib.update({
                    'message': errorMessage.split('\n')[0],
                    'type': str(excType)
                })
                failureNode.text = errorMessage + '\n\n' + stackTrace

            if testCase.extraData is not None:
                for key, val in testCase.extraData.items():
                    newNode = lxml.etree.SubElement(testCaseNode, key)
                    newNode.text = val

        # XXX: We don't have a good way to capture these yet
        systemOutNode = lxml.etree.SubElement(testSuiteNode, 'system-out')
        systemErrNode = lxml.etree.SubElement(testSuiteNode, 'system-err')

        # Write file
        with open(self.outputPath, 'w') as file:
            file.write(lxml.etree.tostring(testSuiteNode, pretty_print=True))
