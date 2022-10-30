
[![Test](../../actions/workflows/test.yml/badge.svg)](../../actions/workflows/test.yml)

`Human! Do Task!` is a library for "half-assed" automation, created by Arlo Belshee and his company [Deep Roots](https://www.digdeeproots.com/). To learn more, see https://www.youtube.com/watch?v=ydq-KjGDRJg.

# Example usage

<!-- snippet: example_usage -->
<a id='snippet-example_usage'></a>
```py
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
    go.print_test_results()
```
<sup><a href='/example_usage.py#L3-L17' title='Snippet source file'>snippet source</a> | <a href='#snippet-example_usage' title='Start of snippet'>anchor</a></sup>
<!-- endSnippet -->
