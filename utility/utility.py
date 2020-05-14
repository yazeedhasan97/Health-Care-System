import functools
import random
import string
import functools


def centerWindow(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def singleton(cls):
    """Make a class a Singleton class (only one instance)"""

    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance

    wrapper_singleton.instance = None
    return wrapper_singleton


def random_alphaNumeric_password(lettersCount, digitsCount):
    sampleStr = ''.join((random.choice(string.ascii_letters) for i in range(lettersCount)))
    sampleStr += ''.join((random.choice(string.digits) for i in range(digitsCount)))

    # Convert string to list and shuffle it to mix letters and digits
    sampleList = list(sampleStr)
    random.shuffle(sampleList)
    finalString = ''.join(sampleList)
    return finalString


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        x = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__} Took {end - start} Time to excute')
        return x

    return wrapper


if __name__ == '__main__':
    print(random_alphaNumeric_password(10, 5))
