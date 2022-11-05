import re
import textwrap
import typing
import approvaltests
import approvaltests.approvals
import contextlib
import io
import unittest
import unittest.mock

import example_usage
import human_do_task


def _scrub_timestamp(s: str) -> str:
    return re.sub(r"\d+:\d+:\d+(\.\d+)?", "{REMOVED}", s)


class redirect_stdin(contextlib._RedirectStream[typing.IO[str]]):
    _stream = "stdin"


def test__verify_happy_path__run() -> None:
    with contextlib.redirect_stdout(io.StringIO()) as stdout:
        with redirect_stdin(
            io.StringIO(
                textwrap.dedent(
                    """\
                    P
                    
                    
                    N
                    
                    
                    """
                )
            )
        ):
            human_do_task.Process.run(example_usage.perform, example_usage.verify)

    approvaltests.approvals.verify(
        stdout.getvalue(),
        options=approvaltests.Options().with_scrubber(_scrub_timestamp),
    )


def test__verify_happy_path__verify() -> None:
    with contextlib.redirect_stdout(io.StringIO()) as stdout:
        with unittest.mock.patch("builtins.input", side_effect=["V", "", "Y"]):
            human_do_task.Process.run(example_usage.perform, example_usage.verify)

    approvaltests.approvals.verify(
        stdout.getvalue(),
        options=approvaltests.Options().with_scrubber(_scrub_timestamp),
    )
