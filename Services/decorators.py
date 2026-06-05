import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Czas wykonania wyniósł: {end-start}")
        return result
    return wrapper


def transaction_check(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        session = self.db
        try:
            result = func(self, *args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            print(e)
    return wrapper