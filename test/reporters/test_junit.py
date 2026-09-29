# -*- coding: UTF-8 -*-

from __future__ import absolute_import
import shutil
import tempfile
from mock import Mock
from behave.model_core import Status
from behave.parser import parse_feature
from behave.reporter.junit import JUnitReporter

FEATURE_TEXT = u"""
Feature: Tabs navigation
  Scenario: Navigate all tabs
    Given a step
"""


class TestJUnitReporter(object):
    def setup_method(self, method):
        self.junit_directory = tempfile.mkdtemp()

    def teardown_method(self, method):
        shutil.rmtree(self.junit_directory)

    def make_reporter(self):
        config = Mock(
            junit_directory=self.junit_directory,
            paths=[],
            base_dir=".",
            show_skipped=False,
            userdata={},
        )
        return JUnitReporter(config)

    def test_failed_scenario_without_failing_step_or_traceback(self):
        feature = parse_feature(FEATURE_TEXT, filename="navigation.feature")
        scenario = feature.scenarios[0]
        scenario.hook_failed = True
        scenario.set_status(Status.failed)
        assert scenario.exc_traceback is None

        self.make_reporter().feature(feature)

        with open("%s/TESTS-navigation.xml" % self.junit_directory) as f:
            report = f.read()
        assert 'failures="1"' in report or 'errors="1"' in report
        assert "Navigate all tabs" in report
