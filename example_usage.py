from human_do_task import Process

# begin-snippet: example_usage
def perform(go: Process) -> None:
    go.tell("Please lorem.")
    go.tell("Please ipsum.")
    go.ask(
        "Are the lights on?", lambda: go.tell("Please turn off the circuit breaker.")
    )
    go.tell("Please do one more thing.")


def verify(go: Process) -> None:
    go.tell("Please do something.")
    go.verify(go.that("the thing is colored blue"))
    # end-snippet


if __name__ == "__main__":
    Process.run(perform, verify)
