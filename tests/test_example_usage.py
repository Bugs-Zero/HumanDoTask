import re
import approvaltests
import approvaltests.approvals
import contextlib
import io
import unittest
import unittest.mock

import example_usage
import human_do_task


def test__verify_happy_path() -> None:
    with contextlib.redirect_stdout(io.StringIO()) as stdout:
        with unittest.mock.patch("builtins.input", side_effect=["V", "", "Y"]):
            human_do_task.Process.run(example_usage.perform, example_usage.verify)

    approvaltests.approvals.verify(
        stdout.getvalue(),
        options=approvaltests.Options().with_scrubber(
            lambda s: re.sub(r"\d+:\d+:\d+(\.\d+)?", "{REMOVED}", s)
        ),
    )
