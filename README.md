
[![Test](../../actions/workflows/test.yml/badge.svg)](../../actions/workflows/test.yml)

`Human! Do Task!` is a library for "half-assed" automation, created by Arlo Belshee and his company [Deep Roots](https://www.digdeeproots.com/). To learn more, see https://www.youtube.com/watch?v=ydq-KjGDRJg.

# Example usage

<!-- snippet: example_usage -->
<a id='snippet-example_usage'></a>
```py
def perform(go):
    go.tell("Please do such and such.")
    go.tell("Please do something else for me.")
    go.ask(
        "Are the lights on?", lambda: go.tell("Please turn off the circuit breaker.")
    )
    go.tell("Please do one more thing.")

def verify(go):
    go.tell("Please do something.")
    go.verify(go.that("the thing is colored blue"))
    go.print_test_result()
```
<sup><a href='/example_usage.py#L3-L17' title='Snippet source file'>snippet source</a> | <a href='#snippet-example_usage' title='Start of snippet'>anchor</a></sup>
<!-- endSnippet -->
