import unittest

from tests.unit.setup import setup, teardown

OLD_TEST_RUN = unittest.result.TestResult.startTestRun
OLD_TEST_STOP = unittest.result.TestResult.stopTestRun


def start_test_run(self):
    setup()
    OLD_TEST_RUN(self)


def stop_test_run(self):
    teardown()
    OLD_TEST_STOP(self)


unittest.result.TestResult.startTestRun = start_test_run
unittest.result.TestResult.stopTestRun = stop_test_run
