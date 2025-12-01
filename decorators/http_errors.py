import logging

from googleapiclient.errors import HttpError


def handle_http_errors(exception_type=HttpError, error_message="HttpError"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_type as error:
                logging.info(f"{error_message}: {error}.")
                return None  # обязателен

        return wrapper

    return decorator
