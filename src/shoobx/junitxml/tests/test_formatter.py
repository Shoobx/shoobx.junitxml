###############################################################################
#
# Copyright 2017 by Plone Foundation and Shoobx, Inc.
#
###############################################################################
"""Shoobx JUnit XML Output Formatter Tests
"""
import mock
import unittest
import sys

from shoobx.junitxml import formatter


class SomeTest(object):

    def id(self):
        return 'shoobx.junitxml.tests.test_formatter.SomeTest'


class XMLOutputFormattingWrapperTest(unittest.TestCase):

    def setUp(self):
        self.delegate = mock.Mock()
        self.formatter = formatter.XMLOutputFormattingWrapper(
            self.delegate, '.')

    def test__getattr__(self):
        self.delegate.someAttr = 123
        self.assertEqual(123, self.formatter.someAttr)

    def test_test_failure(self):
        exc_info = mock.Mock()

        self.formatter.test_failure(SomeTest(), 0.088, exc_info,
                                    stderr=sys.stderr, stdout=sys.stdout)
        self.assertTrue(
            self.delegate.test_failure.called)
        self.assertEqual(
            1, len(self.formatter.testSuite.testCases))
        self.assertEqual(
            1, self.formatter.testSuite.failures)

    def test_test_error(self):
        exc_info = mock.Mock()
        self.formatter.test_error(SomeTest(), 0.088, exc_info,
                                  stderr=sys.stderr, stdout=sys.stdout)
        self.assertTrue(
            self.delegate.test_error.called)
        self.assertEqual(
            1, len(self.formatter.testSuite.testCases))
        self.assertEqual(
            1, self.formatter.testSuite.errors)

    def test_test_success(self):
        self.formatter.test_success(SomeTest(), 0.088)
        self.assertTrue(
            self.delegate.test_success.called)
        self.assertEqual(
            1, len(self.formatter.testSuite.testCases))

    def test_test_skipped(self):
        self.formatter.test_skipped(SomeTest(), u'Server unavailable')
        self.assertTrue(
            self.delegate.test_skipped.called)
        self.assertEqual(
            1, len(self.formatter.testSuite.testCases))

    def test_import_errors(self):
        exc_info = mock.Mock()
        from zope.testrunner.find import StartUpFailure
        errors = [StartUpFailure(
            mock.Mock(post_mortem=False),
            'shoobx.junitxml.tests.test_formatter', exc_info)]
        self.formatter.import_errors(errors)
        self.assertTrue(
            self.delegate.import_errors.called)
        self.assertEqual(
            1, len(self.formatter.testSuite.testCases))

    def test_start_stop_set_up(self):
        self.formatter.start_set_up('test_layer')
        self.assertTrue(self.delegate.start_set_up.called)
        self.formatter.stop_set_up(0.888)
        self.assertTrue(self.delegate.stop_set_up.called)
        self.assertEqual(
            1, len(self.formatter.testSuite.testCases))

    def test_start_stop_set_up_unicode_name(self):
        self.formatter.start_set_up(u'test_layer')
        self.assertTrue(self.delegate.start_set_up.called)
        self.formatter.stop_set_up(0.888)
        self.assertTrue(self.delegate.stop_set_up.called)
        self.assertEqual(
            1, len(self.formatter.testSuite.testCases))

    def test_start_stop_tear_down(self):
        self.formatter.start_tear_down('test_layer')
        self.assertTrue(self.delegate.start_tear_down.called)
        self.formatter.stop_tear_down(0.888)
        self.assertTrue(self.delegate.stop_tear_down.called)
        self.assertEqual(
            1, len(self.formatter.testSuite.testCases))

    def test_start_stop_tear_down_unicode_name(self):
        self.formatter.start_tear_down(u'test_layer')
        self.assertTrue(self.delegate.start_tear_down.called)
        self.formatter.stop_tear_down(0.888)
        self.assertTrue(self.delegate.stop_tear_down.called)
        self.assertEqual(
            1, len(self.formatter.testSuite.testCases))

    def test_tear_down_not_supported(self):
        self.formatter.start_tear_down(u'test_layer')
        self.assertTrue(self.delegate.start_tear_down.called)
        self.formatter.tear_down_not_supported()
        self.assertTrue(self.delegate.tear_down_not_supported.called)
        self.assertEqual(
            1, len(self.formatter.testSuite.testCases))
