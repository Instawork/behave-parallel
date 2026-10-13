# -*- coding: UTF-8 -*-

from __future__ import absolute_import

from types import SimpleNamespace

from behave.runner_mp import MultiProcRunner


def _runner(hooks, dry_run=False):
    runner = object.__new__(MultiProcRunner)
    runner.hooks = hooks
    runner.config = SimpleNamespace(dry_run=dry_run)
    return runner


def test_hook_runs_once_with_a_context():
    calls = []
    runner = _runner({"before_workers": calls.append})

    runner.run_before_workers_hook()

    assert len(calls) == 1
    assert calls[0] is runner.context


def test_missing_hook_is_a_noop():
    runner = _runner({})

    runner.run_before_workers_hook()

    assert not hasattr(runner, "context")


def test_hook_is_skipped_on_dry_run():
    calls = []
    runner = _runner({"before_workers": calls.append}, dry_run=True)

    runner.run_before_workers_hook()

    assert calls == []


def test_hook_failure_is_reported_and_does_not_abort(capsys):
    def failing_hook(context):
        raise RuntimeError("boom")

    runner = _runner({"before_workers": failing_hook})

    runner.run_before_workers_hook()

    assert "HOOK-ERROR in before_workers: RuntimeError: boom" in capsys.readouterr().out
