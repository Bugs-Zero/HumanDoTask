import re
import textwrap
import typing
import approvaltests
import approvaltests.approvals
from approvaltests.core.options import Options
import contextlib
import io
import sys

import example_usage
import human_do_task


def _scrub_timestamp(s: str) -> str:
    return re.sub(r"\d+:\d+:\d+(\.\d+)?", "{REMOVED}", s)


# Older Python doesn't handle the generic type parameter
if sys.version_info >= (3, 10) or typing.TYPE_CHECKING:
    _RedirectStream = contextlib._RedirectStream[io.StringIO]
else:
    _RedirectStream = contextlib._RedirectStream


class redirect_stdin(_RedirectStream):
    _stream = "stdin"


@contextlib.contextmanager
def capture_io(
    input: str,
) -> typing.Generator[io.StringIO, None, None]:
    with contextlib.redirect_stdout(io.StringIO()) as stdout:
        with redirect_stdin(io.StringIO(input)):
            yield stdout


def test__verify_happy_path__run() -> None:
    with capture_io(
        textwrap.dedent(
            """\
            P


            N


            """
        )
    ) as stdout:
        human_do_task.Process.run(example_usage.perform, example_usage.verify)

    approvaltests.approvals.verify(
        stdout.getvalue(),
        options=Options().with_scrubber(_scrub_timestamp),
    )


def test__verify_happy_path__verify() -> None:
    with capture_io(
        textwrap.dedent(
            """\
        V

        Y

        """
        )
    ) as stdout:
        human_do_task.Process.run(example_usage.perform, example_usage.verify)

    approvaltests.approvals.verify(
        stdout.getvalue(),
        options=Options().with_scrubber(_scrub_timestamp),
    )
