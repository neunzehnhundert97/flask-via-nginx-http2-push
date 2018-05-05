import functools
from typing import Union, Tuple, Callable

from flask import make_response
from werkzeug.wrappers import Response


def http2push(*urls: Union[str, Tuple[str]]):
    """
    Intercepts the returned response by a view function
    and adds the link header nginx can use to push resources

    :param urls: The relative urls to be pushed by nginx
    :return: The decorator itself
    """

    # Decorator wrapper
    def decorator(func: Callable):

        # Convert arguments into a list of strings or raises an exception
        if isinstance(urls, str):
            pushes = (urls,)
        elif isinstance(urls, Tuple):
            pushes = urls
        else:
            raise ValueError("")

        # Real decorator
        @functools.wraps(func)
        def headerAdder():

            # Executes view function and saves the return
            response = func()

            # Wraps the response in a Response object to use its functions
            if not isinstance(response, Response):
                response: Response = make_response(response)

            # Create empty list
            link = []

            # Iterate over all items to be pushed
            for push in pushes:
                # Format header part
                link.append("<{}>; rel=preload".format(push))

            # Sets the link header
            response.headers["Link"] = ", ".join(link)

            return response

        return headerAdder

    return decorator
