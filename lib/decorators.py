
import time
from django.db import connection, reset_queries


def db_debugger(func):
    def wrapper(*args, **kwargs):
        reset_queries()
        start_time = time.time()
        value = func(*args, **kwargs)
        end_time = time.time()
        queries = len(connection.queries)
        print(
            f'----------------------\n connection_num: {queries} \n duration: {(end_time - start_time):.3f} \n----------------------')
        return value

    return wrapper


