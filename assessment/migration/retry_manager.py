import time


def retry_operation(
        function,
        retries=3,
        delay=5,
        *args,
        **kwargs):

    for attempt in range(retries):

        try:

            return function(
                *args,
                **kwargs
            )

        except Exception as error:

            print(
                f"Retry {attempt + 1} failed:"
                f" {error}"
            )

            time.sleep(delay)

    raise Exception(
        "Maximum retries exceeded"
    )