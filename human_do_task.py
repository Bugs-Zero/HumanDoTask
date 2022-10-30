from __future__ import annotations

import datetime
import traceback
import typing


class Clock(object):
    started: typing.Optional[datetime.datetime]

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.accumulator = datetime.timedelta(0)
        self.started = None

    def start(self) -> None:
        if not self.started:
            self.started = datetime.datetime.utcnow()

    def stop(self) -> None:
        if self.started:
            self.accumulator += datetime.datetime.utcnow() - self.started
            self.started = None

    @property
    def elapsed(self) -> datetime.timedelta:
        if self.started:
            return self.accumulator + (datetime.datetime.utcnow() - self.started)
        return self.accumulator

    def __repr__(self) -> str:
        return "<Clock {} ({})>".format(
            self.elapsed, "started" if self.started else "stopped"
        )


def _query(
    prefix: list[str], question: str, first_answer: str, second_answer: str
) -> bool:
    for item in prefix:
        print(item)
    return (
        input(f"{question} ({first_answer}/{second_answer})")
        .lower()
        .startswith(first_answer.lower())
    )


class ManualSection:
    def __init__(self, go: Process) -> None:
        self.go = go

    def __enter__(self) -> None:
        self.go._automated.stop()
        self.go._manual.start()

    def __exit__(
        self,
        exception_type: typing.Optional[type[BaseException]],
        exception: typing.Optional[BaseException],
        exception_traceback: typing.Optional[traceback.TracebackException],
    ) -> None:
        self.go._manual.stop()
        self.go._automated.start()


class Process:
    def __init__(self) -> None:
        self._automated = Clock()
        self._automated.start()
        self._manual = Clock()
        self._test_result: list[str] = []
        self._automated_steps = 0
        self._manual_steps = 0

    @staticmethod
    def run(
        perform: typing.Callable[[Process], None],
        verify: typing.Callable[[Process], None],
    ) -> None:
        go = Process()
        with ManualSection(go):
            do_perform = _query(
                [], "Do you wish to perform the process or verify it?", "P", "V"
            )
        if do_perform:
            perform(go)
        else:
            verify(go)
        go._print_stats()

    def do(self, operation: typing.Callable[[], None]) -> None:
        self._automated_steps += 1
        operation()

    def tell(self, message: str) -> None:
        self._manual_steps += 1
        with ManualSection(self):
            print(message)
            input("press enter when done")

    def ask(self, condition: str, operation: typing.Callable[[], None]) -> None:
        self._manual_steps += 1
        with ManualSection(self):
            should_do_it = _query([condition], "Should I perform this step?", "Y", "N")
        if should_do_it:
            operation()

    def ask_yes_no(self, condition: str) -> bool:
        self._manual_steps += 1
        with ManualSection(self):
            return _query([condition], "Should I perform this step?", "Y", "N")

    # Conflicts with built-in keyword `if`. TODO: pick a non-conflicting name.
    #    def if(self, condition, operation) -> None:
    #       self._automatic_steps += 1
    #       if(condition()):
    #          operation()

    def verify(self, condition: typing.Callable[[], bool]) -> None:
        initial = self._manual_steps
        if not condition():
            self._test_result.append(f"Failed expectation: {condition}")
        if initial == self._manual_steps:
            self._automated_steps += 1

    def that(self, condition: str) -> typing.Callable[[], bool]:
        def impl() -> bool:
            self._manual_steps += 1
            with ManualSection(self):
                return _query(
                    [f"Please verify whether {condition}."], "Is this right?", "Y", "N"
                )

        return impl

    def print_test_results(self) -> None:
        if self._test_result:
            print("Verification failed. Please fix the process and try again.")
        for failure in self._test_result:
            print(failure)

    def _print_stats(self) -> None:
        self._automated.stop()
        total_time = self._automated.elapsed + self._manual.elapsed
        print(f"Process complete in {total_time}.")
        print(
            f"   Automated: {self._automated_steps} steps in {self._automated.elapsed}."
        )
        print(f"   Manual: {self._manual_steps} steps in {self._manual.elapsed}.")
