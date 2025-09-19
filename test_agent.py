#!/usr/bin/env python3

from human_do_task import Process


def perform(go: Process) -> None:
    go.tell("Starting process with agent interaction")

    response = go.agent("What is 2+2?")
    print(f"Agent response: {response}")

    go.tell("Process complete")


def verify(go: Process) -> None:
    go.tell("Verification not implemented")


if __name__ == "__main__":
    Process.run(perform, verify)